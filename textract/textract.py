#codeName: textract.py
#Author: Dahir Muhammad Dahir
#Date: 26th-April-2018
#About: extract text to csv file


import os
import csv
import re

thisDir = os.getcwd()

Date = re.compile(r"\b\d{4}\b\s{1,2}[A-Z]{1,1}[a-z]{2,2}\s{1,2}\d{1,2}")
firstParam = re.compile(r"\b4-character ID")
lastParam = re.compile(r"\bSUM\s{1,2}\d{1,2}\d{1,2}\s{1,2}\d{1,2}")
mean12Param = re.compile(r"\bmean\s{1,2}MP12\s{1,2}rms")
mean21Param = re.compile(r"\bmean\s{1,2}MP21\s{1,2}rms")

def main():
    try:
        while(True):
            print("Welcome:\nThis Program allow you to extract text from file and save it to csv format\nNote: You can always use [Control-C] to 'quit' at any point in the program")
            mode = raw_input("Choose mode:\n[1] ==> Auto {in this mode files will be automatically discovered and converted}\n[2] ==> Manual {Choose the files you want to convert}\n[3] ==> Extract specific parameter\n[4] ==> exit\n\n")
            if mode == "1":
                auto()
                print("Completed Successfully...")
                break
            elif mode == "2":
                manual()
                print("Completed Successfully...")
                break
            elif mode == "3":
                extractSpecificParam()
                print("Completed Successfully")
                break
            elif mode == "4":
                print("GoodBye!")
                exit()
            else:
                print("Invalid Input please check you input\n\n")
    except KeyboardInterrupt as e:
        print("Shutting Down...GoodBye...")
        exit()
    except Exception as e:
        error(e)
        exit()


def auto():
    try:
        currentDirList = os.listdir(thisDir)
        files = []
        for item in currentDirList:
            if os.path.isfile(thisDir+"/"+item):
                if item.endswith(".txt"):
                    files.append(item)

        for file in files:
            extract(file)
    except Exception as e:
        error(e)




def manual(paramName=None, mode=None, month=None, year=None):
    try:
        currentDirList = os.listdir(thisDir)
        files = []
        for item in currentDirList:
            if os.path.isfile(thisDir+"/"+item):
                if item.endswith(".txt"):
                    files.append(item)
        i = 1
        for file in files:
            print("\n[%d] ==> %s"%(i, file))
            i += 1

        choices = raw_input("Choose one or more of the file above in the form {1,2,3}:\n\n")
        choices = choices.split(",")

        chosenList = []
        for choice in choices:
            choice = int(choice) - 1
            chosenList.append(files[choice])

        for file in chosenList:
            extract(file, paramName=paramName, mode=mode, month=month, year=year)
    except Exception as e:
        error(e)


def extractSpecificParam():
    paramName = raw_input("\nSpecify the parameter to extract:\n\n")
    if paramName:
        mode = raw_input("\nChoose mode:\n[1] ==> Extract all Chosen parameters to single file\n[2] ==> Extract Chosen parameter on monthly basis\n[3] ==> Extract Chosen parameter on Annual basis\n[4] ==> exit\n\n")
        if mode:
            if mode == "1":
                manual(paramName=paramName, mode="all")
            elif mode == "2":
                monthMap = {"1":"Jan", "2":"Feb", "3":"Mar", "4":"Apr", "5":"May", "6":"Jun", "7":"Jul", "8":"Aug", "9":"Sep", "10":"Oct", "11":"Nov", "12":"Dec", "13":"All"}
                month = raw_input("specify a month:\n[1] == Jan\n[2] ==> Feb\n[3] ==> Mar\n[4] ==> Apr\n[5] ==> May\n[6] ==> Jun\n[7] == Jul\n[8] ==> Aug\n[9] ==> Sep\n[10] ==> Oct\n[11] ==> Nov\n[12] ==> Dec\n[13] ==> All\n\n\n")
                month = monthMap[month]
                year = raw_input("specify year:\n")
                if month and year:
                    manual(paramName=paramName, mode="monthly", month=month, year=year)
            elif mode == "3":
                year = raw_input("specify year:\n")
                if year:
                    manual(paramName=paramName, mode="yearly", year=year)
            elif mode == "4":
                exit()

