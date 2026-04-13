#Project Name
Three-Layer ET and Two-Source Runoff Model

#Short Description
A Python implementation of coupled evapotranspiration and runoff partitioning algorithms for hydrological analysis.This code is a principle-based implementation of classical hydrological models--XAJ.	

#Project structure

├── .gitignore           
├── README.md 
├── LICENSE            
├── main.py              
├── model.py             
└── precipitation.xlsx  

# Requirements
Python 3.7+
pandas
numpy
openpyxl 

#Input Data
precipitation.xlsx
Input data file containing precipitation time series. No specific format requirements—adjust main.py data reading section as needed for your data structure.

#Outputs
Outputs.xlsx

#Model Parameters
All parameters are defined in main.py with detailed inline comments. Open the file to view and modify:
	params = {
    "WUM":20, "WLM":60, "WDM":40,
    "C":1/6, "b":0.3, "Fc":2.5,
    "WU_0":20, "WL_0":60, "WD_0":40}

#Run
main.py

#Notes
1.This code is a principle-based implementation, not commercial software
2.Model parameters require calibration based on actual watershed characteristics
3.Input data format is flexible—modify main.py to match your data structure
4.All parameters are documented with detailed comments in main.py

#References
Xinanjiang model principles

#License

[MIT](LICENSE)
