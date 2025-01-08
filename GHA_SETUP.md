# Sample AOAI App Configuration for CI/CD Pipelines

This guide provides instructions to configure your Sample AOAI App GitHub repository for CI/CD workflows. It covers creating environments, setting up secrets specific to each environment, configuring necessary environment variables, creating Azure App Registrations for each environment, and ensuring all configurations are correctly in place.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environments Setup](#environments-setup)
3. [Azure App Registrations](#azure-app-registrations)
4. [Secrets Configuration](#secrets-configuration)
5. [Environment Variables Configuration](#environment-variables-configuration)
6. [Workflow Files Overview](#workflow-files-overview)
7. [Additional Configurations](#additional-configurations)
8. [Conclusion](#conclusion)

---

## Prerequisites

Before proceeding, ensure you have the following:

- **GitHub Repository Access:** Administrative access to the GitHub repository where the workflows will be configured.
- **Azure Account:** An active Azure account with the necessary permissions to create and manage resources.
- **Azure Dev CLI (`azd`):** Installed and configured on your local machine for provisioning Azure resources.
- **Service Principal:** Created in Azure for authentication purposes.
- **Azure App Registrations:** Separate App Registrations for `dev` and `prod` environments.

---

## Environments Setup

The workflows require two environments: `dev` and `prod`. Environments in GitHub Actions help manage deployments and control access to sensitive information.

### Creating Environments

1. **Navigate to Your Repository:**

   - Go to your GitHub repository.

2. **Access Settings:**

   - Click on the `Settings` tab at the top of the repository page.

3. **Add Environments:**

   - In the left sidebar, click on `Environments`.
   - Click the `New environment` button.

4. **Create `dev` Environment:**

   - **Name:** `dev`
   - **Optional Configurations:**
     - **Environment Protection Rules:** Configure rules such as required reviewers or wait timers if needed.
   - Click `Configure environment` to finalize.

5. **Create `prod` Environment:**

   - Repeat the above steps with the **Name:** `prod`.

---

## Azure App Registrations

Each environment (`dev` and `prod`) requires its own Azure App Registration to handle authentication and authorization. This ensures environment isolation and security.

### Creating an App Registration for Each Environment

Follow these steps to create an App Registration in the Azure Portal for both `dev` and `prod` environments.

#### 1. Navigate to Azure Active Directory

- Log in to the [Azure Portal](https://portal.azure.com).
- Search for and select **Azure Active Directory** from the search bar.

#### 2. Create a New App Registration

1. **Access App Registrations:**

   - In the Azure Active Directory menu, select **App registrations**.

2. **Add a New Registration:**

   - Click **+ New registration**.

3. **Provide Registration Details:**

   - **Name:** Enter a name for your application (e.g., `WebApp-Dev` for the dev environment and `WebApp-Prod` for the prod environment).
   - **Supported account types:** Select the appropriate option (e.g., "Accounts in this organizational directory only").
   - **Redirect URI:**
     - **Platform:** Click on **Add a platform**.
     - **Select Platform:** Choose **Web**.
     - **Redirect URIs:** Enter the URI `http://localhost:5000/.auth/login/aad/callback`.
   - **Implicit Grant and Hybrid Flows:**
     - **Select:** Check the box for **ID tokens (used for implicit and hybrid flows)**.
   - Click **Register**.

   ![Add Web Platform, Redirect URI, and ID Tokens](https://example.com/path-to-your-image.png) *(Replace with actual image if available)*

   > **Note:** Selecting **ID tokens (used for implicit and hybrid flows)** is essential for enabling authentication flows that rely on ID tokens, such as implicit and hybrid OAuth 2.0 flows. This ensures that your application can securely handle user authentication.

#### 3. Note the Application (client) ID and Directory (tenant) ID

- After registration, you will be redirected to the application's **Overview** page.
- **Copy** the **Application (client) ID** and **Directory (tenant) ID** for later use.

#### 4. Add a Client Secret

1. **Navigate to Certificates & Secrets:**

   - In the app registration menu, select **Certificates & secrets**.

2. **Create a New Client Secret:**

   - Under **Client secrets**, click **+ New client secret**.
   - **Description:** Enter a description (e.g., `DefaultClientSecret-Dev` or `DefaultClientSecret-Prod`).
   - **Expires:** Set an expiration period (e.g., 6 months, 12 months, or a custom period).
   - Click **Add**.

3. **Copy the Client Secret Value:**

   - The newly created client secret will appear under **Client secrets**.
   - **Copy** the **Value** immediately. **You will not be able to view it again after navigating away from this page.**

#### 5. App Registration Details

For each environment (`dev` and `prod`), note down the `Application (client) ID`, `Directory (tenant) ID`, and `Client Secret Value`.

---

## Secrets Configuration

The workflows rely on secrets for authentication and configuration. These secrets should be securely stored and scoped to their respective environments (`dev` and `prod`) to ensure that each environment uses its own set of credentials.

### Secrets Table

| Secret Name           | Usage                                       | Workflow(s)           | Environment   |
| --------------------- | ------------------------------------------- | --------------------- | ------------- |
| `AZURE_CREDENTIALS`   | Authenticates GitHub Actions with Azure.    | All pipelines         | `dev`, `prod` |
| `AZURE_OPENAI_KEY`    | Authenticates requests to Azure OpenAI.     | Pull Request pipeline | `dev`, `prod` |
| `AUTH_APP_ID`         | App registration's Directory (tenant) ID.   | All pipelines         | `dev`, `prod` |
| `AUTH_CLIENT_ID`      | App registration's Application (client) ID. | All pipelines         | `dev`, `prod` |
| `AUTH_CLIENT_SECRET`  | App registration's Client Secret.           | All pipelines         | `dev`, `prod` |

---

## Environment Variables Configuration

In addition to secrets, the workflows require specific environment variables for each environment. These variables are used as follows:

### Environment Variables Table

| Variable Name                 | Usage                                                | Workflow(s)           | Environment   |
| ----------------------------- | ---------------------------------------------------- | --------------------- | ------------- |
| `AZURE_ENV_NAME`              | Specifies the Azure Dev environment name.            | Deployment pipelines  | `dev`, `prod` |
| `AZURE_LOCATION`              | Specifies the Azure region for resources.            | Deployment pipelines  | `dev`, `prod` |
| `AZURE_SUBSCRIPTION_ID`       | Specifies the Azure subscription ID.                 | Deployment pipelines  | `dev`, `prod` |
| `AZURE_OPENAI_ENDPOINT`       | Specifies the endpoint URL for Azure OpenAI.         | Pull Request pipeline | `dev`, `prod` |
| `AZURE_OPENAI_MODEL`          | Specifies the Azure OpenAI model name.               | Pull Request pipeline | `dev`, `prod` |
| `AZURE_OPENAI_EMBEDDING_NAME` | Specifies the embedding model name for Azure OpenAI. | Pull Request pipeline | `dev`, `prod` |

---

## Workflow Files Overview

The repository includes three key GitHub Actions workflows to manage CI/CD processes effectively. These workflows are located in the `.github/workflows` directory:

1. **Deploy to Development (`cd-pipeline-dev.yml`)**  
   Automates provisioning and deployment to the `dev` environment. Triggered by changes to the `develop` branch, it ensures the development environment is updated with the latest resources and application state.

2. **Deploy to Production (`cd-pipeline-prd.yml`)**  
   Handles provisioning and deployment to the `prod` environment. Triggered by changes to the `main` branch, this workflow ensures production updates are executed with the necessary configurations for stability and security.

3. **Pull Request Pipeline (`pr-pipeline.yml`)**  
   Focuses on validating code quality and application behavior for pull requests targeting the `develop` branch. It includes steps for running tests and generating reports for both backend and frontend components.

Each workflow is designed to ensure environment-specific configurations are applied, leveraging secrets, environment variables, and pre-defined triggers for seamless automation.

---

## Additional Configurations

### Branch Protection Rules

Optionally, you can set branch protection rules for the `main` and `develop` branches to enforce workflow execution and maintain code quality.

1. **Navigate to Branches:**

   - In `Settings` > `Branches`.

2. **Add Branch Protection:**

   - Click `Add rule`.
   - Specify the branch name pattern (e.g., `main`, `develop`).
   - **Configure Protections:**
     - **Require pull request reviews before merging.**
     - **Require status checks to pass before merging:** Select the relevant workflows.
     - **Include administrators** if you want the rules to apply to repository administrators.
   - Click `Create` to finalize.

---

For any further assistance or advanced configurations, refer to the [GitHub Actions Documentation](https://docs.github.com/en/actions) and the [Azure Dev CLI Documentation](https://learn.microsoft.com/en-us/azure/developer/azure-devs-cli/).