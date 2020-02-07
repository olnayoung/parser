from initialize import tokenize
from parsing import Parser
from extra_funcs import is_digit
from math import nan, e
from copy import deepcopy

def calcul(eq, var_list):
    try:
        eq = eq.replace(" ", "")
        eq_list = tokenize(eq, var_list)

        E = Parser(eq_list, var_list)
        ans = E.eval()

        return ans

    except Exception as e:
        return e