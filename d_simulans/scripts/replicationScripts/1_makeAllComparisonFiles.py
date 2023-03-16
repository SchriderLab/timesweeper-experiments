import runCmdAsJob

runModes = ["d_simulans_output"]
reps = range(1, 11)
targetChroms = "2L 2R 3L 3R X".split()

for runMode in runModes:
    for rep in reps:
        for targetChrom in targetChroms:
            tsCallFileName = f"../../d_simulans_output/aft_{targetChrom}_{rep}_preds.csv"
            compFileName = f"/pine/scr/d/s/dschride/data/timeSeriesSweeps/compareToFETOut/rep{rep}ScoreComp{targetChrom}_{runMode}.txt"
            inputFileName = f'/proj/dschridelab/drosophila/simulansEAndR/aftInputsVelocity/dsim_chrom_{targetChrom}_rep_{rep}.npz'
            cmd = f"python 5_makeComparisonFile.py {tsCallFileName} {rep} {targetChrom} {inputFileName} {compFileName}"
            logFile = f"logs/{runMode}_rep_{rep}_{targetChrom}.log"
            runCmdAsJob.runCmdAsJobWithoutWaitingWithLog(cmd, "makeCmp", "makeCmp.slurm", "2:00:00", "general", "16G", logFile)
