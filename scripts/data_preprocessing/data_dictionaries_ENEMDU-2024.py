import json
import pyreadstat
import pandas as pd

df, meta = pyreadstat.read_sav("BDDenemdu_vivienda_2024_anual.sav")
print(meta.variable_value_labels)  # Dictionary of all value labels

with open("dictionary_vivienda.json", "w") as f:
    json.dump(meta.variable_value_labels, f, indent=4)

df_pandas = pd.DataFrame([v for k,v in meta.readstat_variable_types.items()])
df_pandas.to_excel("types_vivienda.xlsx", index=False)