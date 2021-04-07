
def and_gate(a,b):
        if(a == None or b == None):
                print('No input specified')
        return (a and b)
def or_gate(a,b):
	return (a or b)
def not_gate(a):
	if(not(a)==True):
		return 1
	else:
		return 0
def nand_gate(a,b):
	if(not(a and b)==True):
		return 1
	else:
		return 0
def nor_gate(a,b):
	if(not(a or b)==True):
		return 1
	else:
		return 0
def xnor_gate(a,b):
	if(not(a ^ b)==True):
		return 1
	else:
		return 0
def xor_gate(a,b):
	return (a ^ b)
def half_adder(a,b):
	sum_1 = a^b
	carry = a and b
	return (sum_1,carry)
def full_adder(a,b,cin):
	sum_1 = a^b^cin
	carry = ((a and b) or(cin and (a^b)))
	return (sum_1,carry)
