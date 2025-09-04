# Project Structure: equilibrium-sql-agent

```
equilibrium-sql-agent/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
│
├── esma/
│   └── equilibrium_sql_agent/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       │
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── enaho_parser.py      # PDF parser for ENAHO
│       │   └── geih_parser.py       # Excel parser for GEIH
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── schema.py            # Pydantic models for schema representation
│       │   └── database.py          # Database connection models
│       │
│       ├── knowledge_base/
│       │   ├── __init__.py
│       │   ├── builder.py           # Knowledge base creation
│       │   ├── embeddings.py        # Vector embeddings management
│       │   └── retriever.py         # Schema retrieval logic
│       │
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── router.py            # Router agent (ENAHO vs GEIH)
│       │   ├── enaho_agent.py       # ENAHO-specific agent
│       │   └── geih_agent.py        # GEIH-specific agent
│       │
│       ├── database/
│       │   ├── __init__.py
│       │   ├── duckdb_manager.py    # DuckDB/MotherDuck connections
│       │   └── query_executor.py    # SQL execution with validation
│       │
│       └── utils/
│           ├── __init__.py
│           ├── logging.py
│           └── validation.py
│
├── data/
│   ├── raw/                         # Original documentation files
│   │   ├── enaho_documentation.pdf
│   │   └── geih_documentation.xlsx
│   │
│   ├── processed/                   # Parsed schema files
│   │   ├── enaho_schemas.json
│   │   └── geih_schemas.json
│   │
│   └── embeddings/                  # Vector embeddings storage
│       ├── table_embeddings.pkl
│       └── column_embeddings.pkl
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_parsers/
│   ├── test_knowledge_base/
│   └── test_agents/
│
├── notebooks/                       # Jupyter notebooks for exploration
│   ├── 01_explore_documentation.ipynb
│   ├── 02_test_parsers.ipynb
│   └── 03_test_embeddings.ipynb
│
└── scripts/
    ├── parse_documentation.py       # CLI script to parse docs
    ├── build_knowledge_base.py      # CLI script to build embeddings
    └── test_chatbot.py             # Simple test interface
```
