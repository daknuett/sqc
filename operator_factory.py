# FIXME:
# This is just for testing. Move it into sqc for later
# usage and use relative imports then!
from sqc.operator import operator
from sqc.state import state

from inspect import signature


class operator_factory_spawner(object):
    def __init__(self, operation):
        self._argument_count = len(signature(operation).parameters)
        if(self._argument_count == 0):
            raise ValueError("operation is missing parameter 'operator'")
        self._operation = operation

    def __rmatmul__(self, other):
        if(isinstance(other, operator)):
            return self.make_operator(other)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __mul__(self, other):
        if(isinstance(other, state)):
            nbits = other.nbits
            op = operator(nbits)

            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_factory and '{}'".format(type(other)))

    def make_operator(self, op):
        if(self._argument_count != 1):
            raise ValueError("operation requires arguments")
        return self._operation(op)

    def __call__(self, *args):
        return operator_factory(self._operation, args)


class operator_factory(object):
    def __init__(self, operation, arguments):
        self._operation = operation
        self._arguments = arguments

    def __rmatmul__(self, other):
        if(isinstance(other, operator)):
            return self.make_operator(other)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __mul__(self, other):
        if(isinstance(self, state)):
            nbits = other.nbits
            op = operator(nbits)

            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_factory and '{}'".format(type(other)))
    def make_operator(self, op):
        return self._operation(*(self._arguments), op)



def operation(f):
    return operator_factory_spawner(f)



