from .operator_factory import operation

@operation
def H(i, o):
    return o.H(i)
@operation
def Z(i, o):
    return o.Z(i)
@operation
def Y(i, o):
    return o.Y(i)
@operation
def I(i, o):
    return o.I(i)
@operation
def X(i, o):
    return o.X(i)
@operation
def NOT(i, o):
    return o.NOT(i)

@operation
def CNOT(i, j, o):
    return o.CNOT(i, j)
@operation
def CX(i, j, o):
    return o.CNOT(i, j)

@operation
def u3(i, theta, phi, lam, o):
    return o.u2(i, theta, phi, lam)
@operation
def u2(i, phi, lam, o):
    return o.u2(i, phi, lam)
@operation
def u1(i, lam, o):
    return o.u1(i, lam)

@operation
def S(i, o):
    return o.S(i)

@operation
def Sdg(i, o):
    return o.Sdg(i)
@operation
def T(i, o):
    return o.T(i)
@operation
def Tdg(i, o):
    return o.Tdg(i)

@operation
def Rx(i, theta, o):
    return o.Rx(i, theta)
@operation
def Ry(i, theta, o):
    return o.Ry(i, theta)
@operation
def Rz(i, theta, o):
    return o.Rz(i, theta)
