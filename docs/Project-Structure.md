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
│   │   ├── base.py                  # Base agent class for shared functionality (linear flow)
│   │   ├── baseReAct.py             # Base ReACt agent class for shared functionality
│   │   ├── enaho_ReAct.py           # ENAHO specialist ReAct agent
│   │   ├── enaho.py                 # ENAHO specialist agent (linear flow)
│   │   ├── geih_ReAct.py            # GEIH specialist ReAct agent
│   │   ├── geih.py                  # GEIH specialist agent (linear flow)
│   │   └── router.py                # Router agent logic
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Environment variables, API keys, connection configs
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── prompt_loader.py         # Loader class
│   │   ├── enaho_system.md
│   │   ├── enaho_tables.md
│   │   ├── geih_system.md
│   │   └── geih_tables.md
│   ├── memory/
│   │   ├── __init__.py
│   │   └── state_models.py          # Pydantic models for graph states (linear flow)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── column_retriever.py
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
│       ├── testing-gcs.ipynb
│       ├── testing-gemini.ipynb
│       ├── testing-sql-tools.ipynb
│       └── testing.ipynb
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
