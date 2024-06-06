#  **Intro to HPC Computing for Ag Researchers - Spatial**

### **Tutorial objective**
This tutorial contains a machine learning workflow to predict crop types (Corn, Soybeans, Sugarbeets, Spring Wheat) in one county in Minnesota using time series Sentinel data.

### **Data**
Currently stored on Tier 1. 

### **Environment requirements**

To prepare your environment, run the following commands:
- `mamba create -n hpclearn python=3.11`
- `conda activate hpclearn`
- `mamba install --file requirements.txt -c conda-forge`
- `python -m ipykernel install --user --name hpclearn`
