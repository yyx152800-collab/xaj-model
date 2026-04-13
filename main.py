#code written by Yuxin Ye
import pandas as pd
import numpy as np
from model import run_model

# Read data
data = pd.read_excel("precipitation.xlsx")

# Parameters
''' "WUM": Upper soil water capacity (mm)
    "WLM": Lower soil water capacity (mm)
    "WDM": Deep soil water capacity (mm)
    "C": Deep evaporation coefficient (-)
    "b":Soil moisture distribution index (-)
    "Fc":Stable infiltration rate (mm/h)
    "WU_0":Initial upper soil moisture (mm)
    "WL_0": Initial lower soil moisture (mm)
    "WD_0":Initial deep soil moisture (mm)'''
params = {
    "WUM":20, "WLM":60, "WDM":40,
    "C":1/6, "b":0.3, "Fc":2.5,
    "WU_0":20, "WL_0":60, "WD_0":40
}

# Run the model
result = run_model(data, params)
df = pd.DataFrame(result)

# Save results
df.to_excel("output.xlsx", index=False)