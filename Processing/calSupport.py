def findIntersection(l1,l2):
	return list(set(l1)&set(l2))

def calSupport(y1,y2,z1,z2):
	card1=len(findIntersection(y1,z1))
	card2=len(findIntersection(y2,z2))
	return min(card1,card2)

################test
y1={'2','4'}
z1=['1','2','3','4','5','7']
y2=['1','6']
z2=['6']

print calSupport(y1,y2,z1,z2)
