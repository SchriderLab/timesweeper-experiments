import sys
import numpy as np
import scipy.stats
from sklearn import metrics
import matplotlib.pyplot as plt


origCallFileName = "/proj/dschridelab/drosophila/simulansEAndR/Dsim_F0-F60_Q20_polymorphic_CMH_FET_blockID.sync"
tsCallDir = f"/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/timesweeper_output"

tsCallFileName, rep, targetChrom, inputFileName, compFileName = sys.argv[1:]
rep = int(rep)

def runComps(tsCallFileName, inputFileName, compFileName):
    inputs = np.load(inputFileName)
    freqs = inputs['aftIn'][:,:,25]
    positions = inputs['aftInPosition'][:,25]
    assert len(freqs) == len(positions)


    tsScores = {}
    first = True
    try:
        with open(tsCallFileName, 'rt') as tsf:
            for line in tsf:
                if first:
                    first = False
                else:
                    chrom, pos, classPred, neutProb, softProb, winS, winE = line.strip().split("\t")
                    pos = int(pos)
                    tsScores[(chrom, pos)] = float(softProb)
    except Exception as err:
        print('Error reading tsCallFile:', err)
        return


    header = """Chromosome  position        base    Dsim_Fl_Base_1  Dsim_Fl_Base_2  Dsim_Fl_Base_3  Dsim_Fl_Base_4  Dsim_Fl_Base_5  Dsim_Fl_Base_6  Dsim_Fl_Base_7  Dsim_Fl_Base_8  Dsim_Fl_Base_9  Dsim_Fl_Base_10 Dsim_Fl_Hot_F10_1       Dsim_Fl_Hot_F10_2       Dsim_Fl_Hot_F10_3       Dsim_Fl_Hot_F10_4       Dsim_Fl_Hot_F10_5       Dsim_Fl_Hot_F10_6       Dsim_Fl_Hot_F10_7       Dsim_Fl_Hot_F10_8       Dsim_Fl_Hot_F10_9       Dsim_Fl_Hot_F10_10      Dsim_Fl_Hot_F20_1       Dsim_Fl_Hot_F20_2       Dsim_Fl_Hot_F20_3       Dsim_Fl_Hot_F20_4       Dsim_Fl_Hot_F20_5       Dsim_Fl_Hot_F20_6       Dsim_Fl_Hot_F20_7       Dsim_Fl_Hot_F20_8       Dsim_Fl_Hot_F20_9       Dsim_Fl_Hot_F20_10      Dsim_Fl_Hot_F30_1       Dsim_Fl_Hot_F30_2       Dsim_Fl_Hot_F30_3       Dsim_Fl_Hot_F30_4       Dsim_Fl_Hot_F30_5       Dsim_Fl_Hot_F30_6       Dsim_Fl_Hot_F30_7       Dsim_Fl_Hot_F30_8       Dsim_Fl_Hot_F30_9       Dsim_Fl_Hot_F30_10      Dsim_Fl_Hot_F40_1       Dsim_Fl_Hot_F40_2       Dsim_Fl_Hot_F40_3       Dsim_Fl_Hot_F40_4       Dsim_Fl_Hot_F40_5       Dsim_Fl_Hot_F40_6       Dsim_Fl_Hot_F40_7       Dsim_Fl_Hot_F40_8       Dsim_Fl_Hot_F40_9       Dsim_Fl_Hot_F40_10      Dsim_Fl_Hot_F50_1       Dsim_Fl_Hot_F50_2       Dsim_Fl_Hot_F50_3       Dsim_Fl_Hot_F50_4       Dsim_Fl_Hot_F50_5       Dsim_Fl_Hot_F50_6       Dsim_Fl_Hot_F50_7       Dsim_Fl_Hot_F50_8       Dsim_Fl_Hot_F50_9       Dsim_Fl_Hot_F50_10      Dsim_Fl_Hot_F60_1       Dsim_Fl_Hot_F60_2       Dsim_Fl_Hot_F60_3       Dsim_Fl_Hot_F60_4       Dsim_Fl_Hot_F60_5       Dsim_Fl_Hot_F60_6       Dsim_Fl_Hot_F60_7       Dsim_Fl_Hot_F60_8       Dsim_Fl_Hot_F60_9       Dsim_Fl_Hot_F60_10      -log10(pvalue)_CMH      -log10(p-value)_FET_rep1        -log10(p-value)_FET_rep2        -log10(p-value)_FET_rep3        -log10(p-value)_FET_rep4        -log10(p-value)_FET_rep5        -log10(p-value)_FET_rep6        -log10(p-value)_FET_rep7        -log10(p-value)_FET_rep8        -log10(p-value)_FET_rep9        -log10(p-value)_FET_rep10       blockID_0.75cor blockID_0.35cor""".split()

    focalRepTestIndex = header.index(f"-log10(p-value)_FET_rep{rep}")
    otherRepTestIndices = [header.index(f"-log10(p-value)_FET_rep{x}") for x in range(1, 11) if x != rep]

    ogScores = {}
    otherScores = {}
    with open(origCallFileName, 'rt') as of:
        for line in of:
            line = line.strip().split("\t")
            chrom, pos = line[0], line[1]
            pos = int(pos)

            #Note: setting missing test values to -1, which works because these are -log10(p-value) so they should never be negative
            ogScores[(chrom, pos)] = float(line[focalRepTestIndex]) if line[focalRepTestIndex] != "na" else -1
            otherScores[(chrom, pos)] = [float(line[x]) if line[x] != "na" else -1 for x in otherRepTestIndices]


    y = []
    tsY, ogY = [], []
    with open(compFileName, 'wt') as compF:
        for i in range(len(positions)):
            loc = (targetChrom, positions[i])
            if loc in tsScores and loc in ogScores and loc in otherScores:
                #print(loc, tsScores[loc], ogScores[loc], otherScores[loc])
                maxOther = max(otherScores[loc])
                if ogScores[loc] != -1 and maxOther != -1:
                    freqStr =  "\t".join([f'{x:.4f}' for x in freqs[i]])
                    outLine = "\t".join([str(x) for x in [loc[0], loc[1], tsScores[loc], ogScores[loc], maxOther]]) + "\t" + freqStr
                    compF.write(outLine + "\n")
                    if maxOther >= 30:
                        y.append(1)
                    else:
                        y.append(0)
                    tsY.append(tsScores[loc])
                    ogY.append(ogScores[loc])


runComps(tsCallFileName, inputFileName, compFileName)
