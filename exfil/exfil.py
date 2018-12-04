#!/usr/bin/python3
#codeName: exfil.py
#Author: Dahir Muhammad Dahir
#Date: 04th-December-2018
#About: to for exfiltrating data through sql injection and
#       storing the data in a structured manner for later use

import os
import re
import requests
from string import digits, ascii_letters as letters
from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

thisDir = os.getcwd()
chars = digits + letters
shell_char = "\n\nroot@dmd:~# "
projectDir = thisDir+"/exfil_projects"
db_file = projectDir+"/databases.dmd"
tbl_file = projectDir+"/tables.dmd"
col_file = projectDir+"/columns.dmd"
row_file = projectDir+"/rows.dmd"

def main():
    initialize_projects_folder() # initialize projects director if not existing
    begin()


def initialize_projects_folder():
    if not os.path.isdir(projectDir):
        os.mkdir(projectDir)

        with open(db_file, "w") as f:
            pass
        
        with open(tbl_file, "w") as f:
            pass
        
        with open(col_file, "w") as f:
            pass
        
        with open(row_file, "w") as f:
            pass


def begin():
    while(True):
        task = input("Welcome, what would you like to do:\n[1]=> retrieve database name\n[2]=> retrieve table name\n[3]=> retrieve column name\n[4]=> retrieve row contents\n[5]=> auto pilot\n[6]=> quit%s"%(shell_char))
        
        if task == "1":
            retrieve_db_name()
        elif task == "2":
            retrieve_tbl_name()
        elif task == "3":
            retrieve_col_name()
        elif task == "4":
            retrieve_row_content()
        elif task == "5":
            auto_pilot()
        elif task == "6":
            exit()
        else:
            print("invalid input...please check your input!")


def retrieve_db_name():
    while(True):
        task = input("\n[1]=> show already retrieved database\n[2]=> retrieve new database name\n[3]=> back to previous menu%s"%(shell_char))
        if task == "1":
            show_database()
        elif task == "2":
            retrieve_new_db_name()
        elif task == "3":
            break
        else:
            print("invalid input...")


def show_database():
    with open(db_file, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        print(line.strip("\n"))


def retrieve_new_db_name():
    pre_column_name = "DISTINCT"
    column_name = "table_schema"
    from_where = "information_schema.tables"
    condition = "where table_schema not like '%_schema' and table_schema != 'mysql'"


def retrieve_tbl_name():
    pass


def retrieve_col_name():
    pass


def retrieve_row_content():
    pass


def auto_pilot():
    pass


def queryDB():
    pass

