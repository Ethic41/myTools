
items = [1, 2, 2, 3, 5, 2, 3, 3, 4, 6]
itemsDict = {}

for item in items:
    if not itemsDict.has_key(item):
        itemsDict[item] = 1
    else:
        itemsDict[item] += 1

for items in itemsDict:
    print(itemsDict[items])
