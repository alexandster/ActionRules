def unmarkDecision(minS,minC,S,C):
	NEGATIVE=-1
	POSITIVE=1
	UNMARK=0

	if C==0:
		return NEGATIVE
	elif S<minS:
		return NEGATIVE
	elif S>=minS and C>=minC:
		return POSITIVE
	elif (S>=minS and C<minC) or (S<minS and C>=minC):
		return UNMARK