def extract(file, paramName=None, mode=None, month=None, year=None):
    try:
        #open the file for reading
        with open(thisDir+"/"+file, "rb") as f:
            lines = f.readlines()

        #reading the file into a list line by line
        readLines = []
        for line in lines:
            line = line.strip("\n")
            readLines.append(line)

        #extracting the lines with date in the format of the file
        dateLineIndexes = []
        for line in readLines:
            if Date.match(line):
                dateLineIndexes.append(readLines.index(line))

        #list to hold various index of the parameters to be filtered in the file
        firstParamLineIndexes = []
        lastParamLineIndexes = []
        mp12ParamIndexes = []
        mp21ParamIndexes = []

        #looping through the date indexes that will serve as beginings for file extraction
        for index in dateLineIndexes:
            fileName = file[:-4]+"_"+readLines[index][:12] #the date is used as the csv file name

            #Matching the first and last parameters and storing their indexes for future use
            for line in readLines[index:]:
                if firstParam.match(line):
                    firstParamLineIndexes.append(index + readLines[index:].index(line))
                if lastParam.match(line):
                    lastParamLineIndexes.append(index + readLines[index:].index(line))
                    break

            #Matching the mean parameter values and storing for future use
            for line in readLines[index:]:
                if mean12Param.match(line):
                    mp12ParamIndexes.append(index + readLines[index:].index(line))
                if mean21Param.match(line):
                    mp21ParamIndexes.append(index + readLines[index:].index(line))
                    break

            #Zipping indexes together for use in text extraction
            firstPartIndex = zip(firstParamLineIndexes, lastParamLineIndexes)
            secondPartIndex = zip(mp12ParamIndexes, mp21ParamIndexes)

            #Declaring lists for storing various parts of the text b4 merge
            firstPart = []
            secondPart = []
            thirdPart = []
            lastPart = []

            #Appending various text parts to their corresponding list
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

            completeFile = []       #list for holding complete text

            #Combing the various part to the holding list
            for content in firstPart:
                completeFile.append(content)

            for content in secondPart:
                completeFile.append(content)

            for content in thirdPart:
                completeFile.append(content)

            for content in lastPart:
                completeFile.append(content)

            #calling the function to save the file in csv
            if not paramName:
                csvify(completeFile, fileName)
            elif mode=="all":
                extractParam(completeFile, fileName, paramName, mode="all")
            elif mode == "monthly":
                extractParam(completeFile, fileName, paramName, mode="monthly", month=month, year=year)
            elif mode == "yearly":
                extractParam(completeFile, fileName, paramName, mode="yearly", year=year)

            #Emptying the list in preparation for the next iteration
            firstPart = []
            secondPart = []
            thirdPart = []
            lastPart = []

            firstParamLineIndexes = []
            lastParamLineIndexes = []
            mp12ParamIndexes = []
            mp21ParamIndexes = []
    except Exception as e:
        error(e)


def extractParam(completeFile, fileName, paramName, mode=None, month="All", year=None):

    if not os.path.exists(thisDir+"/converted"):
        os.mkdir(thisDir+"/converted")


    if mode == "monthly":
        dayDate = fileName[10:]
        date = fileName[10:18]
        currentYear = date[:4]
        currentMonth = date[5:8]
        if month == "All":
            currentMonth = "All"
        for line in completeFile[:-2]:
            line = line.split(":", 1)
            if line[0].strip(" ") == paramName.strip(" "):
                if year == currentYear and month == currentMonth:
                    if not os.path.exists(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+date+"_"+paramName)):
                        with open(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+date+"_"+paramName), "ab") as f:
                            writer = csv.writer(f)
                            writer.writerow((dayDate, line[1]))
                    else:
                        with open(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+date+"_"+paramName), "ab") as f:
                            writer = csv.writer(f)
                            if year == currentYear and month == currentMonth:
                                writer.writerow((dayDate, line[1]))
                    break


    elif mode == "yearly":
        dayDate = fileName[10:]
        date = fileName[10:18]
        currentYear = date[:4]
        currentMonth = date[5:8]
        for line in completeFile[:-2]:
            line = line.split(":", 1)
            if line[0].strip(" ") == paramName.strip(" "):
                if year == currentYear:
                    if not os.path.exists(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+year+"_"+paramName)):
                        with open(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+year+"_"+paramName), "ab") as f:
                            writer = csv.writer(f)
                            writer.writerow((dayDate, line[1]))
                    else:
                        with open(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+year+"_"+paramName), "ab") as f:
                            writer = csv.writer(f)
                            writer.writerow((dayDate, line[1]))
                    break
    elif mode == "all":
        dayDate = fileName[10:]
        date = fileName[10:18]
        currentYear = date[:4]
        currentMonth = date[5:8]
        for line in completeFile[:-2]:
            line = line.split(":", 1)
            if line[0].strip(" ") == paramName.strip(" "):
                if not os.path.exists(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+paramName+"_all")):
                    with open(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+paramName+"_all"), "ab") as f:
                        writer = csv.writer(f)
                        writer.writerow((dayDate, line[1]))
                else:
                    with open(thisDir+"/converted/%s.csv"%(fileName[:4]+"_"+paramName+"_all"), "ab") as f:
                        writer = csv.writer(f)
                        writer.writerow((dayDate, line[1]))
                break


def csvify(completeFile, fileName):
    try:
        if not os.path.exists(thisDir+"/converted"):
            os.mkdir(thisDir+"/converted")
        convertedDir = thisDir+"/converted"
        with open(convertedDir+"/"+fileName+".csv", "wb") as f:
            writer = csv.writer(f)
            for line in completeFile[:-2]:
                line = line.split(":",1)
                writer.writerow(line)
            writer.writerow(["first epoch", "last epoch", "hrs", "dt", "#expt", "#have", "%", "mp1", "mp2", "o/slps"])
            line = completeFile[-1]
            writer.writerow([line[4:19], line[19:34], line[34:41], line[41:45], line[48], line[52:59], line[59], line[63:69], line[69:76], line[76:81]])
    except Exception as e:
        error(e)

def error(e):
    print(e)
    print("Shutting Down...GoodBye...")


if __name__=="__main__":
    main()
#End
