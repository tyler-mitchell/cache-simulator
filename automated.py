#! /usr/bin/python3
import os
import sys
import subprocess

# check for valid arguments
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("\nUsage: python automated.py -o results.csv\n")
    exit(-1)

csvFileName = sys.argv[2]

# set automated parameters
traceDirectory = "trace-files/"
traceFileNames = [  "TinyTrace.trc", 
                    "TestTrace.trc", 
                    "Corruption1.trc", 
                    "Trace1A.trc", 
                    "Trace2A.trc", 
                    "A-9_new 1.5.pdf.trc" ]
cacheSizes = [ 8, 64, 256, 1024 ]
blockSizes = [ 4, 16, 64 ]
associativities = [ 2 ] # not specified in instructions
replacementPolicies = [ "RR", "RND" ]

# start CSV file and add header row
csvFile = open(csvFileName, "w", newline='')
csvFile.write("Trace File Name, " \
    + "Cache Size (KB), " \
    + "Block Size (bytes), " \
    + "Associativity, " \
    + "Replacement Policy, " 
    + "Total Blocks (KB), " \
    + "Total Blocks Exponent (2^X), " \
    + "Tag Size (bits), " \
    + "Index Size (bits), " \
    + "Total Indicies (KB), " \
    + "Overhead Memory Size (KB), " \
    + "Implementation Memory Size (KB), " 
    + "Cache Hit Rate %, " \
    + "CPI")
csvFile.flush()

print("Running simulations...")

# set arguments
for fileName in traceFileNames:
    for cacheSize in cacheSizes:
        for blockSize in blockSizes:
            for associativity in associativities:
                for replacementPolicy in replacementPolicies:
                    # run program using automated arguments
                    cmd = "python main.py " \
                        + "-f \"" + traceDirectory + fileName + "\" " \
                        + "-s " + str(cacheSize) + " " \
                        + "-b " + str(blockSize) + " " \
                        + "-a " + str(associativity) + " " \
                        + "-r " + replacementPolicy
                    output = subprocess.check_output(cmd).decode("UTF-8")
                    # print("\nOUTPUT:\n", output)
                    output = output.split("\n")

                    # collect "Calculated Values"
                    totalBlocks = output[9-1].split(" ")[4-1][:-2] # in KB
                    totalBlocksExponent = output[9-1].split(" ")[5-1][3:-2] # X where 2^X is number of blocks
                    tagSize = output[10-1].split(" ")[3-1] # in bits
                    indexSize = output[11-1].split(" ")[3-1] # in bits
                    totalIndicies = output[11-1].split(" ")[7-1] # in KB
                    overheadMemorySizeBytes = output[12-1].split(" ")[4-1] # in bytes
                    overheadMemorySizeKB = output[12-1].split(" ")[7-1] # in KB
                    implementationMemorySizeBytes = output[13-1].split(" ")[4-1] # in bytes
                    implementationMemorySizeKB = output[13-1].split(" ")[7-1] # in KB
                    
                    # collect "Results"
                    cacheHitRate = output[15-1].split(" ")[4-1][:-2] # in %
                    CPI = output[16-1].split(" ")[2-1] # number

                    # write simulation arguments and results to CSV
                    csvFile.write("\n\"%s\", %d, %d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
                        fileName,
                        cacheSize,
                        blockSize,
                        associativity,
                        replacementPolicy,
                        totalBlocks,
                        totalBlocksExponent,
                        tagSize,
                        indexSize,
                        totalIndicies,
                        overheadMemorySizeKB,
                        implementationMemorySizeKB,
                        cacheHitRate,
                        CPI
                    ))
                    csvFile.flush()

print("Simulations complete.")
csvFile.close()