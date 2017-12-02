import csv
import itertools
import web
import cgi  
import HTMLParser
import collections

#connect to GUI
urls = (
  '/', 'index'
)

#call render
app = web.application(urls, globals())
render = web.template.render('GUI/')

#global variables with default attributes
global supp
global conf
global decisionTo
global decisionFrom
global rules
global h
supp = 6.0
conf = 0.15
decisionTo = "Alert"
decisionFrom = "Sustainable"
rules = "Please make sure you adhered to the following guidelines: <br/> 1) Your confidence and support is in whole number or decimal format. FRACTIONS ARE NOT ACCEPTED. <br/> 2) Your confidence is between 0 and 1, with 0 being 0 percent and 1 being 100 percent <br/> 3) There are no symbols or letters in your specifications."
# Stable attributes
stable_attr = ["Fragile States Index 2014", "Neighbors with Equal or Lesser Stability", "Population (millions)"]
# Open the file and read
reader = csv.reader(open("Data/Fragile States Index 2014.csv", 'rU'), dialect=csv.excel_tab)
d1set = []
d2Set = []
attrDict = {}
uniqueValuesDict={}
h = HTMLParser.HTMLParser()
#class for GUI page
class index:
    def GET(self):

		form = web.input(minSup="6.0", minConf="0.15", mapTo="Alert", mapFrom="Sustainable", rules = "none")
		sup  = "%s" % (form.minSup)
		con =  "%s" % (form.minConf)
		to  = "%s" % (form.mapTo)
		mapfrom = "%s" % (form.mapFrom)
		rules = "Please make sure you adhered to the following guidelines: <br/> 1) Your confidence and support is in whole number or decimal format. FRACTIONS ARE NOT ACCEPTED. <br/> 2) Your confidence is between 0 and 1, with 0 being 0 percent and 1 being 100 percent <br/> 3) There are no symbols or letters in your specifications."
		#rules="hello <br> world"
		
		ruleSet = []

		try:
			sup = float(sup)
			con = float(con)
			if(con > 1):
				return render.index(sup, con, to, mapfrom, rules)
				#return(rules)
			if(con < 0):
				return render.index(sup, con, to, mapfrom, rules)
				#return(rules)
			if(sup < 0):
				return render.index(sup, con, to, mapfrom, rules)
				#return(rules)
		except ValueError:
			return render.index(sup, con, to, mapfrom, rules)
			#return(rules)

		setSupport(float(sup))
		setConfidence(float(con))
		setTo(to)
		setFrom(mapfrom)

		ruleSet = start()
		rul3 =  str(ruleSet)[1:-1].strip('()')#rul = ' '.join(ruleSet)
		rul3 = rul3.replace('"', '').replace(',,','')
		rules = rul3

		
		#return render.index(rules)
		return render.index(sup, con, to, mapfrom, rules)

#runs app
if __name__ == "__main__":
	app.run()

#sets support threshold from user entry
def setSupport(sup1):
	global supp
	supp = sup1
	
#sets confidence threshold from user entry
def setConfidence(con1):
	global conf
	conf = con1
	
#sets decision map-to from user entry
def setTo(to1):
	global decisionTo
	decisionTo = to1
	
#sets decision map-from from user entry
def setFrom(mfrom1):
	global decisionFrom
	decisionFrom = mfrom1

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
	global attrDict
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
		return (-1, 0, 0)
	support = max(supportLeft, supportRight)
	# Calculate the confidence
	confidenceLeft = float(supportLeft/float(len(exampleNote1)))
	confidenceRight = float(supportRight/float(len(exampleNote2)))
	confidence = float(confidenceLeft*confidenceRight)
	if support>=THsup:
		if confidence>=THconf:
			return (1, support, confidence)
		elif confidence==0:
			return (-1, support, confidence)
		else:
			return (0, support, confidence)
	else:
		return (-1, support, confidence)

def levelOne():
	positiveNotations=[]
	unmarkedNotations=[]
	negativeNotations=[]
	for attrValues in attrDict:
		# Unique values of each atttribute
		global uniqueValuesDict
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
			(noteMark, support, confidence) = testMark(exampleNote1, exampleNote2)
			exampleNote5 = support
			exampleNote6 = confidence
			if noteMark==0:
				unmarkedNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4, exampleNote5, exampleNote6))
			elif noteMark>0:
				positiveNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4, exampleNote5, exampleNote6))
			elif noteMark<0:
				negativeNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4, exampleNote5, exampleNote6))
	return (positiveNotations, unmarkedNotations, negativeNotations)

