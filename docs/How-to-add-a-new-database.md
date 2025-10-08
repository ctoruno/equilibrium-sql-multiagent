# How to add a new database?

### 1. Google Cloud Storage as Data Lake

1. Create a new Google Cloud Storage Bucket. 

    - Follow the naming convention: `sql-multiagent-<DATABASE>-<YEAR>`.
    - Single Region or Multi-Region. Currently using US-EAST1 for other services.
    - Standard storage
    - **Important**: Enable hierarchical namespaces
    - Use default delete policy

2. Create three subfolders in bucket: `data`, `dictionaries`, `metadata`

3. Upload survey data files to the `sql-multiagent-<DATABASE>-<YEAR>/data`

    - Data files in CSV are preferred, but STATA files would also be ok. Any other format, would require additional edits to the current code.
    - Data file names should be in upper caps and no spaces or special characters (ñ/Ñ)
    - It's ok if column names have special characters like ñ/Ñ

4. Upload data dictionaries to the `sql-multiagent-<DATABASE>-<YEAR>/dictionaries`

    - Dictionary files in PDF or Markdown are preferred. Any other format, would require additional edits to the current code.
    - Dictionary file names should match their correspondent data file in CSV.
    - Dictionaries can be in excel or word format, it is suggested to transform them into PDF.
    - If a single dictionary file is serving multiple data files (CSV), it is suggested to split it and upload one dictionary per data file.

### 2. BigQuery Data Server

1. Create BigQuery Dataset

- Dataset name should be <DATABASE_YEAR>. Do NOT use '-' in name
- Region or Multiregion. Other datasets use 'US-EAST1'

2. Populate dataset

- Use the `scripts/bigquery_setup/data_upload_pipeline.py` script to populate dataset using the data files in GCS
- Add the database information to the `AVAILABLE_DATABASES` and the `self.survey` init inside the script

    ```bash
    uv run scripts/bigquery_setup/data_upload_pipeline.py --survey DATABASE-YEAR
    ```

### 3. Data Dictionaries

1. Parse data dictionaries as JSON files

    Data dictionaries from household surveys usually come as PDF or Excel files. For the chatbot system to be able to search and retrieve information on the variables needed to answer a query, the data will be uploaded to a vector database for Retrieval Augmented Generation (RAG). For this, we need the data dictionaries to be saved as JSON files with the following structure:

    ```json
    "tables": {
        "ENAHO01-2024-100": {   # Make sure the table name matches the CSV file name
            "metadata": {
                "description": "Características de la Vivienda y del Hogar (Módulo 100)",
                "file_name": "ENAHO01-2024-100",
                "business_domain": [
                    "housing",
                    "demographics",
                    "geographic",
                    "utilities",
                    "expenditures",
                    "water_sanitation",
                    "telecommunications"
                ],
                "record_level": "household",
                "module_number": "100"
            },
            "columns": {
                "MES": {
                    "description": "Mes de Ejecución de la Encuesta",
                    "data_type": "CHARACTER",
                    "size": 2,
                    "decimals": 0,
                    "business_meaning": "Survey execution month"
                },
                "NCONGLOME": {
                    "description": "Número de Conglomerado (proveniente del marco)",
                    "data_type": "CHARACTER",
                    "size": 6,
                    "decimals": 0,
                    "business_meaning": "Frame cluster identifier"
                },
                "PERIODO": {
                    "description": "Periodo de ejecución de la Encuesta",
                    "data_type": "NUMERIC",
                    "size": 1,
                    "decimals": 0,
                    "valid_values": {
                        "1": "Primer Período",
                        "2": "Segundo Período",
                        "3": "Tercer Período",
                        "4": "Cuarto Período",
                        "5": "Quinto Período"
                    },
                    "range": "1-5",
                    "business_meaning": "Survey execution period"
                }
            }
        }
    }
    ```

    This step does not need to be manual. LLMs are great tools to read and parse information. You can adapt the `scripts/documentation_preparation/parse_documentation.py` python file to parse documentation into this specific JSON format.

2. Vectorize data dictionaries

- Use the `scripts/vertexai-vector-search/generate_embeddings.py` script to create a JSONL file with the vectorize dictionaries
- Add the database information to the `AVAILABLE_DATABASES` and `DATABASES` objects inside the script
- Run the script with the database argument

    ```bash
    uv run scripts/vertexai-vector-search/populate-columns.py --database DATABASE-YEAR
    ```

3. Update the VertexAI Vector Search Index

- Use the `scripts/vertexai-vector-search/manage_indexes.py` script to update a VertexAI Vector Search Index
- Run the script with the `--type columns` and `--update` arguments to update the index for the data dictionaries

    ```bash
    uv run scripts/vertexai-vector-search/manage_indexes.py --type columns --update
    ```

### 4. Update Settings & Pydantic Models

1. Update `esma/config/settings.py`
    - BigQuery dataset IDs 

2. Update the pydantic models for all tools
    All tools in `esma/tools/` have a `Input(BaseModel)` pydantic model with the following field: `database: Literal["...", "..."]`. If not updated, Chat models won't be able to call the tools for the specific database.

### 5. Update Prompts

1. Update the system general prompt in: `esma/prompts/general_system.md` to include the following:
    - A DATABASE CONTEXT
    - A note on the use of Expansion Factors

2. Create a tables description file in: `esma/prompts/` named `<DATABASE>_tables.md`. This file should contain a brief description of each table in the database, including its name, record level, and business domain. See other examples within the folder.

### 6. Test the agent locally using Langgraph Studio

1. Comment out the following line in `esma/agents/baseReAct.py`:

    ```python
    checkpointer=self.checkpointer
    ```

    >!!!REMEMBER TO UNCOMMENT THIS LINE BEFORE DEPLOYING TO CLOUD RUN!!!

2. Activate the virtual environment:

    ```bash
    # In MacOS
    source .venv/bin/activate

    # In Windows
    .venv/Scripts/activate
    ```

3. Run LangGraph Studio:

    ```bash
    langgraph dev
    ```

### 7. Commit and push changes to GitHub

1. Commit & Push from GitHub Desktop or use git CLI:

    ```bash
    git add .
    git commit -m "Add DATABASE-YEAR"
    git push origin main
    ```

2. This should trigger GitHub Actions to build and push a new Docker image to Google Container Registry. This trigger routine is defined in `cloudbuild.yaml`.

### 8. Deploy to Google Cloud Run

- Go to Google Cloud Console > Cloud Run
- Select the service `esma-agent`
- Click on "Edit & Deploy New Revision"
- In the container section, select the latest container image URL from Google Container Registry
- Click on "Deploy"