Please parse the following information describing the content of a table in a database following this example:

```json
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
```

The text is in Spanish. Please analyze the PDF content and structure it according to this JSON format.
Return only valid JSON without any additional text or markdown formatting.