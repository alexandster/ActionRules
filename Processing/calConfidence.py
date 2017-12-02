def findIntersection(l1,l2):
	return list(set(l1)&set(l2))

def calConfidence(y1,y2,z1,z2):
	t1=1.0*len(findIntersection(y1,z1))/len(y1)
	t2=1.0*len(findIntersection(y2,z2))/len(y2)
	return t1*t2

################test
y1={'2','4'}
z1=['1','2','3','4','5','7']
y2=['1','6']
z2=['6']

print calConfidence(y1,y2,z1,z2)