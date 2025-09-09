"""
Tests for BigQuery client
"""
import logging

from esma.config.settings import settings
from esma.utils.bigquery_client import BigQueryClient

logging.basicConfig(level=logging.INFO)

def manual_test(database_name: str):

    print(f"\n=== Manual Test for BigQueryClient ({database_name}) ===")

    try: 
        # Test 1: Connection establishment
        print("\n1. Testing connection establishment...")
        client = BigQueryClient.get_client(database_name)
        db = client.db
        print("✅ Connection established successfully")

        # Test 2: Simple query execution
        print("\n2. Testing simple query execution...")
        tables = db.get_usable_table_names()
        print(f"Available tables: {tables[:3]}..." if len(tables) > 3 else f"Available tables: {tables}")

        if tables:
            table_name = tables[0]
            sql = f"SELECT * FROM `{client.dataset_id}.{table_name}` LIMIT 5"
            result = client.execute_query(sql)
            print(f"✅ Query executed on table '{table_name}'")
            print(f"Result preview: {result[:200]}...")
        else:
            print("❌ No tables available for query test")

        # Test 3: Table info retrieval
        print("\n3. Testing table info retrieval...")
        if tables:
            test_tables = tables[:2]  # Test with first 2 tables
            table_info = client.get_table_info(test_tables)
            print(f"✅ Retrieved info for tables: {test_tables}")
            print(f"Info preview: {table_info[:300]}...")
        else:
            print("❌ No tables available for info retrieval test")
        
        # Test 4: Table validation
        print("\n4. Testing table validation...")
        if tables:
            test_tables = tables[:2] + ["nonexistent_table_12345"]
            validation_result = client.validate_tables_exist(test_tables)
            print("✅ Table validation completed")
            print(f"Results: {validation_result}")
        else:
            print("❌ No tables available for validation test")

        print("🎉 All manual tests completed successfully!")
        print("\n" + "=" * 60)
    
    except Exception as e:
        print(f"\n❌ Manual test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    manual_test("enaho")
    manual_test("geih")