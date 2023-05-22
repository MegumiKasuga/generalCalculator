import kimieCarole.util.utils as utils
from kimieCarole.core.BasicCalculator import BasicCalculator
from kimieCarole.util.utils import timer
class VariableCalculator:

    _var_dict = {}
    _default_var = 0.0
    _strict = False
    def __init__(self):
        global _var_dict
        _var_dict = {}
        global _default_var
        _default_var = 0.0
        global _strict
        _strict = False
        pass

    # @timer
    def define_variable(self, expression):

        exp_list = str(expression).split('=')

        if len(exp_list) == 1:
            return

        for i in range(0, len(exp_list) - 1):
            self._var_dict.update({self.variable_check(exp_list[i]): exp_list[len(exp_list) - 1]})
            pass

        return

    def variable_inheritance(self, var_dict):
        self._var_dict.update(var_dict)
        pass

    # @timer
    @staticmethod
    def variable_check(expression):
        if not isinstance(expression, str):
            raise TypeError

        expression = str(expression)

        if utils.number_list.__contains__(expression[0]):
            raise SyntaxError

        for i in expression:
            if (utils.regex_list.__contains__(i)):
                raise SyntaxError
            pass
        return expression

    # @timer
    def set_default_var(self, variable):

        if not (isinstance(variable, float) or isinstance(variable, int)):
            raise TypeError

        self._default_var = variable
        return

    def remove_var(self, var_name):
        if self.variables.__contains__(var_name):
            self.variables.pop(var_name)
            pass
        pass


    # @timer
    def set_strict_mode(self, isStrict):
        self._strict = isStrict

    # @timer
    def find_variable(self, expression):

        if not isinstance(expression, str):
            raise TypeError

        expression = str(expression)

        on_catch = False
        front = back = -1
        brackets_and_space = ['(', ')', ' ']
        length = len(expression)

        for i in range(0, length):
            regex = expression[i]
            if not (utils.number_list.__contains__(regex) or utils.regex_list.__contains__(
                    regex) or brackets_and_space.__contains__(regex)):
                if not on_catch:
                    if (i > 0):
                        if expression[i - 1] == '.':
                            raise SyntaxError
                        pass
                    on_catch = True
                    front = i
                    continue
                else:
                    continue
                pass
            if utils.regex_list.__contains__(regex) or brackets_and_space.__contains__(regex):
                if on_catch:
                    back = i
                    return expression[front: back], front, back
                    pass
                on_catch = False
                continue

        if on_catch and front != -1:
            return expression[front: length], front, length

        if front == back == -1:
            return None

    # @timer
    def assignment(self, expression):
        expression = str(expression)

        result = self.find_variable(expression)

        while result is not None:
            replacer = ''
            if result[1] > 0:
                if utils.number_list.__contains__(expression[result[1] - 1]):
                    if self._var_dict.__contains__(result[0]):
                        replacer = '*' + str(self._var_dict[result[0]])
                    else:
                        if self._strict:
                            raise IndexError
                        else:
                            self._var_dict.update({result[0]: self._default_var})
                            replacer = '*' + str(self._default_var)
                            pass
                    expression = expression[0:result[1]] + replacer + expression[result[2]:]
                    result = self.find_variable(expression)
                    continue
            if self._var_dict.__contains__(result[0]):
                replacer = str(self._var_dict[result[0]])
            else:
                if self._strict:
                    raise IndexError
                else:
                    self._var_dict.update({result[0]: self._default_var})
                    replacer = str(self._default_var)
                    pass
            expression = expression[0:result[1]] + str(replacer) + expression[result[2]:]
            result = self.find_variable(expression)
            continue

        return expression

    # @timer
    def calculate(self, expression , calculator):
        expression = str(expression)
        expression = self.assignment(expression)
        return calculator.basic_calculator(expression)