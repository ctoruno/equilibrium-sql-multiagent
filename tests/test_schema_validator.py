"""
Tests for SchemaValidator tool
"""

import json
from esma.tools.schema_validator import SchemaValidator

def test_forbidden_operations_insert():
    """Test that INSERT operations are blocked"""
    validator = SchemaValidator()
    result = validator._run(
        sql_query="INSERT INTO table1 VALUES (1, 'test')",
        database="enaho"
    )
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["valid"] is False
    assert "Forbidden operation: INSERT" in result_dict["errors"][0]
    

def test_forbidden_operations_delete():
    """Test that DELETE operations are blocked"""
    validator = SchemaValidator()
    result = validator._run(
        sql_query="DELETE FROM table1 WHERE id = 1",
        database="enaho"
    )
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["valid"] is False
    assert "Forbidden operation: DELETE" in result_dict["errors"][0]
    

def test_forbidden_operations_drop():
    """Test that DROP operations are blocked"""
    validator = SchemaValidator()
    result = validator._run(
        sql_query="DROP TABLE table1",
        database="enaho"
    )
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["valid"] is False
    assert "Forbidden operation: DROP" in result_dict["errors"][0]

    
def test_valid_select_query():
   """Test validation of a valid SELECT query - requires real database connection"""
   validator = SchemaValidator()
   
   result = validator._run(
       sql_query="SELECT P101, P102 FROM Enaho01-2024-100 WHERE P101 = 1 LIMIT 10",
       database="enaho"
   )
   result_dict = json.loads(result)
   print(result_dict)
   
   assert result_dict["valid"] is True
   assert result_dict["errors"] == []
   assert "Enaho01-2024-100" in result_dict["tables_checked"]

    
def test_invalid_table():
    """Test validation with non-existent table"""
    validator = SchemaValidator()
    
    result = validator._run(
        sql_query="SELECT * FROM INVALID_TABLE",
        database="enaho"
    )
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["valid"] is False
    assert "Tables not found:" in result_dict["errors"][0]
    

def test_invalid_column():
    """Test validation with non-existent column"""
    validator = SchemaValidator()
    
    result = validator._run(
        sql_query="SELECT invalid_column FROM Enaho01-2024-100",
        database="enaho"
    )
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["valid"] is False
    assert "Column validation failed" in result_dict["errors"][0]


def test_syntax_error():
    """Test validation with SQL syntax error"""
    validator = SchemaValidator()
    
    result = validator._run(
        sql_query="SELECT * FORMU Enaho01-2024-100",
        database="enaho"
    )
    result_dict = json.loads(result)
    print(result_dict)
    
    assert result_dict["valid"] is False
    assert "SQL syntax error" in result_dict["errors"][0]