# Deployment Instructions for Google Cloud Run

1. Install Google Cloud SDK
    - Follow instructions at https://cloud.google.com/sdk/docs/install

2. Set up and Initialize Google CLI
    ```bash
    gcloud init
    ```

3. Google Artifact Registry
    - Enable API
    - Create a Docker repository
    - Verify that repository is created:
        ```bash
        gcloud artifacts repositories list
        ```

4. Google Cloud Build API
    - Enable API
    - Connect to GitHub repository
    - Add a cloudbuild.yaml file to the root of your repository
    - Create a trigger for the main branch

5. Google Cloud Run
    - Enable API
    - Create and deploy a new service
    - Set environment variables

