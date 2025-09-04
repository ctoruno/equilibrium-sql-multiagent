import os
import json
from io import BytesIO

import PyPDF2
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

instructions_enaho_2024 = """
Please parse the following information describing the content of a table in a database following this example:

{
    "tables": {
        "ENAHO01-2024-100": {
            "metadata": {
                "description": "Características de la Vivienda y del Hogar (Módulo 100)",
                "file_name": "ENAHO01-2024-100",
                "business_domain": ["housing", "demographics", "geographic"],
                "record_level": "household",
                "module_number": "100"
            },
            "columns": {
                "AÑO": {
                    "description": "Año de la Encuesta",
                    "data_type": "CHARACTER",
                    "size": 4,
                    "decimals": 0,
                    "business_meaning": "Survey year identifier"
                },
                "DOMINIO": {
                    "description": "Dominio Geográfico",
                    "data_type": "NUMERIC",
                    "size": 1,
                    "decimals": 0,
                    "valid_values": {
                        "1": "Costa Norte",
                        "2": "Costa Centro",
                        "3": "Costa Sur",
                        "4": "Sierra Norte",
                        "5": "Sierra Centro",
                        "6": "Sierra Sur",
                        "7": "Selva",
                        "8": "Lima Metropolitana"
                    },
                    "range": "1-8",
                    "business_meaning": "Geographic domain classification"
                },
                "P101": {
                    "description": "Tipo de vivienda",
                    "data_type": "NUMERIC",
                    "size": 1,
                    "decimals": 0,
                    "valid_values": {
                        "1": "Casa independiente",
                        "2": "Departamento en edificio",
                        "3": "Vivienda en quinta",
                        "4": "Vivienda en casa de vecindad (Callejón, solar o corralón)",
                        "5": "Choza o cabaña",
                        "6": "Vivienda improvisada",
                        "7": "Local no destinado para habitación humana",
                        "8": "Otro"
                    },
                    "range": "1-8",
                    "business_meaning": "Housing type classification"
                }
            }
        }
    }
}

The text is in Spanish. Please analyze the PDF content and structure it according to this JSON format.
Return only valid JSON without any additional text or markdown formatting.
"""

instructions_geih_2024 = """
Please parse the following information describing the content of a table in a database following this example:

{
    "tables": {
        "DBF_GECH_45_21": {
            "metadata": {
                "description": "Datos del hogar y la vivienda",
                "file_name": "DBF_GECH_45_21",
                "business_domain": ["housing", "demographics"],
                "record_level": "household",
                "module_number": "45_21"
            },
            "columns": {
                "MES": {
                    "description": "Hace referencia al mes en que fue recolectada la informaciÃ³n de la encuesta.",
                    "data_type": "CHARACTER",
                    "size": 2,
                    "decimals": 0,
                    "business_meaning": "Survey month identifier"
                },
                "P4030S1A1": {
                    "description": "Estrato para tarifa",
                    "data_type": "NUMERIC",
                    "size": 1,
                    "decimals": 0,
                    "valid_values": {
                        "1": "Bajo - Bajo",
                        "2": "Bajo",
                        "3": "Medio - Bajo",
                        "4": "Medio",
                        "5": "Medio - Alto",
                        "6": "Alto",
                        "9": "No sabe o cuenta con planta electrica",
                        "0": "Conexión pirata"
                    },
                    "range": "1-8",
                    "business_meaning": "Socioeconomic stratum assigned for electricity billing, used to classify households."
                },
                "P5222S7": {
                    "description": "¿Cuáles de los siguientes productos financieros utiliza usted o algún miembro del hogar actualmente?",
                    "data_type": "NUMERIC",
                    "size": 1,
                    "decimals": 0,
                    "valid_values": {
                        "7": "Tarjeta de crédito"
                    },
                    "range": "1-1",
                    "business_meaning": "Indicates if the household uses credit cards as a financial product."
                }
            }
        }
    }
}

Take into account the following:
- The text is in Spanish and it contains some encoding issues for words with special characters. Please infer the correct word in those cases. 
- Use the table description and also the content of the whole text to complete the business_domain and record_level metadata keys. If the 
description of a table is missing, you will have to rely in the content of the text to infer it.
- Use the "PREGUNTA LITERAL" section to extract the description of each column(variable). No need to report the question answers, just the question itself.
If no "Pregunta Literal" section is found, pass the variable name as description.
- Infer the business_meaning of each variable based on its description (DESCRIPCION) and the available information.
- The valid_values dictionary should include all the possible values for a column, usually listed under CATEGORIAS section. If not available, omit this key.
- Please analyze the content and structure it according to this JSON format. Return only valid JSON without any additional text or markdown formatting.
"""

instructions = {
    "enaho-2024": instructions_enaho_2024,
    "geih-2024": instructions_geih_2024
}

