from initialize import tokenize
from parsing import Parser
from extra_funcs import from_list_to_str
from extra_funcs import in_eq_domain
from extra_funcs import eq_domain


### main function
def calcul(eq):

    var_list = []
    temp = input()
    temp = temp.split(',')

    try:
        if temp[0] != '':
            for n in range(len(temp)):
                var = temp[n].split(' ')
                if var[-1] in ['e', 'pi']:
                    raise Exception("%s is not available" % (var[-1]))
                var_list.append(var[-1])

        print('f =', eq)
        eq_list = tokenize(eq, var_list)
        print('tokens:', eq_list)

        E = Parser(eq_list, var_list)
        print('tree: ', str(E))
        ans = E.eval()
        print(ans)
        eq, in_eq = E.get_domain()
        print(eq, in_eq)

        print('domain:', in_eq_domain(in_eq, var_list), 'except', eq_domain(eq, var_list))

        return from_list_to_str('', ans)

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