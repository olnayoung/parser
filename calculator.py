from initialize import tokenize
from parsing import Parser
from extra_funcs import from_list_to_str


### main function
def calcul(eq):

    try:
        print('f =', eq)
        eq_list = tokenize(eq)
        print('tokens:', eq_list)

        E = Parser(eq_list)
        print('tree: ', str(E))
        # ans = E.eval()
        # print('ans:', ans.a, ans.b, ans.c)

        # return E.eval()

    except Exception as e:
        print('Error: ', e)
        return 'Error'


def change_x_to_num(eq, xn = None, yn = None):
    try:
        print('f =', eq)
        eq_list = tokenize(eq)
        print('tokens:', eq_list)

        if xn is not None:
            x_applied = []
            for n in range(len(eq_list)):
                if eq_list[n] == 'x':
                    x_applied.append(xn)
                else:
                    x_applied.append(eq_list[n])

            eq_list = x_applied

        if yn is not None:
            y_applied = []
            for n in range(len(eq_list)):
                if eq_list[n] == 'y':
                    y_applied.append(yn)
                else:
                    y_applied.append(eq_list[n])

            eq_list = y_applied

        E = Parser(eq_list)
        print('tree: ', str(E))
        print('ans:', E.eval())

    except Exception as e:
        print('Error: ', e)
        return 'Error'