#CodeName: analyse.py
#Author: Dahir Muhammad Dahir
#Date: 3rd-May-2018
#About: Performs different analysis on the content of a file

import os
import argparse


def main():
	parser = argparse.ArgumentParser(description="perform various analysis on a file eg [retrieving the parcentage of occurence of words]")
	parser.add_argument("file", help="Specify the input fileName")
	parser.add_argument("-P", "--percentage", help="retrieve the percentage occurence of each of the strings[per line] in the file", nargs="?", const=True)
	parser.add_argument("-f", "--outfile", help="file to write the output [default is 'analysed.dmd']", default="analysed.dmd")
	parser.add_argument("-M", "--max", help="return top of the number specified [eg -M 3 {top 3}]", type=int)
	parser.add_argument("-m", "--min", help="return least of the number specified [eg -m 4 {least 4}]", type=int)
	parser.add_argument("-U", "--unique", help="return unique list", nargs="?", const=True)
	args = parser.parse_args()
	analyse(args.file, args.outfile, args.percentage, args.max, args.min, args.unique)


def analyse(fileName, outfile, percent=None, maxi=None, mini=None, uniq=None):
	if percent:
		percentage(fileName, outfile)

	if maxi:
		percentDict = percentage(fileName, outfile, called=True)
		maximum(percentDict, maxi)

	if mini:
		percentDict = percentage(fileName, outfile, called=True)
		minimum(percentDict, mini)

	if uniq:
		percentDict = percentage(fileName, outfile, called=True)
		unique(percentDict)


def percentage(fileName, outfile, called=None):
	cleanLines = []
	with open(fileName, "r") as f:
		lines = f.readlines()

	for line in lines:
		line = line.strip("\n")
		cleanLines.append(line)

	numberOfLines = len(cleanLines)
	linesDict = {}

	for line in cleanLines:
		if not linesDict.has_key(line):
			linesDict[line] = 1
		else:
			linesDict[line] += 1

	percentDict = {}
	for item in linesDict:
		itemValue = linesDict[item]
		percentage = float(itemValue)/float(numberOfLines) * 100
		percentDict[item] = str("%.2f"%percentage)


	with open(outfile, "ab") as f:
		for item in percentDict:
			f.write("%s ==> %s%s\n"%(item, percentDict[item], "%"))

	if called:
		return percentDict


def maximum(percentDict, num):
	with open("top%d.dmd"%(num), "ab") as f:
		for i in range(num):
			maxVal = max(percentDict.values())
			lastMaxItem = ""
			for item in percentDict:
				if percentDict[item] == maxVal:
					f.write("%s ==> %s%s\n"%(item, maxVal, "%"))
					lastMaxItem = item
					break
			percentDict.pop(lastMaxItem)
	print("Done...")


def minimum(percentDict, num):
	with open("least%d.dmd"%(num), "ab") as f:
		for i in range(num):
			minVal = min(percentDict.values())
			lastMinItem = ""
			for item in percentDict:
				if percentDict[item] == minVal:
					f.write("%s ==> %s%s\n"%(item, minVal, "%"))
					lastMinItem = item
					break
			percentDict.pop(lastMinItem)
	print("Done...")


def unique(percentDict):
	with open("unique.dmd", "ab") as f:
		for item in percentDict:
			f.write(item+"\n")
	print("Done...")


if __name__ == '__main__':
	main()
