"""
SQL Schema Validator tool for validating queries against BigQuery schema
"""

import re
import json
from typing import List, Dict, Literal

from sqlalchemy import text
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from esma.utils.bigquery_client import BigQueryClient


class SchemaValidatorInput(BaseModel):
    """Input schema for SchemaValidator tool."""
    sql_query: str = Field(description="SQL query to validate")
    database: Literal["enaho", "geih"] = Field(description="Target database")


class SchemaValidator(BaseTool):
    """
    Tool for validating SQL queries against BigQuery schema.
    Checks table existence, column validity, and prevents dangerous operations.
    """
    
    name: str = "schema_validator"
    description: str = """
    Validate a SQL query against the database schema.
    Checks that tables and columns exist, and prevents dangerous operations.
    Returns validation results with specific error details if validation fails.
    """
    args_schema = SchemaValidatorInput
    
    
    def _run(self, sql_query: str, database: str) -> str:
        """
        Execute the schema validation.
        
        Returns:
            JSON string with validation results
        """
        
        operation_check = self._check_forbidden_operations(sql_query)
        if not operation_check["valid"]:
            return self._format_response({
                "valid": False,
                "errors": [operation_check["error"]],
                "warnings": []
            })
        
        client = BigQueryClient.get_client(database)
        
        tables = self._extract_tables(sql_query)
        table_validation = self._validate_tables(tables, client)
        
        errors = []
        warnings = []
        
        invalid_tables = [t for t, exists in table_validation.items() if not exists]
        if invalid_tables:
            errors.append(f"Tables not found: {', '.join(invalid_tables)}")
        
        if not errors:
            structure_validation = self._validate_query_structure(sql_query, client)
            if not structure_validation["valid"]:
                errors.extend(structure_validation.get("errors", []))
                warnings.extend(structure_validation.get("warnings", []))
        
        return self._format_response({
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "tables_checked": list(table_validation.keys()),
            "table_validation": table_validation
        })
    

    def _check_forbidden_operations(self, sql_query: str) -> Dict:
        """Check if query contains forbidden operations."""
        query_upper = sql_query.upper()
        FORBIDDEN_OPERATIONS = [
            "INSERT", "UPDATE", "DELETE", "DROP", 
            "ALTER", "TRUNCATE", "CREATE", "REPLACE"
        ]
        
        for operation in FORBIDDEN_OPERATIONS:
            pattern = r'\b' + operation + r'\b'
            if re.search(pattern, query_upper):
                return {
                    "valid": False,
                    "error": f"Forbidden operation: {operation}. Only SELECT queries are allowed."
                }
        
        return {"valid": True}
    
    
    def _extract_tables(self, sql_query: str) -> List[str]:
        """
        Extract table names from SQL query.
        Simple regex-based extraction for FROM and JOIN clauses.
        """
        tables = []

        from_pattern = r"FROM\s+([a-zA-Z0-9_\-]+)"
        join_pattern = r"JOIN\s+([a-zA-Z0-9_\-]+)"

        from_matches = re.findall(from_pattern, sql_query, re.IGNORECASE)
        join_matches = re.findall(join_pattern, sql_query, re.IGNORECASE)
        all_tables = from_matches + join_matches
        tables = list(set(all_tables))
        
        return tables
    
    
    def _validate_tables(self, table_names: List[str], client: BigQueryClient) -> Dict[str, bool]:
        """Validate that tables exist in the database."""
        if not table_names:
            return {}
        
        return client.validate_tables_exist(table_names)
    

    def _validate_query_structure(self, sql_query: str, client: BigQueryClient) -> Dict:
        """
        Validate the overall query structure using BigQuery's dry run capability.
        This will catch column errors and syntax issues.
        """
        try:
            dry_run_query = f"SELECT * FROM ({sql_query}) AS validation_check LIMIT 0"
            _ = client.db.run(dry_run_query)
        
            return {"valid": True, "errors": [], "warnings": []}
            
        except Exception as e:
            error_msg = str(e)
            
            if any(phrase in error_msg.lower() for phrase in [
                "not found", "does not exist", "unrecognized name", 
                "name not found", "invalid field", "no such field"
            ]):
                return {
                    "valid": False,
                    "errors": [f"Column validation failed: {error_msg}"],
                    "warnings": []
                }
            elif "syntax error" in error_msg.lower():
                return {
                    "valid": False,
                    "errors": [f"SQL syntax error: {error_msg}"],
                    "warnings": []
                }
            else:
                return {
                    "valid": False,
                    "errors": [f"Query validation failed: {error_msg}"],
                    "warnings": []
                }
            
    
    def _format_response(self, response_dict: Dict) -> str:
        """Format response as JSON string for LLM consumption."""
        return json.dumps(response_dict, indent=2)