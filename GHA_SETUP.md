# GitHub Repository Configuration for CI/CD Workflows

This guide provides comprehensive instructions to configure your GitHub repository to support the provided CI/CD workflows. It covers creating environments, setting up secrets specific to each environment, configuring environment variables necessary for the workflows to run successfully, and ensuring all necessary configurations are in place.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environments Setup](#environments-setup)
3. [Secrets Configuration](#secrets-configuration)
4. [Environment Variables Configuration](#environment-variables-configuration)
5. [Workflow Files Overview](#workflow-files-overview)
6. [Additional Configurations](#additional-configurations)
7. [Conclusion](#conclusion)

---

## Prerequisites

Before proceeding, ensure you have the following:

- **GitHub Repository Access:** Administrative access to the GitHub repository where the workflows will be configured.
- **Azure Account:** An active Azure account with the necessary permissions to create and manage resources.
- **Azure Dev CLI (`azd`):** Installed and configured on your local machine for provisioning Azure resources.
- **Service Principal:** Created in Azure for authentication purposes.

---

## Environments Setup

The workflows require two environments: `dev` and `prod`. Environments in GitHub Actions help manage deployments and control access to sensitive information.

### Creating Environments

1. **Navigate to Your Repository:**
   - Go to your GitHub repository.

2. **Access Settings:**
   - Click on the `Settings` tab located at the top of the repository page.

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

## Secrets Configuration

The workflows rely on secrets for authentication and configuration. These secrets should be securely stored and scoped to their respective environments (`dev` and `prod`) to ensure that each environment uses its own set of credentials.

### Adding Environment-Specific Secrets

GitHub allows you to define secrets at both the repository and environment levels. For enhanced security and environment isolation, secrets should be defined within each environment (`dev` and `prod`).

#### 1. Secrets for `dev` Environment

These secrets are specific to the `dev` environment and are used by workflows that deploy to development resources.

| Secret Name         | Description                                         | Usage                                            |
| ------------------- | --------------------------------------------------- | ------------------------------------------------ |
| `AZURE_CREDENTIALS` | Azure service principal credentials in JSON format. | Authenticates GitHub Actions with Azure for dev. |
| `AZURE_OPENAI_KEY`  | API key for Azure OpenAI in dev environment.        | Authenticates requests to Azure OpenAI.          |

**Steps to Add Secrets to `dev` Environment:**

1. **Navigate to `dev` Environment Secrets:**
   - Go to `Settings` > `Environments` in your repository.
   - Click on the `dev` environment.

2. **Add Each Secret:**
   - Click on `Add secret`.
   - Enter the **Name** (e.g., `AZURE_CREDENTIALS`).
   - Enter the **Value** corresponding to the secret.
   - Click `Add secret`.
   - Repeat for each required secret listed above.

#### 2. Secrets for `prod` Environment

These secrets are specific to the `prod` environment and are used by workflows that deploy to production resources.

| Secret Name         | Description                                         | Usage                                             |
| ------------------- | --------------------------------------------------- | ------------------------------------------------- |
| `AZURE_CREDENTIALS` | Azure service principal credentials in JSON format. | Authenticates GitHub Actions with Azure for prod. |
| `AZURE_OPENAI_KEY`  | API key for Azure OpenAI in prod environment.        | Authenticates requests to Azure OpenAI.           |

**Steps to Add Secrets to `prod` Environment:**

1. **Navigate to `prod` Environment Secrets:**
   - Go to `Settings` > `Environments` in your repository.
   - Click on the `prod` environment.

2. **Add Each Secret:**
   - Click on `Add secret`.
   - Enter the **Name** (e.g., `AZURE_CREDENTIALS`).
   - Enter the **Value** corresponding to the secret.
   - Click `Add secret`.
   - Repeat for each required secret listed above.

### Setting Up `AZURE_CREDENTIALS`

The `AZURE_CREDENTIALS` secret should contain a JSON object with your Azure service principal credentials. This must be done separately for each environment (`dev` and `prod`) to ensure that each environment uses its own credentials.

1. **Create a Service Principal for `dev`:**
   ```bash
   az ad sp create-for-rbac --name "sp-github-actions-dev" --role owner --scopes /subscriptions/{subscription-id} --sdk-auth
   ```
   - Replace `{subscription-id}` with your Azure subscription ID for the dev environment.

2. **Copy the Output:**
   - The command outputs a JSON object. Copy this entire JSON.

3. **Add to GitHub Secrets for `dev`:**
   - In GitHub, navigate to the `dev` environment secrets.
   - Set the `AZURE_CREDENTIALS` secret with the copied JSON.

4. **Create a Service Principal for `prod`:**
   ```bash
   az ad sp create-for-rbac --name "sp-github-actions-prod" --role owner --scopes /subscriptions/{subscription-id} --sdk-auth
   ```
   - Replace `{subscription-id}` with your Azure subscription ID for the prod environment.

5. **Copy the Output:**
   - The command outputs a JSON object. Copy this entire JSON.

6. **Add to GitHub Secrets for `prod`:**
   - In GitHub, navigate to the `prod` environment secrets.
   - Set the `AZURE_CREDENTIALS` secret with the copied JSON.

### Setting Up `AZURE_OPENAI_KEY`

The `AZURE_OPENAI_KEY` is required for authenticating requests to Azure OpenAI services.

1. **Obtain the API Key:**
   - Log in to your Azure portal.
   - Navigate to the Azure OpenAI service instance.
   - Locate and copy the API key.

2. **Add to GitHub Secrets:**
   - In GitHub, navigate to the respective environment secrets (`dev` or `prod`).
   - Click on `Add secret`.
   - Enter the **Name** (`AZURE_OPENAI_KEY`).
   - Paste the **Value** (your Azure OpenAI API key).
   - Click `Add secret`.

---

## Environment Variables Configuration

In addition to secrets, the workflows require specific environment variables for each environment. These variables are used to initialize the Azure Dev CLI (`azd`) with the appropriate settings and configure other workflow-specific parameters.

### Adding Environment-Specific Variables

Environment variables should be defined within each environment (`dev` and `prod`) to ensure that each environment uses its own configuration values.

#### 1. Variables for `dev` Environment

These variables are specific to the `dev` environment and are used by workflows that deploy to development resources.

| Variable Name           | Description                                      | Usage                                |
| ----------------------- | ------------------------------------------------ | ------------------------------------ |
| `AZURE_ENV_NAME`        | The name of the Azure Dev environment.           | Used in `azd init` command.         |
| `AZURE_LOCATION`        | The Azure region/location for resources.         | Used in `azd init` command.         |
| `AZURE_SUBSCRIPTION_ID` | The Azure subscription ID.                       | Used in `azd init` command.         |
| `AZURE_OPENAI_ENDPOINT` | Endpoint URL for Azure OpenAI in dev environment.| Used in the `pr-pipeline.yml` workflow. |
| `AZURE_OPENAI_MODEL`    | Azure OpenAI model name for dev environment.     | Specifies the OpenAI model in workflows. |
| `AZURE_OPENAI_EMBEDDING_NAME` | Embedding model name for Azure OpenAI in dev. | Specifies the embedding model in workflows. |

**Steps to Add Variables to `dev` Environment:**

1. **Navigate to `dev` Environment Variables:**
   - Go to `Settings` > `Environments` in your repository.
   - Click on the `dev` environment.

2. **Add Each Variable:**
   - Click on `Add variable`.
   - Enter the **Name** (e.g., `AZURE_ENV_NAME`).
   - Enter the **Value** corresponding to the variable.
   - Click `Add variable`.
   - Repeat for each required variable listed above.

#### 2. Variables for `prod` Environment

These variables are specific to the `prod` environment and are used by workflows that deploy to production resources.

| Variable Name           | Description                                      | Usage                                |
| ----------------------- | ------------------------------------------------ | ------------------------------------ |
| `AZURE_ENV_NAME`        | The name of the Azure Dev environment.           | Used in `azd init` command.         |
| `AZURE_LOCATION`        | The Azure region/location for resources.         | Used in `azd init` command.         |
| `AZURE_SUBSCRIPTION_ID` | The Azure subscription ID.                       | Used in `azd init` command.         |
| `AZURE_OPENAI_ENDPOINT` | Endpoint URL for Azure OpenAI in prod environment.| Used in the `pr-pipeline.yml` workflow. |
| `AZURE_OPENAI_MODEL`    | Azure OpenAI model name for prod environment.     | Specifies the OpenAI model in workflows. |
| `AZURE_OPENAI_EMBEDDING_NAME` | Embedding model name for Azure OpenAI in prod. | Specifies the embedding model in workflows. |

**Steps to Add Variables to `prod` Environment:**

1. **Navigate to `prod` Environment Variables:**
   - Go to `Settings` > `Environments` in your repository.
   - Click on the `prod` environment.

2. **Add Each Variable:**
   - Click on `Add variable`.
   - Enter the **Name** (e.g., `AZURE_ENV_NAME`).
   - Enter the **Value** corresponding to the variable.
   - Click `Add variable`.
   - Repeat for each required variable listed above.

### Example Usage in Workflows

In your workflow files (`cd-pipeline-dev.yml` and `cd-pipeline-prd.yml`), you can utilize these environment variables as follows:

```yaml
- name: Initialize Azure Dev Environment
  run: azd init -e ${{ env.AZURE_ENV_NAME }} -l ${{ env.AZURE_LOCATION }} -s ${{ env.AZURE_SUBSCRIPTION_ID }}
```

This command initializes the Azure Dev environment using the specified environment variables.

> **Note:** Ensure that the environment variables are correctly defined in each respective environment (`dev` and `prod`) to avoid configuration issues during workflow execution.

---

## Workflow Files Overview

Your repository includes three GitHub Actions workflows. Ensure these files are placed in the `.github/workflows` directory of your repository.

### 1. Deploy to Development (`cd-pipeline-dev.yml`)

- **File Path:** `.github/workflows/cd-pipeline-dev.yml`
- **Trigger:** Push to the `develop` branch.
- **Jobs:**
  - **provision:**
    - Provisions Azure resources in the `dev` environment using `azd provision`.
    - **Steps:**
      1. **Checkout repository**
         ```yaml
         uses: actions/checkout@v3
         ```
      2. **Log in to Azure**
         ```yaml
         uses: azure/login@v1
         with:
           creds: ${{ secrets.AZURE_CREDENTIALS }}
         ```
      3. **Install Azure Dev CLI**
         ```yaml
         uses: Azure/setup-azd@v1.0.0
         with:
           version: latest
         ```
      4. **Initialize Azure Dev Environment**
         ```yaml
         run: azd init -e ${{ env.AZURE_ENV_NAME }} -l ${{ env.AZURE_LOCATION }} -s ${{ env.AZURE_SUBSCRIPTION_ID }}
         ```
      5. **Provision Azure Resources**
         ```yaml
         run: azd provision
         ```

  - **deploy:**
    - Deploys the application to the `dev` environment using `azd deploy`.
    - **Steps:**
      1. **Checkout repository**
         ```yaml
         uses: actions/checkout@v3
         ```
      2. **Log in to Azure**
         ```yaml
         uses: azure/login@v1
         with:
           creds: ${{ secrets.AZURE_CREDENTIALS }}
         ```
      3. **Install Azure Dev CLI**
         ```yaml
         uses: Azure/setup-azd@v1.0.0
         with:
           version: latest
         ```
      4. **Initialize Azure Dev Environment**
         ```yaml
         run: azd init -e ${{ env.AZURE_ENV_NAME }} -l ${{ env.AZURE_LOCATION }} -s ${{ env.AZURE_SUBSCRIPTION_ID }}
         ```
      5. **Deploy Application**
         ```yaml
         run: azd deploy
         ```

### 2. Deploy to Production (`cd-pipeline-prd.yml`)

- **File Path:** `.github/workflows/cd-pipeline-prd.yml`
- **Trigger:** Push to the `main` branch.
- **Jobs:**
  - **provision:**
    - Provisions Azure resources in the `prod` environment using `azd provision`.
    - **Steps:**
      1. **Checkout repository**
         ```yaml
         uses: actions/checkout@v3
         ```
      2. **Log in to Azure**
         ```yaml
         uses: azure/login@v1
         with:
           creds: ${{ secrets.AZURE_CREDENTIALS }}
         ```
      3. **Install Azure Dev CLI**
         ```yaml
         uses: Azure/setup-azd@v1.0.0
         with:
           version: latest
         ```
      4. **Initialize Azure Dev Environment**
         ```yaml
         run: azd init -e ${{ env.AZURE_ENV_NAME }} -l ${{ env.AZURE_LOCATION }} -s ${{ env.AZURE_SUBSCRIPTION_ID }}
         ```
      5. **Provision Azure Resources**
         ```yaml
         run: azd provision
         ```

  - **deploy:**
    - Deploys the application to the `prod` environment using `azd deploy`.
    - **Steps:**
      1. **Checkout repository**
         ```yaml
         uses: actions/checkout@v3
         ```
      2. **Log in to Azure**
         ```yaml
         uses: azure/login@v1
         with:
           creds: ${{ secrets.AZURE_CREDENTIALS }}
         ```
      3. **Install Azure Dev CLI**
         ```yaml
         uses: Azure/setup-azd@v1.0.0
         with:
           version: latest
         ```
      4. **Initialize Azure Dev Environment**
         ```yaml
         run: azd init -e ${{ env.AZURE_ENV_NAME }} -l ${{ env.AZURE_LOCATION }} -s ${{ env.AZURE_SUBSCRIPTION_ID }}
         ```
      5. **Deploy Application**
         ```yaml
         run: azd deploy
         ```

### 3. Pull Request Pipeline (`pr-pipeline.yml`)

- **File Path:** `.github/workflows/pr-pipeline.yml`
- **Trigger:** Pull requests targeting the `develop` branch.
- **Permissions:** 
  - `contents: read`
- **Jobs:**
  - **backend:**
    - **Runs on:** `ubuntu-latest`
    - **Environment:** `dev`
    - **Steps:**
      1. **Checkout repository**
         ```yaml
         uses: actions/checkout@v3
         ```
      2. **Set up Python 3.11**
         ```yaml
         uses: actions/setup-python@v3
         with:
           python-version: "3.11"
         ```
      3. **Install dependencies**
         ```yaml
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements-dev.txt
         ```
      4. **Test with pytest**
         ```yaml
         env:
           AZURE_OPENAI_ENDPOINT: ${{ env.AZURE_OPENAI_ENDPOINT }}
           AZURE_OPENAI_MODEL: ${{ env.AZURE_OPENAI_MODEL }}
           AZURE_OPENAI_EMBEDDING_NAME: ${{ env.AZURE_OPENAI_EMBEDDING_NAME }}
         run: |
           export PYTHONPATH=$(pwd)
           coverage run -m pytest -v --show-capture=stdout
           coverage report -m --include=app.py,backend/*,tests/*
           coverage xml
         ```
      5. **Code Coverage Report**
         ```yaml
         uses: irongut/CodeCoverageSummary@v1.3.0
         with:
           filename: coverage.xml
           badge: true
           fail_below_min: true
           format: markdown
           hide_branch_rate: false
           hide_complexity: true
           indicators: true
           output: both
           thresholds: '50 80'
         ```

  - **frontend:**
    - **Runs on:** `ubuntu-latest`
    - **Environment:** `dev`
    - **Defaults:**
      - **Run:** 
        ```yaml
        working-directory: frontend
        ```
    - **Strategy:**
      - **Matrix:**
        ```yaml
        node-version: [14.x, 16.x, 18.x, 21.x]
        ```
        *See supported Node.js release schedule at https://nodejs.org/en/about/releases/*
    - **Steps:**
      1. **Checkout repository**
         ```yaml
         uses: actions/checkout@v3
         ```
      2. **Use Node.js ${{ matrix.node-version }}**
         ```yaml
         uses: actions/setup-node@v3
         with:
           node-version: ${{ matrix.node-version }}
           cache: 'npm'
           cache-dependency-path: '**/package-lock.json'
         ```
      3. **Install dependencies**
         ```yaml
         run: npm ci
         ```
      4. **Build frontend application**
         ```yaml
         run: NODE_OPTIONS=--max_old_space_size=8192 npm run build --if-present
         ```
      5. **Run frontend tests if present**
         ```yaml
         run: npm run test --if-present
         ```

---

## Additional Configurations

### Permissions

Ensure that your GitHub Actions have the necessary permissions to perform their tasks.

- The `pr-pipeline.yml` workflow has restricted permissions (`contents: read`). Modify this if additional permissions are required for other workflows.

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

### Azure Dev CLI (`azd`) Configuration

The workflows utilize the Azure Dev CLI (`azd`). Ensure that:

- Your Azure resources are properly configured to work with `azd`.
- The service principal used has the necessary permissions to provision and deploy resources.

### Node.js Versions for Frontend

The `frontend` job in `pr-pipeline.yml` tests against multiple Node.js versions (14.x, 16.x, 18.x, 21.x). Ensure your frontend application supports these versions or adjust the matrix accordingly.

---

## Conclusion

By following the steps outlined in this guide, your GitHub repository will be properly configured to support the provided CI/CD workflows. This setup ensures automated provisioning and deployment of your application to both development and production environments, as well as running comprehensive tests on pull requests to maintain code quality.

For any further assistance or advanced configurations, refer to the [GitHub Actions Documentation](https://docs.github.com/en/actions) and the [Azure Dev CLI Documentation](https://learn.microsoft.com/en-us/azure/developer/azure-devs-cli/).