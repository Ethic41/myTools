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
	args = parser.parse_args()
	analyse(args.file, args.outfile, args.percentage)


def analyse(fileName, outfile, percent=None):
	if percent:
		percentage(fileName, outfile)

def percentage(fileName, outfile):
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
		percentDict[item] = str(percentage)+"%"

	with open(outfile, "ab") as f:
		for item in percentDict:
			f.write("%s ==> %s\n"%(item, percentDict[item]))



if __name__ == '__main__':
	main()
