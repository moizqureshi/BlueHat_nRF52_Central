from sys import argv
from datetime import datetime

script, inputFilename, outputFilename = argv
time_format = "%Y-%m-%d %H:%M:%S"
itemCount = 0

with open(inputFilename, "r") as inputFile, open(outputFilename, "w") as outputFile:
    for line in inputFile:
        if line is not None:
            line = line.split()
            # if len(line) == 3:
            #     print line[2]
            if len(line) == 2 and line[0] == 'RSSI:':
                print line[1]
