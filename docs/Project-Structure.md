# Project Structure: equilibrium-sql-agent

```
equilibrium-sql-agent/
├── docs
│   ├── Project-Structure.md
│   └── Project-Summary.md
├── esma/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── baseReAct.py             # Base ReACt agent class for shared functionality
│   │   └── esma.py                  # ESMA class to initialize agents based on user input
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── app.py                   # FastAPI app with endpoints
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Environment variables, API keys, connection configs
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── prompt_loader.py         # Loader class
│   │   ├── general_system.md
│   │   ├── enaho_tables.md
│   │   └── geih_tables.md
│   ├── memory/
│   │   ├── __init__.py
│   │   └── state_models.py          # Pydantic models for graph states and memory
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── column_retriever.py
│   │   ├── schema_gatherer.py
│   │   ├── schema_validator.py
│   │   ├── sql_executor.py
│   │   └── table_descriptions_retriever.py
│   └── utils/
│       ├── __init__.py
│       └── bigquery_client.py
└── scripts/
│   ├── bigquery_setup
│   │   └── data_upload_pipeline.py
│   ├── data_preprocessing
│   ├── documentation_preparation
│   │   └── parse_documentation.py
│   ├── knowledge_base
│   │   └── build_knowledge_base.py
│   └── notebooks
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_bigquery_client.py
│   ├── test_column_retriever.py
│   ├── test_schema_validator.py
│   └── test_sql_executor.py
├── langgraph.json
├── pyproject.toml
└── README.md
```
