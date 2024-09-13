   
# Import all required packages
import pandas as pd
import numpy as np
import multiprocessing as mp
import csv
import sys
import os

# read in the dataframe
#df = pd.read_csv('chr1_A_matrix.csv', index_col=0)

outprefix = sys.argv[1]
data = sys.argv[2]
df = pd.read_csv(data, index_col=0)

# Generate all unique combinations of columns and store as a list in pair
pair = [[i, j] for i in range(len(df.columns)-1) for j in range(i+1, len(df.columns))]
    
# Split the list subarrays
pair_split = np.array_split(pair, 10)
    
# Define the function that compares elements of the two columns and calculates percentage difference in the columns
# Fix the dataframe argument to take in the df of interest and let combination remain a variable to iterate over
def Perc_diff(combn, df = df):
    pair = df.iloc[:, combn]
    pairNoNA = pair.dropna()
    TotalSites = pairNoNA.shape[0]
    DiffSites = np.sum(pairNoNA[pairNoNA.columns[0]] != pairNoNA[pairNoNA.columns[1]])
    PercDiff = round((DiffSites * 100)/ TotalSites, 2)
    # Generate a list as output
    result = [pair.columns[0], pair.columns[1], TotalSites, DiffSites, PercDiff]
    
    return result


def SNP_parallel(x):
    #Using multiprocessing for parallel computation, instantiate pool and assign the total number of cores available using mp.cpu_count()
    pool = mp.Pool(mp.cpu_count())
    # Apply the funtion over one subarray of pair_split at a time usine pool.map as follows
    results = pool.map(Perc_diff, [combn for combn in pair_split[x]])
    # Do not forget to close the pool
    pool.close()
    
    return results
   
x = int(sys.argv[3])
print("x is ", x)
results = SNP_parallel(x)
# Convert the results list into a dataframe
Results = pd.DataFrame(results, columns = ['Sample1', 'Sample2', 'Total_sites', 'Diff_Sites', 'Percent_Diff'])

# Save the results dataframe as a csv file
Results.to_csv(outprefix+'/'+outprefix+'_%s.csv' %x, index=False)
print(Results.head())

