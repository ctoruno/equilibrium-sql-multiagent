from pathlib import Path

class PromptLoader:
    """Simple loader for markdown prompt templates"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent
    
    def load_system_prompt(self, database: str) -> str:
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
        if not database:
            raise ValueError("Database parameter cannot be empty")
        
        template_file = self.templates_dir / f"{database}_system.md"
        
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        return template_file.read_text(encoding="utf-8")