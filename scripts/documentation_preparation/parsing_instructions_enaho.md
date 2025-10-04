Please parse the following information describing the content of a table in a database following this example:

```json
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
```

The text is in Spanish. Please analyze the PDF content and structure it according to this JSON format.
Return only valid JSON without any additional text or markdown formatting.