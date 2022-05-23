import sys
import numpy as np


inFileName = "/proj/dschridelab/drosophila/simulansEAndR/Dsim_F0-F60_Q20_polymorphic_CMH_FET_blockID.sync"
outDir = "/proj/dschridelab/drosophila/simulansEAndR/aftInputsVelocityRounded/"
winSize = 51
sampleSize = 200
targetChrom = sys.argv[1]

def getRepAndGen(headerEntry):
    genInfo, repInfo = headerEntry.split("_")[-2:]
    rep = int(repInfo)
    if genInfo == "Base":
        gen = 0
    else:
        gen = int(genInfo.lstrip("F"))
    return rep, gen


def getFreqs(baseCounts):
    aCount, tCount, cCount, gCount, nCount, delCount = [int(x) for x in baseCounts.split(":")]
    counts = [aCount, tCount, cCount, gCount, delCount]
    denom = sum(counts)

    return [x/denom for x in counts]


def getWinningAlleleIndex(allFreqsForSnp, mode="final"):
    assert allFreqsForSnp.shape == (7, 5) #7 timepoints X freqs for 5 possible alleles

    freqScores = []
    for alleleIndex in range(allFreqsForSnp.shape[1]):
        if mode == "final":
            freqScore = allFreqsForSnp[-1][alleleIndex]
        elif mode == "velocity":
            freqScore = allFreqsForSnp[-1][alleleIndex] - allFreqsForSnp[0][alleleIndex]
        freqScores.append(freqScore)

    return np.argmax(freqScores)


def getMostCommonOtherAlleleIndex(allFreqsForSnp, winningAlleleIndex):
    assert allFreqsForSnp.shape == (7, 5) #7 timepoints X freqs for 5 possible alleles

    totalFreqs = []
    for alleleIndex in range(allFreqsForSnp.shape[1]):
        if alleleIndex == winningAlleleIndex:
            totalFreqs.append(-1)
        else:
            totalFreq = sum(allFreqsForSnp[:, alleleIndex])
            totalFreqs.append(totalFreq)

    return np.argmax(totalFreqs)


def encodeFreqsInPlace(freqArray, sampleSizeToRound=None):
    for snpIndex in range(len(freqArray[0])):
        allFreqsForSnp = []

        for gen in range(len(freqArray)):
            freqs = freqArray[gen][snpIndex]
            allFreqsForSnp.append(freqs)

        allFreqsForSnp = np.array(allFreqsForSnp)
        winningAlleleIndex = getWinningAlleleIndex(allFreqsForSnp, mode="velocity")
        otherAlleleIndex = getMostCommonOtherAlleleIndex(allFreqsForSnp, winningAlleleIndex)

        for gen in range(len(freqArray)):
            freqs = freqArray[gen][snpIndex]
            winningFreq = freqs[winningAlleleIndex]
            otherFreq = freqs[otherAlleleIndex]

            freq = winningFreq/(winningFreq+otherFreq)
            if sampleSizeToRound:
                count = round(freq*sampleSizeToRound)
                freqArray[gen][snpIndex] = count/sampleSizeToRound
            else:
                freqArray[gen][snpIndex] = freq
        #assert winningFreq > 0 and winningFreq >= otherFreq


