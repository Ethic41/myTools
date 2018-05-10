import re

pattern = re.compile(r"\s")

text = raw_input("Enter text:\n")
print(re.sub(pattern, "/*time*/", text))




#test
