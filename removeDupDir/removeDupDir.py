#CodeName: removeDupDir.py
#Author: Dahir Muhammad Dahir
#Date: 27th-May-2018
#About: removes duplicate empty dirs

import os

thisDir = os.getcwd()


def main():
	for dirpath, dirnames, filenames in os.walk(thisDir):
		for dir in dirnames:
			fullDir = os.path.join(dirpath, dir)
			if os.listdir(fullDir) == []:
				os.rmdir(fullDir)

		for filename in filenames:
			if os.path.isfile(os.path.join(dirpath, filename)):
				validFilename = os.path.splitext(filename)[0]
				length = len(validFilename)
				size = os.path.getsize(os.path.join(dirpath, filename))
				for file in filenames:
					if os.path.isfile(os.path.join(dirpath, file)):
						validFile = os.path.splitext(file)[0]
						curFileSize = os.path.getsize(os.path.join(dirpath, file))
						if validFile[:length] == validFilename and len(validFile) > length and curFileSize == size:
							os.remove(os.path.join(dirpath, file))
	print("Done...")



if __name__ == '__main__':
	main()
