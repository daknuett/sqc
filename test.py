from operator_factory import operation
import sqc

@operation
def NOT(bit_to_act, o):
	return o.NOT(bit_to_act)

@operation
def H(bit_to_act, o):
	return o.H(bit_to_act)

Nbits = 3

state = sqc.state(Nbits, basis=[ "|%d>|%d>" % (i%2,i//2) for i in range(4) ])
one = sqc.operator(Nbits)

print(one @ NOT(1) * state)
print(one @ NOT(0) * state)
print(one @ NOT(1) @ NOT(1) * state)

print(one @ NOT(1) @ H(1) @ H(0) * state)
print(one.NOT(1).H(1).H(0) * state)
