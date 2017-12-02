inList = ["a1","a2","a3"]
outList = []

for i in inList:
    for j in inList:
        inter = []
        inter.append([i,j])
        outList.append(inter)
print(outList)
