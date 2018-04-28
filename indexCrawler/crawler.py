#Date: 10th-March-2018
#Author: Dahir Muhammad Dahir
#About: this is supposed to be quick therefore it will be rough
#don't expect any clean code


import os
import requests
from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

projecDir = os.getcwd()
resumeFile = projecDir+"/resume.dmd"
beginFile = projecDir+"/begin.dmd"

newSubLinks = []

if not os.path.exists(projecDir+"/extensions.dmd"):
    with open(projecDir+"/extensions.dmd", "w") as f:
        pass

with open(projecDir+"/extensions.dmd", "r") as f:
    savedExtensions = f.readlines()

validExtension = []

if savedExtensions:
    for extension in savedExtensions:
        extension = extension.strip("\n")
        validExtension.append(extension)
else:
    extensions = raw_input("specify the file type to retrieve:\ne.g[.pdf, .html, .txt]\n")
    if extensions:
        with open(projecDir+"/extensions.dmd", "a") as f:
            extensions = extensions.strip(" ").split(",")
            for extension in extensions:
                extension = extension.strip(" ")
                validExtension.append(extension)
                f.write(extension+"\n")


def main():
    if not os.path.isfile(beginFile):
        with open(beginFile, "w") as f:
            pass
    if not os.path.isfile(resumeFile):
        with open(resumeFile, "w") as f:
            pass
    with open(resumeFile, "r") as f:
        address = f.readlines()
        if not address:
            with open(beginFile, "r") as s:
                address = f.readline()
                if not address:
                    address = raw_input("provide a valid address:\n")
                    with open(beginFile, "w") as f:
                        f.write(address)
                    crawler([address])
                    recurse()
                else:
                    crawler([address])
                    recurse()
        else:
            recurse()


def recurse():
    while(True):
        linkList = []
        with open(resumeFile, "r") as f:
            addresses = f.readlines()
        for link in addresses:
            link = link.strip("\n")
            linkList.append(link)
        if linkList:
            crawler(linkList)
        else:
            break


def crawler(addresses):
    if addresses:
        for link in addresses:
            getLinks(link)
        with open(resumeFile, "w") as f:
            for link in newSubLinks:
                f.write(link+"\n")
    else:
        print("Invalid address supplied...")

def getLinks(mainlink):
    with requests.Session() as s:
        page = s.get(mainlink, headers=headers)
    page = page.content
    soup = bs(str(page), "html.parser")
    cleanSoup = soup.prettify("utf8")
    soup = bs(cleanSoup, "html.parser")
    links = soup.find_all("a", attrs={"href":True})
    if links:
        for link in links:
            soup = bs(str(link), "html.parser")
            link = soup.a["href"].encode("utf8")
            validateLink(mainlink, link)


def validateLink(mainlink, link):
    if checkLinkIsFile(mainlink, link):
        pass
    else:
        checkLinkIsDir(mainlink, link)


def checkLinkIsDir(mainlink, link):
    fullLink = mainlink+link
    if link != "../":
        if link.endswith("/"):
            if not fullLink in newSubLinks:
                newSubLinks.append(fullLink)


def checkLinkIsFile(mainlink, link):
    for extension in validExtension:
        if link.endswith(extension):
            fileRetrieve(mainlink, link)
            return True
    return False


def fileRetrieve(mainlink, link):
    fullLink = mainlink+link
    initialDirectory = os.getcwd()
    with open(beginFile, "r") as f:
        domain = f.readline()
    directory = fullLink[len(domain):]
    directories = directory.split("/")[:-1]
    createDir(directories)
    os.chdir(initialDirectory)
    filename = getFileName(fullLink)
    if not os.path.isfile(os.getcwd()+"/"+directory):
        with requests.Session() as s:
            getFile = s.get(fullLink, headers=headers)
        newfile = getFile.content
        writeFile(newfile, filename, directory)


def writeFile(newfile, filename, directory):
    with open(os.getcwd()+"/"+directory, "wb") as f:
        f.write(newfile)
        print("Retrieved %s"%filename)

def createDir(directories):
    for dir in directories:
        if dir:
            if not os.path.isdir(os.getcwd()+"/"+dir):
                os.mkdir(os.getcwd()+"/"+dir)
                os.chdir(os.getcwd()+"/"+dir)

def getFileName(fullLink):
    filename = fullLink.split("/")[-1]
    return filename

if __name__=="__main__":
    main()
