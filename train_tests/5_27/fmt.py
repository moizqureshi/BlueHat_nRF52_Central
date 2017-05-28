#
# with open('rawData2.txt') as inputFile, open('rawData3.txt', 'w') as outputFile:
#     outputFile.write('Ratio,Distance\n')
#     inputFile.next()
#     for line in inputFile:
#         line = line.strip().split(",")
#         ratio = float(line[0])/-51
#         distance = float(line[1])
#         # print("%f,%s" % (ratio, line[1]))
#         outputFile.write("%f,%s" % (ratio, distance))
#         outputFile.write('\n')

with open('rawData.txt') as inputFile:
    inputFile.next()
    for line in inputFile:
        line = line.strip().split(",")
        if line[1]=='50':
            print line[0]+',',
