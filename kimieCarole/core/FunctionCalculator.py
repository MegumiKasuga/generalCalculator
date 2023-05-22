from kimieCarole.core.BasicCalculator import BasicCalculator
from kimieCarole.core.VariableCalculator import VariableCalculator
from kimieCarole.util.utils import number_list, regex_list
from copy import deepcopy


class FunctionCalculator:

    variables = {}
    functions = []
    variable_calculator = VariableCalculator()
    calculator = BasicCalculator()
    default_var = 0
    _strict = False

    def __init__(self):
        global variables
        variables = {}
        global functions
        functions = []
        global variable_calculator
        variable_calculator = VariableCalculator()
        global calculator
        calculator = BasicCalculator()
        pass

    def load_function(self, function):
        if isinstance(function, Function):
            self.functions.append(function)
        else:
            raise TypeError
        pass

    def registerate_function(self, expression):
        expression = str(expression)
        function = Function()
        function.define_function(expression)
        self.functions.append(function)
        pass

    def get_function(self, func_name):
        for i in self.functions:
            if i.name == func_name:
                return i
            pass
        return None

    def discard_function(self, func_name):
        func = self.find_function(func_name)
        if func is not None:
            self.functions.remove(func)
            pass
        pass

    def define_variables(self, expression):
        exp_list = str(expression).split('=')

        if len(exp_list) == 1:
            return

        for i in range(0, len(exp_list) - 1):
            self.variables.update({VariableCalculator.variable_check(exp_list[i]): exp_list[len(exp_list) - 1]})
            pass

        self.variable_calculator.define_variable(expression)
        return

    def remove_variable(self, var_name):
        if self.variables.__contains__(var_name):
            self.variables.pop(var_name)
            self.variable_calculator.remove_var(var_name)
            pass
        return

    def set_default_var(self, var):
        if not (isinstance(var, float) or isinstance(var, int)):
            raise TypeError

        self._default_var = var
        self.variable_calculator.set_default_var(var)
        return

    def strict_mode(self, strict):
        self._strict = strict
        self.variable_calculator.set_strict_mode(strict)

    def find_function(self, expression):
        expression = str(expression)
        brackets_and_space = ['(', ')', ' ']
        front = back = -1
        switch = False
        level = 0
        for i in range(0, len(expression)):
            regex = expression[i]
            if not (number_list.__contains__(regex) or regex_list.__contains__(regex)):
                if not brackets_and_space.__contains__(regex):
                    if not switch:
                        front = i
                        switch = True
                    else:
                        pass
                    continue
                    pass
                else:
                    if regex == '(' and switch:
                        level += 1
                        continue
                        pass
                    elif regex == ')':
                        level -= 1
                        if level == 0 and switch:
                            back = i
                            break
                            pass
                        pass
                    continue
                    pass

            if regex_list.__contains__(regex) and level == 0:
                switch = False
                front = back = -1
                continue
            pass

        if front != -1 and back != -1:
            return expression[front: back + 1], front, back
        else:
            return None

    def calculate(self, expression):
        expression = str(expression)

        func = self.find_function(expression)
        while func is not None:
            func_name = func[0][0:func[0].find('(')]
            catched = self.get_function(func_name)
            if catched is None:
                raise SyntaxError
            expression = expression[0:func[1]] + '(' + catched.assignment(func[0]) + ')' + expression[func[2]+1:]
            func = self.find_function(expression)
            continue
            pass

        return self.variable_calculator.calculate(expression, self.calculator)

    def print(self):
        print(__name__.center(40,'='))
        print('strict mode:')
        print('          ', self._strict)
        print('variables:')
        print('          ' , self.variables)
        print('functions:')
        for i in self.functions:
            i.print(5)
            pass
        print('='.center(15 + len(__name__), '='))



def remove_all_spaces(l):
    l = list(l)
    while l.__contains__(''):
        l.remove('')
        pass
    return l


