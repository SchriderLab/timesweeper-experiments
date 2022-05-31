import sys
import glob
import numpy as np

runMode, percentileThresh, printLines, tsOrFet = sys.argv[1:]

assert tsOrFet in ["ts","FET"]
percentileThresh = float(percentileThresh)
printLines = bool(printLines == "True")

allScoreCompFileNames = glob.glob(f"/pine/scr/d/s/dschride/data/timeSeriesSweeps/compareToFETOut/rep*ScoreComp*_{runMode}.txt")

scoreIndex = 2 if tsOrFet == "ts" else 3

scores = []
for cfn in allScoreCompFileNames:
    #sys.stderr.write(f'reading {cfn}\n')
    with open(cfn, 'rt') as cf:
        for line in cf:
            scores.append(float(line.strip().split()[scoreIndex]))
threshold = np.percentile(scores, percentileThresh*100)
sys.stderr.write(f'chosen threshold for {runMode}: ({percentileThresh*100}th percentile): {threshold}\n')

for rep in range(1, 11):
    outLines = []
    expectation, observation = 0, 0
    sys.stderr.write(f'processing rep {rep}\n')
    fn = f"/pine/scr/d/s/dschride/data/timeSeriesSweeps/replicationOfTopHits{'' if tsOrFet == 'ts' else 'FET'}/rep{rep}_{runMode}_repComp.txt"
    with open(fn, 'rt') as f:
        for line in f:
            line = line.strip()
            splitLine = line.split("\t")
            chrom, pos, tsScore, fetScore, freqVel, otherTsScoreStr, otherFetScoreStr, otherFreqVelsStr = splitLine
            pos = int(pos)
            if tsOrFet == "ts":
                otherScores = [float(x) for x in otherTsScoreStr.split("|")]
            else:
                otherScores = [float(x) for x in otherFetScoreStr.split("|")]
            #expectation += 1 - (percentileThresh**len(otherScores))
            expectation += (1-percentileThresh)*len(otherScores)
            replicationVector = [1 if x > threshold else 0 for x in otherScores]
            observation += sum(replicationVector)
            outLines.append((chrom, pos, len(otherScores), replicationVector, line))

    outLines.sort()
    sys.stderr.write(f"observed: {observation}, expected: {expectation}\n")

    if printLines:
        for chrom, pos, otherScoreLen, replicationVector, line in outLines:
            print(str(rep) + "\t" + str(otherScoreLen) + "\t" + "|".join([str(x) for x in replicationVector])  + "\t" + line)
