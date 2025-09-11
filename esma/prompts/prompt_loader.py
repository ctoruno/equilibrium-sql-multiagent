from pathlib import Path

class PromptLoader:
    """Simple loader for markdown prompt templates"""
    
    def __init__(self, database: str):
        self.templates_dir = Path(__file__).parent
        if not database:
            raise ValueError("Database parameter cannot be empty")
        else:
            self.database = database
    
    def load_system_prompt(self) -> str:
        """
        Load system prompt for specified database
        
        Args:
            database: Database name (e.g., 'enaho-2024', 'geih-2024')
            
        Returns:
            Content of the markdown file as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            ValueError: If database parameter is invalid
        """
        
        template_file = self.templates_dir / f"{self.database}_system.md"
        
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        return template_file.read_text(encoding="utf-8")