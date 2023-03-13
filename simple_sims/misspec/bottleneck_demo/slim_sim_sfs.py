import allel 
import glob
import random
import numpy as np

filelist = glob.glob("bottleneck/vcfs/neut/*final")
sfs_list = []
for vcf in filelist:
    samplist = sorted(random.sample(range(20000), 200))
    loaded_vcf = allel.read_vcf(vcf, fields="*", samples=samplist)
    counts = allel.GenotypeArray(loaded_vcf["calldata/GT"]).count_alleles()
    filt_counts = counts[counts[:, 1] > 0, 1]
    sfs_list.append(allel.sfs(filt_counts))
    
np.savetxt("slim_sfs.csv", np.stack(sfs_list), delimiter=",")