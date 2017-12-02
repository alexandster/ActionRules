import csv

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

reader = csv.reader(open("../Data/Fragile States Index 2014.csv", 'rU'), dialect=csv.excel_tab)
num_row=0
attrDict = {}
for row in reader:
	values = row[0].split(",")
	if num_row==0:
		attributes = values
		del attributes[0]
		for attr in attributes:
			attrDict[attr] = []
	else:
		del values[0]
		for idx, attr in enumerate(attributes):
			if RepresentsInt(values[idx]):
				val = int(values[idx])
			else:
				val = values[idx]
			attrDict[attr].append(val)
	num_row+=1

uniqueValuesDict={}
for attrValues in attrDict:
	uniqueValuesDict[attrValues] = list(set(attrDict[attrValues]))
print uniqueValuesDict





