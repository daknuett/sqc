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
            return operator_product_factory(self, other, True)
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

    def __or__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self, other, False)
        raise TypeError("cannot __or__ operator_factory_spawner and '{}'".format(type(other)))


class operator_factory(object):
    def __init__(self, operation, arguments):
        self._operation = operation
        self._arguments = arguments

    def __rmatmul__(self, other):
        if(isinstance(other, operator)):
            return self.make_operator(other)
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(other, self, True)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __matmul__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self, other, True)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_factory".format(type(other)))

    def __mul__(self, other):
        if(isinstance(other, state)):
            nbits = other.nbits
            op = operator(nbits)
            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_factory and '{}'".format(type(other)))
    def make_operator(self, op):
        return self._operation(*(self._arguments), op)
    def __or__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self, other, False)
        raise TypeError("cannot __or__ operator_factory and '{}'".format(type(other)))

class operator_product_factory(object):
    def __init__(self, leftside, rightside, is_matmul):
        if(isinstance(leftside, list)):
            self._list = leftside
        else:
            self._list = [leftside]

        if(isinstance(rightside, list)):
            self._list.extend(rightside)
        else:
            self._list.append(rightside)

        self._is_matmul = is_matmul

    def __rmatmul__(self, other):
        if(isinstance(other, operator)):
            o = other
            if(self._is_matmul):
                # This operator product factory has been created using 
                # the matmul operator (@), which means that the gates 
                # are treated, as if they were multiplied on the states
                # (from right to left). This is the most intuitive way to use
                # them, but it can be confusing when they are compared to 
                # a quantum gate circuit.
                for factory in reversed(self._list):
                    o = o @ factory
            else:
                # This operator product factory has been created using the
                # bitwise-or (|) operator, so they are treated like in a 
                # quantum gate circuit (from left to right).
                for factory in self._list:
                    o = o @ factory
            return o
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            if(not self._is_matmul):
                raise SyntaxError("Cannot mix piped operators (joined using '|') and multiplied operators (joined using '@')")
            return operator_product_factory(other, self._list, True)
        raise TypeError("Cannot __rmatmul__ '{}' and operator_product_factory ".format(type(other)))

    def __matmul__(self, other):
        if(not self._is_matmul):
            raise SyntaxError("Cannot mix piped operators (joined using '|') and multiplied operators (joined using '@')")
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self._list, other, True)
        if(isinstance(other, operator_product_factory)):
            return operator_product_factory(self._list, other._list, True)
        raise TypeError("Cannot __matmul__ operator_product_factory '{}' and  '{}'".format(type(other)))

    def __mul__(self, other):
        if(isinstance(other, state)):
            nbits = other.nbits
            op = operator(nbits)
            return (op @ self) * other
        raise TypeError("Cannot __mul__ operator_product_factory and '{}'".format(type(other)))

    def __or__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(self._list, other, False)
        if(isinstance(other, operator_product_factory)):
            return operator_product_factory(self._list, other._list, False)
        raise TypeError("cannot __or__ operator_product_factory and '{}'".format(type(other)))

    def __ror__(self, other):
        if(isinstance(other, (operator_factory, operator_factory_spawner))):
            return operator_product_factory(other, self._list, False)
        if(isinstance(other, operator_product_factory)):
            return operator_product_factory(other._list, self._list, False)
        raise TypeError("cannot __or__ operator_product_factory and '{}'".format(type(other)))
        



def operation(f):
    return operator_factory_spawner(f)



