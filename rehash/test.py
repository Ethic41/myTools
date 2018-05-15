
import re
from bs4 import BeautifulSoup as bs

hashPattern = re.compile(r"staff\.php\?id=")

soup = bs(open("/root/Documents/baze.html"), "html.parser")
clean = soup.prettify("utf8")
soup = bs(clean, "html.parser")

divs = soup.find_all("a", attrs={"href":hashPattern})
for div in divs:
    soup = bs(str(div), "html.parser")
    string = soup.find("a").string
    print(string.strip("\n").strip(" ").strip("\n").strip("\n"))
