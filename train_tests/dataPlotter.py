from sys import argv
import plotly.plotly as py
from plotly.graph_objs import *

script, inputFilename, outputFilename, distance = argv
deviceID = ''
prevLine = ''

rssiInside = 0
rssiOutside = 0

tickInside = 1
tickOutside = 1

rssiInsideVals = []
rssiOutsideVals = []

ticksInside = []
ticksOutside = []

print inputFilename
with open(inputFilename, "r") as inputFile, open(outputFilename, "w") as outputFile:
    print inputFilename
    for line in inputFile:
        if line is not None:
            line = line.split()
            if len(line) == 2 and line[0] == 'ID:':
                if line[1] == 'aaaaaaaa':
                    deviceID = 'Inside Hat'
                    prevLine = 'a'
                if line[1] == 'bbbbbbbb':
                    deviceID = 'Outside Hat'
                    prevLine = 'b'
            if len(line) == 2 and line[0] == 'RSSI:':
                if prevLine == 'a':
                    rssiInside = int(line[1])
                    ticksInside.insert(tickInside, tickInside)
                    rssiInsideVals.insert(tickInside, rssiInside)
                    print ('%s,%d,%d') % (deviceID, tickInside, rssiInside)
                    outputFile.write(deviceID)
                    outputFile.write(',')
                    outputFile.write(str(rssiInside))
                    outputFile.write('\n')
                    tickInside = tickInside+1
                if prevLine == 'b':
                    rssiOutside = int(line[1])
                    ticksOutside.insert(tickOutside, tickOutside)
                    rssiOutsideVals.insert(tickOutside, rssiOutside)
                    print ('%s,%d,%d') % (deviceID, tickOutside, rssiOutside)
                    outputFile.write(deviceID)
                    outputFile.write(',')
                    outputFile.write(str(rssiOutside))
                    outputFile.write('\n')
                    tickOutside = tickOutside+1

graphLayout = Layout(
    title = 'BlueHat RSSI Data - %sft.' % distance,
    titlefont = dict(
        family = 'verdana',
        size = 22,
        color = '#7F7F7F'
    ),
    xaxis = dict (
        autorange = True,
        showgrid = True,
        autotick = True,
        showline = True,
        title = 'Tick',
        titlefont = dict(
            family = 'verdana',
            size = 18,
            color = '#7F7F7F'
        )
    ),
    yaxis = dict (
        autorange = True,
        showgrid = True,
        autotick = True,
        showline = True,
        title = 'RSSI @ %sft.' % distance,
        titlefont = dict(
            family = 'verdana',
            size = 18,
            color = '#7F7F7F'
        )
    ),
    legend = dict (
        x = 0.7070486656200942,
        y = 1.1242331288343559,
    )
)

insideTrace = Scatter (
    x = ticksInside,
    y = rssiInsideVals,
    mode = 'lines+markers',
    name = 'Inside Hat',
    marker = Marker (
        size = 3,
        color = '#ff7f0e',
        symbol = 'circle-open',
        line = dict (
            width = 1.5
        )
    )
)

outsideTrace = Scatter (
    x = ticksOutside,
    y = rssiOutsideVals,
    mode = 'lines+markers',
    name = 'Outside Hat',
    marker = Marker (
        size = 3,
        color = '#1F77B4',
        symbol = 'circle-open',
        line = dict (
            width = 1.5
        )
    )
)

graphData = [insideTrace, outsideTrace]
graphFig = dict (data = graphData, layout = graphLayout)
py.plot(graphFig, filename = 'RSSI @ %sft.' % distance)
