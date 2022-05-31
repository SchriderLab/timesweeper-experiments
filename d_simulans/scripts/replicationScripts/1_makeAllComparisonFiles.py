import runCmdAsJob

#runModes = "logunif_last_0_thresh  logunif_last_25_thresh  logunif_vel_0_thresh  logunif_vel_25_thresh  unif_last_0_thresh  unif_last_25_thresh  unif_velocity_0_thresh  unif_velocity_25_thresh".split()
runModes = "unif_vel_0_thresh unif_vel_0_thresh_rounded unif_last_0_thresh".split()
reps = range(1, 11)
targetChroms = "2L 2R 3L 3R X".split()

for runMode in runModes:
    for rep in reps:
        for targetChrom in targetChroms:
            tsCallFileName = f"/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/timesweeper_output/{runMode}/aft_{targetChrom}_{rep}_preds.csv"
            compFileName = f"/pine/scr/d/s/dschride/data/timeSeriesSweeps/compareToFETOut/rep{rep}ScoreComp{targetChrom}_{runMode}.txt"
            inputFileName = f'/proj/dschridelab/drosophila/simulansEAndR/aftInputsVelocity/dsim_chrom_{targetChrom}_rep_{rep}.npz'
            cmd = f"python makeComparisonFile.py {tsCallFileName} {rep} {targetChrom} {inputFileName} {compFileName}"
            logFile = f"logs/{runMode}_rep_{rep}_{targetChrom}.log"
            runCmdAsJob.runCmdAsJobWithoutWaitingWithLog(cmd, "makeCmp", "makeCmp.slurm", "2:00:00", "general", "16G", logFile)
