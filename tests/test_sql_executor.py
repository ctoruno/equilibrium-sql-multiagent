"""
Simple test suite for SQLExecutor tool - runs actual queries against BigQuery
"""

import json
from esma.tools.sql_executor import SQLExecutor


def test_enaho_query_execution():
    """Test executing a simple query on ENAHO database"""
    executor = SQLExecutor()
    
    result = executor._run(
        sql_query="SELECT CONGLOME, P301A, P301B FROM Enaho01A-2024-300 LIMIT 5",
        database="enaho"
    )
    
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["success"] is True
    assert result_dict["error"] is None
    assert result_dict["results"] is not None
    assert result_dict["database"] == "enaho"


def test_geih_query_execution():
    """Test executing a simple query on GEIH database"""
    executor = SQLExecutor()
    
    result = executor._run(
        sql_query="SELECT DIRECTORIO, HOGAR, ORDEN, P2061, P1906S4 FROM DBF_GECH_6_234 LIMIT 5",
        database="geih"
    )
    
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["success"] is True
    assert result_dict["error"] is None
    assert result_dict["results"] is not None
    assert result_dict["database"] == "geih"


def test_empty_query():
    """Test that empty queries are handled properly"""
    executor = SQLExecutor()
    
    result = executor._run(
        sql_query="",
        database="enaho"
    )
    
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["success"] is False
    assert "SQL query cannot be empty" in result_dict["error"]