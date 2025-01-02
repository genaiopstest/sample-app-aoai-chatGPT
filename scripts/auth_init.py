import argparse
import subprocess

from azure.identity import AzureDeveloperCliCredential
import urllib3
import requests
import json

def get_auth_headers(credential):
    return {
        "Authorization": "Bearer "
        + credential.get_token("https://graph.microsoft.com/.default").token
    }


def check_for_application(credential, app_id):
    resp = urllib3.request(
        "GET",
        f"https://graph.microsoft.com/v1.0/applications/{app_id}",
        headers=get_auth_headers(credential),
    )
    if resp.status != 200:
        print("Application not found")
        return False
    return True

import requests
import json

def create_application(credential):
    headers = get_auth_headers(credential)
    
    # Ensure the Content-Type header is set to application/json
    headers["Content-Type"] = "application/json"
    
    url = "https://graph.microsoft.com/v1.0/applications"

    payload = {
        "displayName": "WebApp",
        "signInAudience": "AzureADMyOrg",  # Changed from 'AzureADandPersonalMicrosoftAccount'
        "web": {
            "redirectUris": ["http://localhost:5000/.auth/login/aad/callback"],
            "implicitGrantSettings": {"enableIdTokenIssuance": True},
        },
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,  # requests handles JSON encoding
            timeout=(10, 10)  # (connect timeout, read timeout)
        )

        # Debugging: Print response status and body
        print(f"Create Application Response Status: {response.status_code}")
        print(f"Create Application Response Body: {response.text}")

        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()

        data = response.json()
        app_id = data["id"]
        client_id = data["appId"]

        return app_id, client_id

    except requests.exceptions.HTTPError as http_err:
        print("Failed to create application.")
        try:
            error_info = response.json()
            print("Error details:", error_info)
        except json.JSONDecodeError:
            print("Response is not in JSON format.")
        raise  # Re-raise the exception after logging

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        raise  # Re-raise the exception after logging

    except (KeyError, json.JSONDecodeError) as e:
        print("Failed to parse response JSON:", e)
        print("Response data:", response.text)
        raise KeyError("'id' or 'appId' not found in response") from e


from datetime import datetime, timedelta

def add_client_secret(credential, app_id):
    """
    Adds a client secret to the Azure AD application and returns the secret text.

    :param credential: Authentication credentials (e.g., Bearer token)
    :param app_id: The Application (client) ID of the Azure AD application
    :return: The client secret text
    """
    headers = get_auth_headers(credential)
    headers["Content-Type"] = "application/json"

    # Define the API endpoint
    url = f"https://graph.microsoft.com/v1.0/applications/{app_id}/addPassword"

    # Define the password credential
    # Adjust the expiry as needed (e.g., 180 days from now)
    expiry_days = 180  # Change this value based on your policy
    expiry_date = (datetime.utcnow() + timedelta(days=expiry_days)).isoformat() + "Z"

    payload = {
        "passwordCredential": {
            "displayName": "DefaultClientSecret",
            "endDateTime": expiry_date,
            "startDateTime": datetime.utcnow().isoformat() + "Z"
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,  # requests handles JSON encoding
            timeout=(10, 10)  # (connect timeout, read timeout)
        )

        # Debugging: Print response status and body
        print(f"Add Client Secret Response Status: {response.status_code}")
        print(f"Add Client Secret Response Body: {response.text}")

        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()

        data = response.json()

        # Extract the secretText
        client_secret = data.get("secretText")
        if not client_secret:
            print("Failed to retrieve 'secretText' from the response.")
            print("Full response:", data)
            raise KeyError("'secretText' not found in the response.")

        return client_secret

    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred while adding client secret:", http_err)
        try:
            error_info = response.json()
            print("Error details:", json.dumps(error_info, indent=2))
        except json.JSONDecodeError:
            print("Response is not in JSON format.")
        raise  # Re-raise the exception after logging

    except requests.exceptions.RequestException as err:
        print(f"An error occurred while adding client secret: {err}")
        raise  # Re-raise the exception after logging

    except KeyError as e:
        print(f"Key error: {e}")
        raise  # Re-raise the exception after logging


def update_azd_env(name, val):
    subprocess.run(f"azd env set {name} {val}", shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an App Registration and client secret (if not already created)",
        epilog="Example: auth_update.py",
    )
    parser.add_argument(
        "--appid",
        required=False,
        help="Optional. ID of registered application. If provided, this script just makes sure it exists.",
    )
    args = parser.parse_args()

    credential = AzureDeveloperCliCredential()

    if args.appid and args.appid != "no-id":
        print(f"Checking if application {args.appid} exists")
        if check_for_application(credential, args.appid):
            print("Application already exists, not creating new one.")
            exit(0)

    print("Creating application registration")
    app_id, client_id = create_application(credential)

    print(f"Adding client secret to {app_id}")
    client_secret = add_client_secret(credential, app_id)

    print("Updating azd env with AUTH_APP_ID, AUTH_CLIENT_ID, AUTH_CLIENT_SECRET")
    update_azd_env("AUTH_APP_ID", app_id)
    update_azd_env("AUTH_CLIENT_ID", client_id)
    update_azd_env("AUTH_CLIENT_SECRET", client_secret)
