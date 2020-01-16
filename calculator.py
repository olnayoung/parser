from initialize import tokenize
from parsing import Parser
from extra_funcs import from_list_to_str
from extra_funcs import in_eq_domain
from extra_funcs import eq_domain
from extra_funcs import diff
import matplotlib.pyplot as plt


### main function
def calcul(eq, var_list):

    # var_list = []
    # temp = input()
    # temp = temp.split(',')

    try:
        # var_list = []
        # temp = temp.split(',')

        # if temp[0] != '':
        #     for n in range(len(temp)):
        #         var = temp[n].split(' ')
        #         if var[-1] in ['e', 'pi']:
        #             raise Exception("%s is not available" % (var[-1]))
        #         var_list.append(var[-1])

        # var_list = ['x', 'y']

        print('f =', eq)
        eq_list = tokenize(eq, var_list)
        print('tokens:', eq_list)

        E = Parser(eq_list, var_list)
        print('tree: ', str(E))
        ans = E.eval()
        domain, in_domain = E.get_domain()

        # if not domain and not in_domain:
        #     print('domain: -inf ~ inf')
        # elif not domain and in_domain:
        #     print('domain:', in_eq_domain(in_domain, var_list))
        # elif domain and not in_domain:
        #     print('domain: -inf ~ inf except', eq_domain(domain, var_list))
        # else:
        #     print('domain:', in_eq_domain(in_domain, var_list), 'except', eq_domain(domain, var_list))

        eq_diff = []
        for n in range(len(var_list)):
            eq_diff.append(from_list_to_str('', diff(ans, var_list[n])))


        return [from_list_to_str('', ans), eq_diff, domain, in_domain]

    except Exception as e:
        print('Error: ', e)
        return 'Error'


def change_x_to_num(eq, var_list, string):
    try:
        print('f =', eq)
        eq_list = tokenize(eq, var_list)
        print('tokens:', eq_list)

        variable = []
        value = []
        string = string.split(',')

        for n in range(len(string)):
            temp = string[n].split('=')
            vari = temp[0].split(' ')
            val = temp[1].split(' ')
            for m in range(len(vari)):
                if vari[m] != '':
                    variable.append(vari[m])
            value.append(val[-1])

        for n in range(len(variable)):
            eq_temp = []

            for m in range(len(eq_list)):
                if eq_list[m] == variable[n]:
                    eq_temp.append(float(value[n]))
                else:
                    eq_temp.append(eq_list[m])

            eq_list = eq_temp

        E = Parser(eq_list, var_list)
        print('tree: ', str(E))

        ans = E.eval()
        
        return from_list_to_str('', ans)

    except Exception as e:
        print('Error: ', e)
        return 'Error'


def plot_graph(eq, var_list, ran):
    var = var_list[0]

    ipt = []
    opt = []

    for n in range(int((ran[1]-ran[0])/0.1)):
        value = ran[0] + 0.1 * n
        ans = change_x_to_num(eq, var_list, var + '=' + str(value))

        ipt.append(value)
        opt.append(float(ans))

    # eq_temp = []
    # for m in range(len(eq)):
    #     if eq[m] == var:
    #         eq_temp.append('nn')
    #     else:
    #         eq_temp.append(eq[m])
        
    plt.plot(ipt, opt)
    plt.show()
    
    return 0