import pandas as pd
from glob import glob

dfs = [pd.read_csv(i, sep="\t") for i in glob("params/*.tsv")]

bigdf = pd.concat(dfs)
filtered = bigdf.loc[:, ["sweep", "rep", "sel_coeff"]]

filtered.to_csv("OoA_params.csv", index=False, header=True)