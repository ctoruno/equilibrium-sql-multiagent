"""
Tests for Column retriever Tool.
Run with pytest: uv run pytest test/test_column_retriever.py
Or manually: uv run test/test_column_retriever.py
"""

from esma.tools.column_retriever import ColumnRetriever

def test_column_retriever():
    """Test ColumnRetriever with various queries."""
    retriever = ColumnRetriever()
    
    query1 = "cuántas casas cuentas con licencia de construcción?"
    print(f"Testing query: {query1}")
    result1 = retriever._run(
        query=query1,
        database="enaho", 
        selected_tables=["ENAHO01-2024-100"]
    )
    assert isinstance(result1, str)
    assert len(result1) > 0
    print(f"ENAHO result: {result1}")

    query2 = "cuántas personas obtuvieron su empleo a través de internet?"
    print(f"Testing query: {query2}")
    result2 = retriever._run(
        query=query2,
        database="geih",
        selected_tables=["DBF_GECH_6_67"]
    )
    assert isinstance(result2, str)
    assert len(result2) > 0
    print(f"GEIH result: {result2}")
    
    print("Testing with invalid database...")
    result3 = retriever._run(
        query="invalid test",
        database="invalid_db",
        selected_tables=["some_table"]
    )
    assert isinstance(result3, str)
    print(f"Invalid DB result: {result3}")

def test_empty_query():
    """Test with empty query."""
    retriever = ColumnRetriever()
    result = retriever._run(query="", database="enaho", selected_tables=[])
    assert isinstance(result, str)
    print(f"Empty query result: {result}")