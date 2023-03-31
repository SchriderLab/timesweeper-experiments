# TimeSweeper Experiments

Repo for experiments for the TimeSweeper manuscript.

The source code for the Timesweeper package can be found here: https://github.com/SchriderLab/Timesweeper

**Note:** All code here was run using the `blinx.yaml` conda environment found in the Timesweeper repo

---

## Parameterization Experiments

Each experiment under the `simple_sims` directory is a basic re-parameterization of the SLiM simulations to test the effect of sample size, selection coefficient, etc. Within each experiment is a pre-made configuration file (`config.yaml`) as well as two scripts. 

1. `simulate.sh` is a simulation SLURM submission script that will launch batches of 50 simulations up to the maximum specified as array jobs. Each simulation replicate takes roughly a minute on average, meaning time generally scales linearly with the number of replicates, but occassionally a lot of restarts will be required to not lose a target mutation which can increase the runtime.
2. `simple_workflow.sh` is a higher-memory high-CPU job (I recommend at least 2GB per core) that will condense simulated VCFs, train the network, and plot the inputs. Depending on the number of replicates, window size, and number of samples/timepoints this can take anywhere from 1-3 hours typically across 16 cores.

Using both of these for each experiment in order will follow the methods used to generate and analyze the data for the majority of the Timesweeper manuscript.

