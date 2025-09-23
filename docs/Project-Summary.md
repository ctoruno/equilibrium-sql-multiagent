# Equilibrium SQL Agent (ESMA)

## Project Overview
AI-powered chatbot system that answers complex user questions by querying two household survey databases: **ENAHO** (Peru) and **GEIH** (Colombia). The system uses a single ReAct agent to understand natural language queries and generate appropriate SQL queries for either database.

## Technical Stack
- **Databases**: Google BigQuery (separate datasets for each survey)
- **AI Framework**: LangChain + LangGraph for agent orchestration
- **LLMs**: Gemini 2.5 Pro (primary), configurable for OpenAI GPT models
- **Embeddings**: VoyageAI (voyage-3.5 model)
- **Vector Database**: Pinecone with separate indexes per database
- **API Framework**: FastAPI with streaming and non-streaming endpoints
- **Architecture**: Single ReAct agent with specialized tools

## Current Architecture

### ReAct Agent Flow
```
User Query → ESMA ReAct Agent → Tool Selection Loop → Response Generation
                    ↓
    [Table Description Retriever]
    [Column Retriever (Vector DB)]
    [Schema Gatherer]
    [Schema Validator] 
    [SQL Executor]
```

### Key Components
- **Single Universal Agent**: One ReAct agent handles both ENAHO and GEIH databases
- **Database Selection**: Agent determines target database from user context (Peru/Colombia keywords)
- **Tool-Based Workflow**: 5 specialized tools for different aspects of SQL generation
- **Memory Management**: Automatic conversation summarization when token limits are approached
- **Thread Persistence**: Conversation continuity through configurable thread IDs

## Database Complexity
- **ENAHO Database**: 11 tables, ~440-660 total columns (Peruvian household survey)
- **GEIH Database**: 8 tables, ~320-480 total columns (Colombian household survey)
- **Challenge**: Cannot load all 800-1200+ columns into LLM context efficiently

## Knowledge Base Architecture

### Pinecone Indexes
- **enaho-2024** index with `enaho-2024-columns` namespace
- **geih-2024** index with `geih-2024-columns` namespace

### Vector Record Structure
```json
{
    "id": "ENAHO01-2024-100_P101",
    "values": [...],  
    "metadata": {
        "table_id": "ENAHO01-2024-100",
        "column_name": "P101", 
        "description": "Tipo de vivienda",
        "data_type": "NUMERIC",
        "business_meaning": "Housing type classification",
        "valid_values": {
            "1": "Casa independiente",
            "2": "Departamento en edificio"
        }
    }
}
```

## Tool System

### 1. Table Description Retriever
- Loads markdown documentation for available tables
- Provides business context for table selection
- Returns available tables in BigQuery vs. documented tables

### 2. Column Retriever  
- Vector similarity search for relevant columns
- Filtered by selected tables
- Returns column metadata including valid values and business meaning

### 3. Schema Gatherer
- Retrieves actual BigQuery schema information
- Provides sample data for understanding value formats
- Validates table existence

### 4. Schema Validator
- Validates SQL queries against BigQuery schema
- Prevents dangerous operations (INSERT, DELETE, etc.)
- Checks table and column existence

### 5. SQL Executor
- Executes validated queries against BigQuery
- Applies result limits automatically
- Provides structured error handling

## API Layer (FastAPI)

### Endpoints
- `POST /chat` - Non-streaming chat with JSON response
- `POST /chat/stream` - Server-sent events streaming
- `POST /thread/new` - Create new conversation thread
- `GET /` - API documentation

### Features
- **Thread Management**: Persistent conversations with unique thread IDs
- **Streaming Support**: Real-time response streaming for better UX
- **Error Handling**: Structured error responses with details
- **CORS Ready**: Configurable for frontend integration

## Memory & Token Management

### Conversation Summarization
- Automatic summarization when token threshold exceeded (configurable)
- Preserves key information: queries, operations, findings, errors
- Maintains conversation context while respecting LLM limits
- Uses separate summarizer LLM for efficiency

### Message Management
- Keeps recent messages in active context
- Removes old messages after summarization
- Maintains system prompt and conversation flow

## 🔧 Current Limitations
- **Single Universal User**: No individual user authentication
- **Restricted Access**: Prototype-level access control
- **No Caching**: Direct BigQuery queries without caching layer
- **Limited Documentation Search**: Only column-level vector search implemented

## Configuration Management
- Environment-based configuration using Pydantic Settings
- Configurable LLM models, token limits, similarity thresholds
- Separate dataset IDs for each database
- API key management for all external services

## Query Workflow Example
1. User asks about unemployment rates in Colombia
2. Agent identifies GEIH database from context
3. Retrieves table descriptions to select relevant tables
4. Uses vector search to find employment-related columns
5. Generates and validates SQL query
6. Executes query and formats results
7. Provides interpretation with statistical context

## Future Enhancement Opportunities
- **User Authentication**: Individual accounts and personalized history
- **Query Caching**: Redis/similar for performance optimization  
- **Documentation Search**: Full methodology document vector search
- **Cross-Database Queries**: Advanced analysis combining both surveys
- **Export Capabilities**: CSV/Excel download of query results
- **Query Templates**: Pre-built queries for common analyses