import runCmdAsJob

#runModes = "logunif_last_0_thresh  logunif_last_25_thresh  logunif_vel_0_thresh  logunif_vel_25_thresh  unif_last_0_thresh  unif_last_25_thresh  unif_velocity_0_thresh  unif_velocity_25_thresh".split()
runModes = "unif_vel_0_thresh unif_vel_0_thresh_rounded unif_last_0_thresh".split()
reps = range(1, 11)
targetChroms = "2L 2R 3L 3R X".split()

def readCompFile(compFileName, compDataForRep):
    try:
        with open(compFileName, 'rt') as cf:
            for line in cf:
                line = line.strip().split()

                c, p, ts, fet, maxOtherFet = line[:5]
                p, ts, fet, maxOtherFet = int(p), float(ts), float(fet), float(maxOtherFet)
                freqs = [float(x) for x in line[5:]]

                assert not (c, p) in compDataForRep
                compDataForRep[(c, p)] = (ts, fet, freqs)
    except Exception as err:
        print('Error reading compFile:', err)


def getBestHitsByTs(compDataForRep, top=100):
    hits = []
    for (c, p) in compDataForRep:
        ts = compDataForRep[(c, p)][0]
        if ts > 0.9:
            hits.append((ts, c, p))

    hits.sort()
    bestHits = [(x[1], x[2]) for x in hits[-top:]]
    if len(bestHits) != top:
        print(f"\twarning: only {len(bestHits)} of {top} desired bestHits found!")
    return bestHits


for runMode in runModes:
    print(f"working on {runMode}")
    compData = {}
    for targetChrom in targetChroms:
        print(f"\treading {targetChrom}")
        for rep in reps:
            print(f"\t\treading rep {rep}")

            compFileName = f"/pine/scr/d/s/dschride/data/timeSeriesSweeps/compareToFETOut/rep{rep}ScoreComp{targetChrom}_{runMode}.txt"
            if not rep in compData:
                compData[rep] = {}
            readCompFile(compFileName, compData[rep])
            
    for rep in reps:
        print(f"\tworking on rep {rep} after reading in all chroms")

        outFileName = f"/pine/scr/d/s/dschride/data/timeSeriesSweeps/replicationOfTopHits/rep{rep}_{runMode}_repComp.txt"
        with open(outFileName, 'wt') as outFile:
            bestHits = getBestHitsByTs(compData[rep])
            found, total = 0, 0
            for chrom, pos in bestHits:

                tsScore, fetScore, freqVel = compData[rep][(chrom, pos)]
                otherTsScores, otherFetScores, otherFreqVels = [], [], []

                for otherRep in [x for x in reps if x != rep]:
                    if (chrom, pos) in compData[otherRep]:
                        otherTsScore, otherFetScore, otherFreqVel = compData[otherRep][(chrom, pos)]
                        otherTsScores.append(otherTsScore)
                        otherFetScores.append(otherFetScore)
                        otherFreqVels.append(otherFreqVel)
                        found += 1
                    total += 1

                otherTsScoreStr = "|".join([str(x) for x in otherTsScores])
                otherFetScoreStr = "|".join([str(x) for x in otherFetScores])
                otherFreqVelsStr = "|".join([str(x) for x in otherFreqVels])
                outFile.write(f"{chrom}\t{pos}\t{tsScore}\t{fetScore}\t{freqVel}\t{otherTsScoreStr}\t{otherFetScoreStr}\t{otherFreqVelsStr}\n")
            if total > 0:
                print(f"fraction of other reps containing scores to compare to focal rep {rep}: {found/total}")
