import csv
import itertools

# Function to test if the string is an integer
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Function to get all combinations for the notations of a flexible attribute
def notation_flexible(inList):
	outList = []
	for i in inList:
	    for j in inList:
	        inter = []
	        outList.append((i,j))
	return outList

# Function to get all combinations for the notations of a stable attribute
def notation_stable(inList):
	outList = []
	for i in inList:
	        inter = []
	        outList.append((i,i))
	return outList

# Function to find the example numbers of notations for a specific attribute
# Output: list of examples indexes
def notation2examples(notation, attr):
	examples=[]
	for idx, eachValue in enumerate(attrDict[attr]):
		if eachValue==notation:
			examples.append(idx+1)
	return examples

# Function to find intersections between two lists
def findIntersection(l1,l2):
	return list(set(l1)&set(l2))

# Function to test whether the 
def testMark(exampleNote1, exampleNote2):
	# Find intersections between the flexible attribute and the action attribute
	intersectionLeft = findIntersection(exampleNote1, d1Set)
	intersectionRight = findIntersection(exampleNote2, d2Set)
	# Calculate the support using the intersection
	supportLeft = len(intersectionLeft)
	supportRight = len(intersectionRight)
	if supportRight==0 or supportLeft==0:
		return -1
	support = max(supportLeft, supportRight)
	# Calculate the confidence
	confidenceLeft = float(supportLeft/float(len(exampleNote1)))
	confidenceRight = float(supportRight/float(len(exampleNote2)))
	confidence = float(confidenceLeft*confidenceRight)
	if support>=THsup:
		if confidence>=THconf:
			return 1
		elif confidence==0:
			return -1
		else:
			return 0
	else:
		return -1

def levelOne():
	positiveNotations=[]
	unmarkedNotations=[]
	negativeNotations=[]
	for attrValues in attrDict:
		# Unique values of each atttribute
		uniqueValuesDict[attrValues] = list(set(attrDict[attrValues]))
		# Generate notations for stable attributes, which are between each value and itself
		if attrValues in stable_attr:
			attrNotations = notation_stable(uniqueValuesDict[attrValues])
		# Generate notations for flexible attributes, which are between all values and each other
		else:
			attrNotations = notation_flexible(uniqueValuesDict[attrValues])
		# For each combination
		for note in attrNotations:
			# Find example indeces for the combination of the right and left sets, which are the same
			exampleNote1 = notation2examples(note[0], attrValues)
			# If the attribute is stable the transition of attribute is between iteself
			if attrValues in stable_attr:
				exampleNote2 = exampleNote1
			# If the attribute is flexible the transition of attribute is between the combinations of different values
			else:
				exampleNote2 = notation2examples(note[1], attrValues)
			# Store the attribute in order to extract it for listing all rules at the end
			exampleNote3 = [attrValues]
			# Store the transition (change) of values in order to extract it for listing all rules at the end
			exampleNote4 = [note]
			noteMark = testMark(exampleNote1, exampleNote2)
			if noteMark==0:
				unmarkedNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4))
			elif noteMark>0:
				positiveNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4))
			elif noteMark<0:
				negativeNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4))
	return (positiveNotations, unmarkedNotations, negativeNotations)

def nextLevel(unmarkedNotations):
	combUnmarkedNotations = list(itertools.combinations(unmarkedNotations, 2))
	positiveNotations=[]
	unmarkedNotations=[]
	negativeNotations=[]
	for eachComb in combUnmarkedNotations:
		exampleNote1 = list(set(eachComb[0][0]) & set(eachComb[1][0]))
		exampleNote2 = list(set(eachComb[0][1]) & set(eachComb[1][1]))
		exampleNote3 = eachComb[0][2] + eachComb[1][2]
		exampleNote4 = eachComb[0][3] + eachComb[1][3]
		noteMark = testMark(exampleNote1, exampleNote2)
		if noteMark==0:
			unmarkedNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4))
		elif noteMark>0:
			positiveNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4))
		elif noteMark<0:
			negativeNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4))
	return (positiveNotations, unmarkedNotations, negativeNotations)

# Stable attributes
stable_attr = ["Fragile States Index 2014", "Neighbors with Equal or Lesser Stability", "Population (millions)"]

# Open the file and read
reader = csv.reader(open("Data/Fragile States Index 2014.csv", 'rU'), dialect=csv.excel_tab)
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
			# Test if the string is an integer
			if RepresentsInt(values[idx]):
				val = int(values[idx])
			else:
				val = values[idx]
			attrDict[attr].append(val)
	num_row+=1

# Get decision attribute's set of examples first
decision1="Alert"
decision2="Sustainable"
decisionAttribute="Status"
d1Set = notation2examples(decision1, decisionAttribute)
d2Set = notation2examples(decision2, decisionAttribute)

# Threshold support and confidence
THsup=3.0
THconf=0.25		# Must be in decimal format

uniqueValuesDict={}
level=1
# Get the positively and negatively marked, and unmarked for the first level
(positiveNotations, unmarkedNotations, negativeNotations) = levelOne()
print "level", level

rules=[]
# Gather rules in one array
for eachrule in positiveNotations:
	rules.append((eachrule[2], eachrule[3]))

prevNumNotations = len(unmarkedNotations)
saturationFlag=0
# Get the positively and negatively marked, and unmarked for all next levels
# Keep looping until there are no more unmarked notations or the unmarked notations are saturated
while (unmarkedNotations!=[]):
	level+=1
	print "level", level
	(positiveNotations, unmarkedNotations, negativeNotations) = nextLevel(unmarkedNotations)
	# Gather rules in one array
	for eachrule in positiveNotations:
		rules.append((eachrule[2], eachrule[3]))
	if prevNumNotations<=len(unmarkedNotations):
		if saturationFlag==0:
			saturationFlag=1
		else:
			print "Saturated: the unmarked notations will stay the same forever"
			break
	prevNumNotations = len(unmarkedNotations)

print "rules", rules
print "len(rules)", len(rules)

# The unmarked notations saturate and the while loop keeps repeating till infinity >> address this case in the report
# This happens when the support & confidence thresholds are too low like supth=5 & confth=0.25, therefore, we made a saturation check
# This case is avoided by stopping the loop when saturation happens using saturation flag and the comparing the previous number of unmarked notations with the current one

