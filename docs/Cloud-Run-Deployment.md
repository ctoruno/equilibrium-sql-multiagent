# Deployment Instructions for Google Cloud Run

1. Install Google Cloud SDK
    - Follow instructions at https://cloud.google.com/sdk/docs/install

2. Set up Google CLI
    - Initialize the SDK: 
        ```bash
        gcloud init
        ```

3. Google Secret Manager
    - Enable API
    - Create and store secrets

4. Google Artifact Registry
    - Enable API
    - Create a Docker repository
    - Verify that repository is created:
        ```bash
        gcloud artifacts repositories list
        ```

5. Google Cloud Build API
    - Enable API
    - Connect to GitHub repository
    - Add a cloudbuild.yaml file to the root of your repository
    - Create a trigger for the main branch

