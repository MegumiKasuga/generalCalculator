from kimieCarole.core.VariableCalculator import VariableCalculator
from kimieCarole.util.utils import number_list, regex_list
from copy import deepcopy


class FunctionCalculator:

    def __init__(self):
        pass

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
        parameters = []
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
        for i in self.idenpendent_variables:
            if parameter_list.__contains__(''):
                parameter_list.remove('')
            if parameter_list.__contains__(i):
                parameter_list.remove(i)
                pass
            pass

        self.parameters = parameter_list

        if left_side > 0:
            for i in range(0, len(exp_list) - 2):
                self.dependent_variables.append(VariableCalculator.variable_check(exp_list[i]))
                pass
            pass

        self.bubbleSorting(self.idenpendent_variables)
        self.bubbleSorting(self.parameters)
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
        left = right = -1
        offset = 0
        for xi in range(0, len(self.idenpendent_variables)):
            i = self.idenpendent_variables[xi]
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
                        exp = exp[0: left] + '*' + regexs_list[xi] + exp[right: len(exp)]
                    else:
                        exp = exp[0:left] + regexs_list[xi]
                    right = left = -1
                    break
                elif regex_list.__contains__(exp[pointer + len(i)]) or number_list.__contains__(
                        exp[pointer + len(i)]) or brackets_and_space.__contains__(exp[pointer + len(i)]):
                    right = pointer + len(i)
                    if number_list.__contains__(exp[pointer - 1]):
                        exp = exp[0: left] + '*' + regexs_list[xi] + exp[right: len(exp)]
                    else:
                        exp = exp[0: left] + regexs_list[xi] + exp[right: len(exp)]
                    right = left = -1
                    break
                else:
                    offset += pointer
                    pointer = exp.find(i, offset)
                continue
                pass
            pass

        return exp

    def print(self):
        print(('<Function ' + self.name + '>').center(30, '='))
        print('indenpent vars:')
        print('          ', self.idenpendent_variables)
        if len(self.dependent_variables) > 0:
            print('dependent vars:')
            print('          ', self.dependent_variables)
            pass
        else:
            print('no dependent var')
            pass
        if len(self.parameters) > 0:
            print('parameters:')
            print('          ', self.parameters)
            pass
        else:
            print('no parameter')
        print('expression:')
        print(self.name + str(tuple(self.idenpendent_variables)).replace(',)', ')').replace('\'', '') + '=' + self.body)

    def bubbleSorting(self, regexs):
        last_regexs = []

        while last_regexs != regexs:
            last_regexs = deepcopy(regexs)
            for i in range(0, len(regexs) - 1):
                if len(regexs[i]) < len(regexs[i + 1]):
                    cache = regexs[i]
                    regexs[i] = regexs[i + 1]
                    regexs[i + 1] = cache
                    continue
                    pass
                pass
            pass

        return regexs
