from inspect import signature

from .operator import operator
from .state import state



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
    def __matmul__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self, other)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __mul__(self, other):
        if(isinstance(other, state)):
            nbits = other.nbits
            op = operator(nbits)
            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_factory_spawner and '{}'".format(type(other)))

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
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(other, self)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __matmul__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self, other)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __mul__(self, other):
        if(isinstance(other, state)):
            nbits = other.nbits
            op = operator(nbits)
            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_factory and '{}'".format(type(other)))
    def make_operator(self, op):
        return self._operation(*(self._arguments), op)

class operator_product_factory(object):
    def __init__(self, leftside, rightside):
        if(isinstance(leftside, list)):
            self._list = leftside
        else:
            self._list = [leftside]

        if(isinstance(rightside, list)):
            self._list.extend(rightside)
        else:
            self._list.append(rightside)

    def __rmatmul__(self, other):
        if(isinstance(other, operator)):
            o = other
            for factory in self._list:
                o = o @ factory
            return o
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(other, self._list)
        if(isinstance(other, operator_product_factory)):
            return operator_product_factory(other._list, self._list)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_product_factory ".format(type(other)))

    def __matmul__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self._list, other)
        if(isinstance(other, operator_product_factory)):
            return operator_product_factory(self._list, other._list)
        raise TypeError("Cannot __matmul__ operator_product_factory '{}' and  '{}'".format(type(other)))

    def __mul__(self, other):
        if(isinstance(other, state)):
            nbits = other.nbits
            op = operator(nbits)
            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_product_factory and '{}'".format(type(other)))



def operation(f):
    return operator_factory_spawner(f)