#header line copied from README_for_F0-F60SNP_CMH_FET_blockID.sync.docx
header = """Chromosome	position	base	Dsim_Fl_Base_1	Dsim_Fl_Base_2	Dsim_Fl_Base_3	Dsim_Fl_Base_4	Dsim_Fl_Base_5	Dsim_Fl_Base_6	Dsim_Fl_Base_7	Dsim_Fl_Base_8	Dsim_Fl_Base_9	Dsim_Fl_Base_10	Dsim_Fl_Hot_F10_1	Dsim_Fl_Hot_F10_2	Dsim_Fl_Hot_F10_3	Dsim_Fl_Hot_F10_4	Dsim_Fl_Hot_F10_5	Dsim_Fl_Hot_F10_6	Dsim_Fl_Hot_F10_7	Dsim_Fl_Hot_F10_8	Dsim_Fl_Hot_F10_9	Dsim_Fl_Hot_F10_10	Dsim_Fl_Hot_F20_1	Dsim_Fl_Hot_F20_2	Dsim_Fl_Hot_F20_3	Dsim_Fl_Hot_F20_4	Dsim_Fl_Hot_F20_5	Dsim_Fl_Hot_F20_6	Dsim_Fl_Hot_F20_7	Dsim_Fl_Hot_F20_8	Dsim_Fl_Hot_F20_9	Dsim_Fl_Hot_F20_10	Dsim_Fl_Hot_F30_1	Dsim_Fl_Hot_F30_2	Dsim_Fl_Hot_F30_3	Dsim_Fl_Hot_F30_4	Dsim_Fl_Hot_F30_5	Dsim_Fl_Hot_F30_6	Dsim_Fl_Hot_F30_7	Dsim_Fl_Hot_F30_8	Dsim_Fl_Hot_F30_9	Dsim_Fl_Hot_F30_10	Dsim_Fl_Hot_F40_1	Dsim_Fl_Hot_F40_2	Dsim_Fl_Hot_F40_3	Dsim_Fl_Hot_F40_4	Dsim_Fl_Hot_F40_5	Dsim_Fl_Hot_F40_6	Dsim_Fl_Hot_F40_7	Dsim_Fl_Hot_F40_8	Dsim_Fl_Hot_F40_9	Dsim_Fl_Hot_F40_10	Dsim_Fl_Hot_F50_1	Dsim_Fl_Hot_F50_2	Dsim_Fl_Hot_F50_3	Dsim_Fl_Hot_F50_4	Dsim_Fl_Hot_F50_5	Dsim_Fl_Hot_F50_6	Dsim_Fl_Hot_F50_7	Dsim_Fl_Hot_F50_8	Dsim_Fl_Hot_F50_9	Dsim_Fl_Hot_F50_10	Dsim_Fl_Hot_F60_1	Dsim_Fl_Hot_F60_2	Dsim_Fl_Hot_F60_3	Dsim_Fl_Hot_F60_4	Dsim_Fl_Hot_F60_5	Dsim_Fl_Hot_F60_6	Dsim_Fl_Hot_F60_7	Dsim_Fl_Hot_F60_8	Dsim_Fl_Hot_F60_9	Dsim_Fl_Hot_F60_10	-log10(pvalue)_CMH	-log10(p-value)_FET_rep1	-log10(p-value)_FET_rep2	-log10(p-value)_FET_rep3	-log10(p-value)_FET_rep4	-log10(p-value)_FET_rep5	-log10(p-value)_FET_rep6	-log10(p-value)_FET_rep7	-log10(p-value)_FET_rep8	-log10(p-value)_FET_rep9	-log10(p-value)_FET_rep10	blockID_0.75cor	blockID_0.35cor"""
header = header.strip().split()

freqs = {}
for i in range(len(header)):
    if "Dsim" in header[i]:
        rep, gen = getRepAndGen(header[i])
        if not rep in freqs:
            freqs[rep] = {}
        if not gen in freqs[rep]:
            freqs[rep][gen] = {}


sys.stderr.write("reading snps and freqs\n")
positions = {}
with open(inFileName, 'rt') as inFile:
    for line in inFile:
        line = line.strip().split()
        chrom = line[0]
        pos = int(line[1])
        if chrom == targetChrom:
            if not chrom in positions:
                positions[chrom] = []
                for rep in freqs:
                    for gen in freqs[rep]:
                        freqs[rep][gen][chrom] = []

            for i in range(len(line)):
                if ":" in line[i]:
                    rep, gen = getRepAndGen(header[i])
                    currFreqs = getFreqs(line[i])
                    freqs[rep][gen][chrom].append(currFreqs)
            positions[chrom].append(pos)
sys.stderr.write("got all snps and freqs\n")


sys.stderr.write("formatting output\n")
for rep in freqs:
    for chrom in positions:
        outFileName = f"{outDir}/dsim_chrom_{chrom}_rep_{rep}.npz"

        assert len(positions[chrom]) == len(freqs[rep][gen][chrom])

        freqArray = []
        for gen in sorted(freqs[rep]):
            freqArray.append([])
            for posIndex in range(len(positions[chrom])):
                currFreqs = freqs[rep][gen][chrom][posIndex]
                freqArray[-1].append(currFreqs)

        encodeFreqsInPlace(freqArray, sampleSizeToRound=sampleSize)
        freqArray = np.array(freqArray)
        numGens = len(freqs[rep])
        assert freqArray.shape == (numGens, len(positions[chrom]))

        allFreqWins = []
        allPosWins = []
        startingIndices = range(len(positions[chrom]) - winSize)
        for i in startingIndices:
            currWin = freqArray[:, i:i+winSize]
            allFreqWins.append(currWin)
            currPositions = positions[chrom][i:i+winSize]
            allPosWins.append(currPositions)
        assert i+winSize == len(positions[chrom])-1

        allFreqWins = np.array(allFreqWins)
        allPosWins = np.array(allPosWins)
        assert allFreqWins.shape == (len(startingIndices), numGens, winSize)
        assert allPosWins.shape == (len(startingIndices), winSize)

        np.savez(outFileName, aftIn=allFreqWins, aftInPosition=allPosWins)
sys.stderr.write('all done!\n')