class Function:
    name = ''
    body = ''
    idenpendent_variables = []
    dependent_variables = []
    parameters = []

    def __init__(self):
        global name
        global body
        global idenpendent_variables
        global dependent_variables
        global parameters

        name = ''
        body = ''
        idenpendent_variables = []
        dependent_variables = []
        parameters = {}
        pass

    def define_function(self, expression):

        expression = str(expression)

        exp_list = expression.split('=')

        left_side = 0
        right_side = 1

        if len(exp_list) < 2:
            raise SyntaxError

        if len(exp_list) > 2:
            left_side = len(exp_list) - 2
            right_side = len(exp_list) - 1

        if not (exp_list[left_side].__contains__('(') and exp_list[left_side].__contains__(')')):
            raise SyntaxError

        if exp_list[left_side].count('(') != exp_list[left_side].count(')'):
            raise SyntaxError

        if exp_list[left_side][-1] != ')':
            raise SyntaxError

        self.name = VariableCalculator.variable_check(exp_list[left_side][0: exp_list[left_side].find('(')])

        vars = exp_list[left_side][exp_list[left_side].find('(') + 1: len(exp_list[left_side]) - 1]

        front = 0

        level = 0
        for i in range(0, len(vars)):
            regex = vars[i]
            if regex == '(':
                level += 1
                continue
            if regex == ')':
                level -= 1
                continue
            if level == 0 and regex == ',':
                self.idenpendent_variables.append(vars[front: i])
                front = i + 1
                continue
            pass

        self.idenpendent_variables.append(vars[front: len(vars)])

        self.body = exp_list[right_side]

        parameter_check = self.body
        for i in number_list:
            parameter_check = parameter_check.replace(i, ' ')
            pass

        for i in regex_list:
            parameter_check = parameter_check.replace(i, ' ')
            pass

        exp_length = 0
        while exp_length != len(parameter_check):
            exp_length = len(parameter_check)
            parameter_check.replace('  ', ' ')
            continue

        parameter_list = parameter_check.split(' ')
        for i in parameter_list:
            if self.idenpendent_variables.__contains__(i):
                parameter_list.remove(i)
                pass
            pass

        while parameter_list.__contains__(''):
            parameter_list.remove('')
            pass

        self.parameters = dict.fromkeys(parameter_list, 0)

        if left_side > 0:
            for i in range(0, len(exp_list) - 2):
                self.dependent_variables.append(VariableCalculator.variable_check(exp_list[i]))
                pass
            pass

        self.bubbleSorting(self.dependent_variables)

        return self

    def assignment(self, expression):
        expression = str(expression)

        brackets_and_space = ['(', ')', ' ']

        function_name = expression[0: expression.find('(')]
        if function_name != self.name:
            raise TypeError

        regexs = expression[expression.find('(') + 1: expression.rfind(')')]
        regexs_list = []
        level = 0
        front = 0
        for i in range(0, len(regexs)):
            pattern = regexs[i]
            if pattern == '(':
                level += 1
                continue
            elif pattern == ')':
                level -= 1
                continue

            if pattern == ',' and level == 0:
                regexs_list.append(regexs[front:i])
                front = i + 1
                continue
            pass

        regexs_list.append(regexs[front:len(regexs)])

        if len(regexs_list) != len(self.idenpendent_variables):
            raise SyntaxError

        exp = deepcopy(self.body)
        variables = self.bubbleSorting(self.idenpendent_variables + list(self.parameters.keys()))

        assigment_list = []
        for i in variables:
            if self.idenpendent_variables.__contains__(i):
                assigment_list.append(str(regexs_list[self.idenpendent_variables.index(i)]))
            else:
                assigment_list.append(str(self.parameters.get(i)))
                pass
            pass

        offset = 0
        for xi in range(0, len(variables)):
            i = variables[xi]
            pointer = exp.find(i, offset)
            while pointer != -1:

                if pointer == 0:
                    left = 0
                elif regex_list.__contains__(exp[pointer - 1]) or number_list.__contains__(
                        exp[pointer - 1]) or brackets_and_space.__contains__(exp[pointer - 1]):
                    left = pointer
                else:
                    offset += pointer
                    pointer = exp.find(i, offset)
                    continue

                if pointer == len(exp) - len(i):
                    right = pointer
                    if number_list.__contains__(exp[pointer - 1]):
                        exp = exp[0: left] + '*' + assigment_list[xi] + exp[right: len(exp)]
                    else:
                        exp = exp[0:left] + assigment_list[xi]
                    break
                elif regex_list.__contains__(exp[pointer + len(i)]) or number_list.__contains__(
                        exp[pointer + len(i)]) or brackets_and_space.__contains__(exp[pointer + len(i)]):
                    right = pointer + len(i)
                    if number_list.__contains__(exp[pointer - 1]):
                        exp = exp[0: left] + '*' + assigment_list[xi] + exp[right: len(exp)]
                    else:
                        exp = exp[0: left] + assigment_list[xi] + exp[right: len(exp)]
                    break
                else:
                    offset += pointer
                    pointer = exp.find(i, offset)
                continue
                pass
            pass

        return exp

    def print(self , offset_len=0):
        offset = ''
        for i in range(offset_len):
            offset += ' '
            pass

        print(offset+(('<Function ' + self.name + '>').center(30, '=')))
        print(offset + 'indenpent vars:')
        print(offset + '          ', self.idenpendent_variables)
        if len(self.dependent_variables) > 0:
            print(offset + 'dependent vars:')
            print(offset + '          ', self.dependent_variables)
            pass
        else:
            print(offset + '--no dependent var--')
            pass
        if len(self.parameters) > 0:
            print(offset + 'parameters:')
            print(offset + '          ', self.parameters)
            pass
        else:
            print(offset + '--no parameter--')
        print(offset + 'expression:')
        print(offset + self.name + str(tuple(self.idenpendent_variables)).replace(',)', ')').replace('\'', '') + '=' + self.body)

        print(offset + ''.center(18+len('<Function ' + self.name + '>'), '='))

    def bubbleSorting(self, regexs):
        last_regexs = []

        regexs_keys = regexs if isinstance(regexs, list) else remove_all_spaces(list(regexs.keys()))

        while last_regexs != regexs_keys:
            last_regexs = deepcopy(regexs_keys)
            for i in range(0, len(regexs_keys) - 1):
                if len(regexs_keys[i]) < len(regexs_keys[i + 1]):
                    cache = regexs_keys[i]
                    regexs_keys[i] = regexs_keys[i + 1]
                    regexs_keys[i + 1] = cache
                    continue
                    pass
                pass
            pass

        if isinstance(regexs, list):
            regexs = regexs_keys
            return regexs
        else:
            result = dict.fromkeys(regexs_keys , '0')
            for i in regexs_keys:
                result.__setitem__(i, regexs.get(i))
            regexs = result
            return regexs
        pass

