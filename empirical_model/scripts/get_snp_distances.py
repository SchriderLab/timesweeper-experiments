import sys
import allel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Iterates through VCF file and calculates snp distances from left-most to right-most polymorphism in windows."""
win_size = 51
vcf_file = sys.argv[1]

fields = ["variants/CHROM", "variants/POS"]
_fields, _samples, _headers, vcf_iter = allel.iter_vcf_chunks(
    vcf_file, fields=fields, chunk_length=10000000
)

for chunk in vcf_iter:
    chunk = chunk[0]
    chroms, bps = list(chunk["variants/CHROM"]), list(chunk["variants/POS"])
    # print(chroms[:50], bps[:50])
    res = []
    for i in range(0, len(bps) - win_size):
        if chroms[i] == chroms[i + win_size]:
            dist = bps[i + win_size] - bps[i]
            res.append(dist)
        else:
            continue
    # print(res)
    res = np.array(res)
    print(np.median(res))
    print(np.mean(res))
    print(np.std(res))
    # hist = np.histogram(np.array(res), bins=10))
    res = res[res <= 2e6]
    plt.hist(res, 50)
    plt.yscale("log")
    plt.xlabel("Distance Bins (50)")
    plt.ylabel("log10(occurances)")
    plt.savefig("dists_0_7_filtered.png")

