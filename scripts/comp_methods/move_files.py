import multiprocessing as mp
import os
import sys
import shutil
from tqdm import tqdm

"""Moves files into id-matched directories faster than bash"""


def worker(i):
    for swp in ["neut", "sdn", "ssv"]:
        try:
            shutil.move(
                f"{target_dir}/{swp}/{i}.multivcf.final",
                f"{target_dir}/{swp}/{i}/{i}.multivcf.final",
            )
            for j in range(11):
                shutil.move(
                    f"{target_dir}/{swp}/{i}.final.{swp}.win_{j}.msOut",
                    f"{target_dir}/{swp}/{i}/{i}.final.{swp}.win_{j}.msOut",
                )
                shutil.move(
                    f"{target_dir}/{swp}/{i}.final.{swp}.win_{j}.fvec",
                    f"{target_dir}/{swp}/{i}/{i}.final.{swp}.win_{j}.fvec",
                )
        except:
            pass


target_dir = "/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs"
pool = mp.Pool(mp.cpu_count())
pool.map(worker, list(range(10001)))
