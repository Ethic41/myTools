#codeName: indexMaker.py
#Author: Dahir Muhammad Dahir
#Date: 03rd-April-2018
#About: just make a file called index for the files in it's directory


import os

thisDir = os.getcwd()

def indexMaker():
    with open(thisDir+"/index.dmd", "a") as f:
        for dirpath, dirname, filenames in os.walk(thisDir):
            for filename in filenames:
                f.write(filename+"\n")
    print("Done...")


if __name__=="__main__":
    indexMaker()
