from esma.tools.column_retriever import ColumnRetriever

def test_column_retriever():
    """Test ColumnRetriever with various queries."""
    retriever = ColumnRetriever()
    
    result1 = retriever._run(
        query="cuántas casas cuentas con licencia de construcción?",
        database="enaho", 
        selected_tables=["ENAHO01-2024-100"]
    )
    assert isinstance(result1, str)
    assert len(result1) > 0
    print(f"ENAHO result: {result1}")
    
    result2 = retriever._run(
        query="cuántas personas obtuvieron su empleo a través de internet?",
        database="geih",
        selected_tables=["DBF_GECH_6_67"]
    )
    assert isinstance(result2, str)
    assert len(result2) > 0
    print(f"GEIH result: {result2}")
    
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

def manual_test():
    """Original test function for manual running."""
    retriever = ColumnRetriever()
    
    test_cases = [
        {
            "query": "cuántas casas cuentan con licencia de construcción?",
            "database": "enaho", 
            "selected_tables": ["ENAHO01-2024-100"]
        },
        {
            "query": "cuántas personas obtuvieron su empleo a través de internet?",
            "database": "geih",
            "selected_tables": ["DBF_GECH_6_67"]
        },
        {
            "query": "invalid test",
            "database": "invalid_db",
            "selected_tables": ["some_table"]
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Query: {test_case['query']}")
        result = retriever._run(**test_case)
        print(f"Result: {result}")

if __name__ == "__main__":
    manual_test()