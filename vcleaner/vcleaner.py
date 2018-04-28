#codeName: vcleaner.py
#Author: Dahir Muhammad Dahir
#Date: 26th-March-2018
#About: remove the "v" virus and rename the file that have been corrupted to
#       their orignal names

import os

thisDir = os.getcwd()

def vcleaner():
    print("Welcome\n")
    targetDir = thisDir
    targetExt = raw_input("Enter the extension type to search for:\n")
    #targetSize = raw_input("Enter target file size in bytes:\n")
    for root, dirs, files in os.walk(thisDir):
        for file in files:
            if file.endswith(targetExt) and os.path.exists(os.path.join(root, "v"+file)):
                os.remove(os.path.join(root, file))
                os.rename(os.path.join(root, "v"+file), os.path.join(root, file))
    print("Done...")


if __name__=="__main__":
    vcleaner()
