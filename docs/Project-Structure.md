# Project Structure: equilibrium-sql-agent

```
equilibrium-sql-agent/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── esma/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router.py                # Router agent logic
│   │   ├── enaho.py                 # ENAHO specialist agent
│   │   ├── geih.py                  # GEIH specialist agent
│   │   └── base.py                  # Base agent class for shared functionality
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Environment variables, API keys, BigQuery/Pinecone connection configs
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── prompt_loader.py         # Loader class
│   │   ├── templates/               # Markdown prompt files
│   │   │   ├── router.md            
│   │   │   ├── enaho_system.md      
│   │   │   ├── geih_system.md       
│   │   │   ├── sql_generation.md    # Shared SQL generation template
│   │   │   ├── error_handling.md    # Error recovery prompts
│   │   │   └── clarification.md     # User clarification templates
│   │   └── examples/                # Few-shot examples
│   │   │   ├── enaho_queries.md     
│   │   │   └── geih_queries.md
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── conversation_manager.py  # Main orchestrator
│   │   ├── persistence.py           # BigQuery storage (Long-term Memory Persistance)
│   │   ├── trimmer.py               # Token management & summarization
│   │   └── state_models.py          # Pydantic models for graph states
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── column_retriever.py      # Pinecone vector search for columns
│   │   ├── schema_validator.py      # BigQuery INFORMATION_SCHEMA queries
│   │   └── sql_executor.py          # Execute final SQL
│   └── utils/
│       ├── __init__.py
│       └── bigquery_client.py       # BigQuery connection wrapper
└── scripts/
    ├── bigquery_setup
    │   └── data_upload_pipeline.py
    └── knowledge_base
        └── build_knowledge_base.py
```
