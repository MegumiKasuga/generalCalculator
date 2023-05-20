from copy import copy
from kimieCarole.util.utils import timer
import kimieCarole.util.utils as utils

class BasicCalculator:

    def __init__(self):
        pass

    # @timer
    def calculator_core(self, expression):

        exp = str(expression)
        exp = exp.replace(' ', '')

        self.expression_checking(exp)
        exp_list = self.automatic_sentence_breaking(exp)

        while True:
            for i in range(0 , len(exp_list)):
                pattern = exp_list[i]
                if pattern == '*':
                    exp_list[i + 1] = float(exp_list[i - 1]) * float(exp_list[i + 1])
                    exp_list[i] = exp_list[i-1] = ''
                if pattern == '/':
                    exp_list[i + 1] = float(exp_list[i - 1]) / float(exp_list[i + 1])
                    exp_list[i] = exp_list[i - 1] = ''
                pass
            exp_list = list(filter(lambda x: x != '' , exp_list))
            if not (exp_list.__contains__('*') or exp_list.__contains__('/')):
                break
            continue

        for i in range(len(exp_list)):
            pattern = exp_list[i]
            if pattern == '+':
                exp_list[i + 1] = float(exp_list[i - 1]) + float(exp_list[i + 1])
            if pattern == '-':
                exp_list[i + 1] = float(exp_list[i - 1]) - float(exp_list[i + 1])
            if pattern == '%':
                exp_list[i + 1] = float(exp_list[i - 1]) % float(exp_list[i + 1])
            pass

        return exp_list[-1]

    # @timer
    def automatic_sentence_breaking(self, expression):
        exp = str(expression)
        exp_check = str(copy(exp))
        for i in utils.regex_list:
            exp_check = exp_check.replace(i, '')

        for i in utils.number_list:
            exp_check = exp_check.replace(i, '')

        if exp_check != '':
            raise TypeError

        result = []
        while exp != '':
            i = 0
            regex = ''
            for x in exp:
                i += 1
                if utils.regex_list.__contains__(x):
                    regex = x
                    break
                pass

            if i == len(exp):
                result.append(exp)
                break
            else:
                result.append(exp[0:i - 1])
                result.append(regex)
                exp = exp[i:]
                i = 0
            pass

        return result

    # @timer
    def expression_checking(self, expression):
        exp = str(expression)

        if utils.regex_list.__contains__(exp[0]) or utils.regex_list.__contains__(exp[-1]):
            raise SyntaxError

        counter = 0
        for i in exp:
            if utils.regex_list.__contains__(i):
                counter += 1
                pass

            if counter > 1:
                raise SyntaxError

            if utils.number_list.__contains__(i):
                counter = 0
                pass
        return

    # @timer
    def bracket_checking(self, expression):
        counter_front = 0
        counter_back = 0

        exp = str(expression)

        if exp.find('(') == -1:
            if exp.find(')') == -1:
                return False
            else:
                raise SyntaxError
            pass
        else:
            if exp.find(')') == -1:
                raise SyntaxError
            pass

        for i in expression:
            if i == '(':
                counter_front += 1
                continue
            if i == ')':
                counter_back += 1
                continue
            pass

        if counter_front != counter_back:
            raise SyntaxError

        return True

    # @timer
    def automatic_bracket_breaking(self, expression):
        if not self.bracket_checking(expression):
            return expression

        exp = str(expression)
        level = 0
        front_bracket = -1
        back_bracket = -1

        for i in range(0, len(exp)):
            regex = exp[i]
            if regex == '(':
                if level == 0:
                    front_bracket = i
                    pass
                level += 1
                pass

            if regex == ')':
                if level == 1:
                    back_bracket = i
                    break
                    pass
                level -= 1
                pass
            pass

        return exp[front_bracket + 1: back_bracket], front_bracket, back_bracket + 1

    # @timer
    def basic_calculator(self, expression):
        exp = str(expression)

        if self.bracket_checking(exp):
            results = self.automatic_bracket_breaking(exp)
            result_str = self.basic_calculator(results[0])
            exp = exp[0:results[1]] + str(result_str) + exp[results[2]:]
            pass
        if not self.bracket_checking(exp):
            return self.calculator_core(exp)
