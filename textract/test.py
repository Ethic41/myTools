import os
import csv
import re
"""
with open("eggs.csv", "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Spam"]*5 + ["BakedBeans"])
    writer.writerow(["Time"]*6)
"""
"""
with open("eggs.csv", "rb") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
"""
"""
with open("neweggs.csv", "wb") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["time"]*5)
    writer.writerow(["onething"]*5)
"""
#fourDigit = re.compile(r"\b\d{4}\b")
#fourDigitWithSpace = re.compile(r"\b\d{4}\b\s{1,2}")
Date = re.compile(r"\b\d{4}\b\s{1,2}[A-Z]{1,1}[a-z]{2,2}\s{1,2}\d{1,2}")
#if yearAndMonth.match("2011 Dec 11"):
#    print("yes")
firstParam = re.compile(r"\b4-character ID")
lastParam = re.compile(r"\bSUM\s{1,2}\d{1,2}\d{1,2}\s{1,2}\d{1,2}")
mean12Param = re.compile(r"\bmean\s{1,2}MP12\s{1,2}rms")
mean21Param = re.compile(r"\bmean\s{1,2}MP21\s{1,2}rms")



"""

with open("data.txt", "rb") as f:
    lines = f.readlines()


readLines = []
for line in lines:
    line = line.strip("\n")
    readLines.append(line)

for line in readLines:
    if lastParam.match(line):
        print(line)
"""
"""
for line in readLines:
    if Date.match(line):
        print(readLines.index(line))

"""

def csvify(completeFile, fileName):
    with open(fileName+".csv", "wb") as f:
        writer = csv.writer(f)
        for line in completeFile[:-2]:
            line = line.split(":",1)
            writer.writerow(line)
        writer.writerow(["first epoch", "last epoch", "hrs", "dt", "#expt", "#have", "%", "mp1", "mp2", "o/slps"])
        line = completeFile[-1]
        writer.writerow([line[4:19], line[19:34], line[34:41], line[41:45], line[48], line[52:59], line[59], line[63:69], line[69:76], line[77:81]])



def extract():
    with open("data.txt", "rb") as f:
        lines = f.readlines()

    readLines = []
    for line in lines:
        line = line.strip("\n")
        readLines.append(line)

    dateLineIndexes = []
    for line in readLines:
        if Date.match(line):
            dateLineIndexes.append(readLines.index(line))

    firstParamLineIndexes = []
    lastParamLineIndexes = []
    mp12ParamIndexes = []
    mp21ParamIndexes = []
    for index in dateLineIndexes:
        fileName = readLines[index][:12]
        for line in readLines[index:]:
            if firstParam.match(line):
                firstParamLineIndexes.append(index + readLines[index:].index(line))
            if lastParam.match(line):
                lastParamLineIndexes.append(index + readLines[index:].index(line))
                break

        for line in readLines[index:]:
            if mean12Param.match(line):
                mp12ParamIndexes.append(index + readLines[index:].index(line))
            if mean21Param.match(line):
                mp21ParamIndexes.append(index + readLines[index:].index(line))
                break

        firstPartIndex = zip(firstParamLineIndexes, lastParamLineIndexes)
        secondPartIndex = zip(mp12ParamIndexes, mp21ParamIndexes)

        firstPart = []
        secondPart = []
        thirdPart = []
        lastPart = []

        for index in firstPartIndex:
            for line in readLines[index[0]:index[1]-1]:
                firstPart.append(line)
            firstPart.append("\r")
            firstPart.append("\r")

        for index in secondPartIndex:
            for line in readLines[index[0]:index[0]+5]:
                secondPart.append(line)
            secondPart.append("\r")
            secondPart.append("\r")

            for line in readLines[index[1]:index[1]+5]:
                thirdPart.append(line)
            thirdPart.append("\r")
            thirdPart.append("\r")

        for index in firstPartIndex:
            lastPart.append(readLines[index[1]-1])
            lastPart.append(readLines[index[1]])

        completeFile = []
        for content in firstPart:
            completeFile.append(content)

        for content in secondPart:
            completeFile.append(content)

        for content in thirdPart:
            completeFile.append(content)

        for content in lastPart:
            completeFile.append(content)

        csvify(completeFile, fileName)

        firstPart = []
        secondPart = []
        thirdPart = []
        lastPart = []

        firstParamLineIndexes = []
        lastParamLineIndexes = []
        mp12ParamIndexes = []
        mp21ParamIndexes = []

        break


extract()

















#