def nextLevel(unmarkedNotations):
	combUnmarkedNotations = list(itertools.combinations(unmarkedNotations, 2))
	positiveNotations=[]
	unmarkedNotations=[]
	negativeNotations=[]
	for eachComb in combUnmarkedNotations:
		exampleNote1 = list(set(eachComb[0][0]) & set(eachComb[1][0]))
		exampleNote2 = list(set(eachComb[0][1]) & set(eachComb[1][1]))
		# str3 = "Attribute: " +  str(eachComb[0][2]) + str(eachComb[1][2])
		# str4 = "From " + str(eachComb[0][3]) + " to " + str(eachComb[1][3])
		exampleNote3 = eachComb[0][2] + eachComb[1][2]
		exampleNote4 = eachComb[0][3] + eachComb[1][3]
		# exampleNote3 = str3
		# exampleNote4 = str4
		(noteMark, support, confidence) = testMark(exampleNote1, exampleNote2)
		exampleNote5 = support
		exampleNote6 = confidence
		if noteMark==0:
			unmarkedNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4, exampleNote5, exampleNote6))
		elif noteMark>0:
			# str3 = "Attribute " + str(exampleNote1)
			# str4 = "From " + str(exampleNote2)
			# str5 = "To " + str(exampleNote3)
			#positiveNotations.append((str3, str4, str5, exampleNote4))
			positiveNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4, exampleNote5, exampleNote6))
		elif noteMark<0:
			negativeNotations.append((exampleNote1, exampleNote2, exampleNote3, exampleNote4, exampleNote5, exampleNote6))
	return (positiveNotations, unmarkedNotations, negativeNotations)

def start():
	num_row=0
	
	#Read data into array
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
	global decision1
	global decision2
	decision1=decisionTo
	decision2=decisionFrom
	decisionAttribute="Status"
	global d1Set
	global d2Set
	d1Set = notation2examples(decision1, decisionAttribute)
	d2Set = notation2examples(decision2, decisionAttribute)

	# Threshold support and confidence

	global THsup
	global THconf
	
	THsup=supp
	THconf=conf
	print "Sup:", THsup
	print "Con:", THconf

	level=1
	# Get the positively and negatively marked, and unmarked for the first level
	(positiveNotations, unmarkedNotations, negativeNotations) = levelOne()
	print "level", level

	rules=[]
	newRules=[]
	# Gather rules in one array
	for eachrule in positiveNotations:
		str1 = "<span>RULE - </span>" + "<b>Attribute: </b>" + str(eachrule[2]).strip('[]').strip('()').strip(',')
		str2 = "<b>From-to: </b>" + str(eachrule[3]).strip('[]') 
		str8 = "<b>Support: </b>" + str(eachrule[4]).strip('[]').strip('()').strip(',')
		str9 = "<b>Confidence: </b>" + str(eachrule[5]).strip('[]').strip('()').strip(',')
 		str13 = str1 + '&nbsp&nbsp' + str2 + '&nbsp&nbsp' + str8 + '&nbsp&nbsp' + str9 + '<br />' + ","
 		 
 		rules.append(str13)

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
			attributesRule = eachrule[2]
			valueRule = eachrule[3]
			supportRule = eachrule[4]
			confidenceRule = eachrule[5]
			
			# Filter repeating attributes which also has the same value change
			repeatedAttr = [item for item, count in collections.Counter(attributesRule).items() if count > 1]
			for eachRepeated in repeatedAttr:
				repeatedIndex = attributesRule.index(eachRepeated)
				del attributesRule[repeatedIndex]
				del valueRule[repeatedIndex]
			str5 = "<span>RULE - </span>"+ "<b>Attribute: </b>" + str(attributesRule).strip('[]').strip('()').strip(',')
			str6 = "<b>From-to: </b>" + str(valueRule).strip('[]')
			str10 = "<b>Support: </b>" + str(supportRule).strip('[]').strip('()').strip(',')
			str11 = "<b>Confidence:</b> " + str(confidenceRule).strip('[]').strip('()').strip(',')
			str12 = str5 + '&nbsp&nbsp' + str6 + '&nbsp&nbsp' + str10 + '&nbsp&nbsp' + str11 + '<br />' + ","
			rules.append(str12)

		if prevNumNotations<=len(unmarkedNotations):
			if saturationFlag==0:
				saturationFlag=1
			else:
				print "Saturated: the unmarked notations will stay the same forever"
				break
		prevNumNotations = len(unmarkedNotations)


	for rule in rules: 
		rul2 = str(rule)
		print rul2.strip('[]').strip('()')
			
	print "len(rules)", len(rules)
	
	return rules
	# The unmarked notations saturate and the while loop keeps repeating till infinity >> address this case in the report
	# This happens when the support & confidence thresholds are too low like supth=5 & confth=0.25, therefore, we made a saturation check
	# This case is avoided by stopping the loop when saturation happens using saturation flag and the comparing the previous number of unmarked notations with the current one

