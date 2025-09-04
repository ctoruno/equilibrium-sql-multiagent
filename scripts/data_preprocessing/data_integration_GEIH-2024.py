"""
This script integrates monthly CSV files from the GEIH 2024 dataset into annual CSV files.
File names needed to be adjusted due to encoding issues.
"""

import pandas as pd

path2data = "../GEIH-2024/data"
months = [
    "Enero_2024",
    "Febrero_2024", 
    "Marzo_2024",
    "Abril_2024",
    "Mayo_2024",
    "Junio_2024",
    "Julio_2024",
    "Agosto_2024",
    "Septiembre_2024",
    "Octubre_2024",
    "Noviembre_2024",
    "Diciembre_2024"
]
files = [
    'Características generales, seguridad social en salud y educación.CSV',
    'Migración.CSV',
    'Datos del hogar y la vivienda.CSV',
    'Otros ingresos e impuestos.CSV',
    'Ocupados.CSV',
    'Fuerza de trabajo.CSV',
    'No ocupados.CSV',
    'Otras formas de trabajo.CSV'
]

for file in files:
    data_list = []
    for month in months:
        print(f"Processing {file} for {month}...")
        try:
            df = pd.read_csv(f"{path2data}/{month}/CSV/{file}")
        except UnicodeDecodeError:
            df = pd.read_csv(f"{path2data}/{month}/CSV/{file}", encoding='latin1')
        data_list.append(df)
    full_data = pd.concat(data_list, ignore_index=True)
    full_data.to_csv(f"{path2data}/2024-CSV/{file.lower()}", index=False)