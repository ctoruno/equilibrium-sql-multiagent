import logging
import sys
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from dotenv import load_dotenv

class GEIHDataDictionaryScraper:
    """
    Web scraper for GEIH 2024 data dictionary documentation.
    
    Scrapes variable information from DANE's microdata catalog and uploads
    formatted documentation to Google Cloud Storage.
    """
    
    def __init__(self, bucket_name: str):
        """
        Initialize the scraper with GCS configuration.
        
        Args:
            bucket_name: Name of the Google Cloud Storage bucket
            
        Raises:
            GoogleCloudError: If unable to connect to GCS
        """
        self.bucket_name = bucket_name
        self.base_url = "https://microdatos.dane.gov.co"
        
        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(bucket_name)
        except GoogleCloudError as e:
            logging.error(f"Failed to initialize GCS client: {e}")
            raise
    

    @staticmethod
    def get_table_config() -> List[Dict[str, str]]:
        """
        Get the configuration for all GEIH tables to process.
        
        Returns:
            List of dictionaries containing module, table_name, and doc_url
        """
        modules = [
            "Caracteristicas generales, seguridad social en salud y educacion",
            "Ocupados",
            "Fuerza de trabajo",
            "No ocupados",
            "Otras formas de trabajo",
            "Migracion",
            "Datos del hogar y la vivienda",
            "Otros ingresos e impuestos"
        ]
        
        table_names = [
            "DBF_GECH_6_234",
            "DBF_GECH_6_67",
            "DBF_GECH_6_5",
            "DBF_GECH_6_8",
            "DBF_GECH_6_9",
            "DBF_GECH_6_13",
            "DBF_GECH_45_21",
            "DBF_GECH_6_10"
        ]
        
        doc_urls = [
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F63?file_name=Caracteristicas%20generales,%20seguridad%20social%20en%20salud%20y%20educacion",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F64?file_name=Ocupados",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F65?file_name=Fuerza%20de%20trabajo",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F66?file_name=No%20ocupados",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F67?file_name=Otras%20formas%20de%20trabajo",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F68?file_name=Migracion",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F69?file_name=Datos%20del%20hogar%20y%20la%20vivienda",
            "https://microdatos.dane.gov.co/index.php/catalog/819/data-dictionary/F70?file_name=Otros%20ingresos%20e%20impuestos"
        ]
        
        return [
            {"module": m, "table_name": t, "doc_url": u}
            for m, t, u in zip(modules, table_names, doc_urls)
        ]
    

    def fetch_page(self, url: str, timeout: int = 30) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None
    

    def extract_variable_info(self, var_url: str, var_name: str) -> Optional[str]:
        """
        Extract variable information from a variable detail page.
        
        Args:
            var_url: URL of the variable detail page
            var_name: Name of the variable
            
        Returns:
            Formatted variable description or None if failed
        """
        
        # Handle relative URLs (NOT USED)
        if var_url.startswith('/'):
            var_url = urljoin(self.base_url, var_url)
        
        soup = self.fetch_page(var_url)
        if not soup:
            return None
        
        try:
            var_container = soup.find("div", class_="variable-container")
            if not var_container:
                logging.warning(f"Variable container not found for {var_name}")
                return None
            
            var_info = (
                var_container.text.strip()
                .replace("\n\n", "\n")
                .replace("\t\t", " ")
                .replace("\n\n", "\n")
            )
            
            return f"""
            Variable Name: {var_name}
            {var_info}
            [END OF VARIABLE DESCRIPTION]
            """
        
        except Exception as e:
            logging.error(f"Failed to extract variable info for {var_name}: {e}")
            return None
    

    def scrape_table_documentation(self, table_config: Dict[str, str]) -> Optional[str]:
        """
        Scrape documentation for a single table.
        
        Args:
            table_config: Dictionary with module, table_name, and doc_url
            
        Returns:
            Formatted markdown documentation or None if failed
        """
        logging.info(f"Processing table: {table_config['module']}")
        
        soup = self.fetch_page(table_config["doc_url"])
        if not soup:
            return None
        
        try:
            datafile_container = soup.find("div", {"id": "datafile-container"})
            description = datafile_container.text.strip() if datafile_container else "No description available"
            
            variables_container = soup.find("div", {"id": "variables-container"})
            if not variables_container:
                logging.warning(f"No variables container found for {table_config['module']}")
                return None
            
            data_dict = variables_container.find("div", class_="data-dictionary")
            if not data_dict:
                logging.warning(f"No data dictionary found for {table_config['module']}")
                return None
            
            variables = data_dict.find_all("a", class_="var-id text-break")
            
            vdesc_list = []
            for variable in variables:
                var_url = variable.get("href")
                var_name = variable.text.strip()
                
                logging.info(f"--- Fetching variable: {var_name}")
                
                var_desc = self.extract_variable_info(var_url, var_name)
                if var_desc:
                    vdesc_list.append(var_desc)
                    logging.info(f"--- Completed variable: {var_name}")
                else:
                    logging.warning(f"--- Failed to process variable: {var_name}")
            
            documentation = f"""
            # TABLE: {table_config["table_name"]}

            ## Module Description
            {table_config["module"]}

            ## Table Description
            {description}

            ## Variables
            {chr(10).join(vdesc_list)}
            """
            return documentation
            
        except Exception as e:
            logging.error(f"Failed to scrape table {table_config['module']}: {e}")
            return None
    

    def upload_documentation(self, content: str, filename: str, prefix: str = "dictionaries") -> bool:
        """
        Upload documentation to Google Cloud Storage.
        
        Args:
            content: Documentation content to upload
            filename: Name for the file (without extension)
            prefix: GCS prefix/folder
            
        Returns:
            True if successful, False otherwise
        """
        try:
            blob_name = f"{prefix}/{filename}.md"
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(content, content_type="text/markdown")
            
            logging.info(f"Uploaded {blob_name} to bucket {self.bucket_name}")
            return True
            
        except GoogleCloudError as e:
            logging.error(f"Failed to upload {filename}: {e}")
            return False
    

    def run(self) -> None:
        """
        Run the complete scraping and upload process for all tables.
        """
        table_configs = self.get_table_config()
        
        success_count = 0
        failure_count = 0
        
        for table_config in table_configs:
            try:
                documentation = self.scrape_table_documentation(table_config)
                
                if documentation:
                    if self.upload_documentation(
                        documentation, 
                        table_config["table_name"],
                        "dictionaries"
                    ):
                        success_count += 1
                    else:
                        failure_count += 1
                else:
                    failure_count += 1
                
                logging.info("=" * 50)
                
            except Exception as e:
                logging.error(f"Unexpected error processing {table_config['module']}: {e}")
                failure_count += 1
        
        logging.info(f"Process completed. Success: {success_count}, Failures: {failure_count}")


def setup_logging(level: str = "INFO") -> None:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('geih_scraper.log')
        ]
    )


def main() -> None:
    """
    Main entry point for the application.
    """
    load_dotenv()
    setup_logging()
    BUCKET_NAME = "sql-multiagent-geih-2024"
    
    try:
        scraper = GEIHDataDictionaryScraper(BUCKET_NAME)
        scraper.run()
        
    except Exception as e:
        logging.error(f"Application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()