class OpenAIParser:
    def __init__(self, survey: str):
        """
        Initialize the OpenAI parser
        
        Args:
            survey (str): Survey documentation to parse.
        """
        
        self.openai_client = OpenAI()

        self.gcs_client = storage.Client()
        if not self.gcs_client:
                raise Exception("GCP client not initialized. Please provide credentials.")
        
        if survey not in ["enaho-2024", "geih-2024"]:
            raise ValueError("Survey must be either 'enaho-2024' or 'geih-2024'")
        else:
            self.survey = survey
            self.instruction = instructions[self.survey]
            if self.survey == "enaho-2024":
                self.bucket_name = "sql-multiagent-enaho-2024"
            if self.survey == "geih-2024":
                self.bucket_name = "sql-multiagent-geih-2024"
            

    def list_files_in_bucket(self, prefix: str, format: str) -> list:
        """
        List all files in a GCS bucket.
        
        Args:
            bucket_name (str): Name of the GCS bucket
            prefix (str): Prefix to filter files
            format (str): File format to filter (e.g., '.pdf', '.md')
            
        Returns:
            list: List of file names
        """
        if not self.gcs_client:
            raise Exception("GCP client not initialized. Please provide credentials.")
        
        try:
            bucket = self.gcs_client.bucket(self.bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)
            
            files = []
            for blob in blobs:
                if blob.name.lower().endswith(format):
                    files.append(blob.name)
            
            return files
            
        except Exception as e:
            raise Exception(f"Error listing files in bucket: {str(e)}")
        
    
    def read_pdf_from_gcs(self, blob_name: str) -> str:
        """
        Read text content from a PDF file stored in Google Cloud Storage.
        
        Args:
            bucket_name (str): Name of the GCS bucket
            blob_name (str): Name/path of the PDF file in the bucket
            
        Returns:
            str: Extracted text content from the PDF
        """

        if not self.gcs_client:
            raise Exception("GCP client not initialized. Please provide credentials.")
        
        try:
            bucket = self.gcs_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)            
            pdf_bytes = blob.download_as_bytes()
            pdf_stream = BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            return text_content.strip()
            
        except Exception as e:
            raise Exception(f"Error reading PDF from GCS: {str(e)}")
        
    
    def read_md_from_gcs(self, blob_name: str) -> str:
        """
        Read text content from a Markdown file stored in Google Cloud Storage.
        
        Args:
            blob_name (str): Name/path of the Markdown file in the bucket
            
        Returns:
            str: Text content from the Markdown file
        """
        
        if not self.gcs_client:
            raise Exception("GCP client not initialized. Please provide credentials.")
        
        try:
            bucket = self.gcs_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)            
            md_content = blob.download_as_text(encoding='utf-8')
            
            return md_content.strip()
            
        except Exception as e:
            raise Exception(f"Error reading Markdown from GCS: {str(e)}")
    

    def send_to_openai(self, content: str, model: str = "gpt-5") -> str:
        """
        Send PDF content to OpenAI API with predefined instructions.
        
        Args:
            pdf_content (str): Text content extracted from PDF
            model (str): OpenAI model to use (default: gpt-4)
            
        Returns:
            str: Response from OpenAI API
        """
        try:
            response = self.openai_client.responses.create(
                model = model,
                reasoning = {"effort": "low"},
                input=[
                    {
                        "role": "developer",
                        "content": "You are a data analyst expert in parsing survey database documentation and creating structured JSON representations."
                    },
                    {
                        "role": "user",
                        "content": f"{self.instruction}\n\nPDF Content:\n{content}"
                    }
                ]
            )
            
            return response.output_text
            
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
        
    
    def save_json(self, data: str, filename: str) -> None:
        """
        Save the API response as a JSON file locally and/or upload to GCS.
        
        Args:
            data (str): JSON string from OpenAI API
            output_path (str): Local path where to save the JSON file, or filename if uploading to GCS only
            gcs_bucket (str): Optional GCS bucket name to upload the file
        """
        
        if not self.gcs_client:
                raise Exception("GCP client not initialized. Cannot upload to GCS.")
        
        try:
            parsed_data = json.loads(data)            
            json_content = json.dumps(parsed_data, indent=2, ensure_ascii=False)
            
            gcs_object_name = f"dictionaries/{filename}"
            bucket = self.gcs_client.bucket(self.bucket_name)
            blob = bucket.blob(gcs_object_name)            
            blob.upload_from_string(json_content, content_type='application/json')
            
            print(f"JSON file uploaded to GCS: gs://{self.bucket_name}/{gcs_object_name}")
            
        except json.JSONDecodeError as e:
            print("Warning: Response is not valid JSON. Saving as text file...")
            raise Exception(f"Invalid JSON response: {str(e)}")
            
        except Exception as e:
            raise Exception(f"Error uploading file: {str(e)}")
        

def main():
    """Command line interface for the parser."""
    parser = argparse.ArgumentParser(description="Parse documentation using OpenAI API and save as JSON")
    parser.add_argument("--survey", help="Survey name to work with (e.g., 'enaho-2024', 'geih-2024')")
    
    args = parser.parse_args()

    if args.survey not in ["enaho-2024", "geih-2024"]:
        print("❌ Error: Survey must be either 'enaho-2024' or 'geih-2024'")
        return 1
    else:
        print(f"✅ Survey selected: {args.survey}")

    try:
        parser = OpenAIParser(survey=args.survey)
        
        if args.survey in ["enaho-2024"]:
            pdf_files = parser.list_files_in_bucket(prefix="dictionaries/", format=".pdf")
            if not pdf_files:
                print("No PDF files found in the specified bucket.")
                return 1

            for pdf_file in pdf_files:
                print(f"Processing file: {pdf_file}")
                pdf_content = parser.read_pdf_from_gcs(pdf_file)
                response = parser.send_to_openai(pdf_content, model="gpt-5")
                
                base_filename = os.path.basename(pdf_file).replace(".pdf", ".json")
                parser.save_json(response, base_filename)
                print(f"✅ Successfully processed and saved: {base_filename}")
        
        if args.survey in ["geih-2024"]:
            md_files = parser.list_files_in_bucket(prefix="dictionaries/", format=".md")
            if not md_files:
                print("No MD files found in the specified bucket.")
                return 1

            for md_file in md_files:
                print(f"Processing file: {md_file}")
                md_content = parser.read_md_from_gcs(md_file)
                response = parser.send_to_openai(md_content, model="gpt-5")
                
                base_filename = os.path.basename(md_file).replace(".md", ".json")
                parser.save_json(response, base_filename)
                print(f"✅ Successfully processed and saved: {base_filename}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    main()
