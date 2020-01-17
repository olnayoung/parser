from initialize import tokenize
from parsing import Parser
from extra_funcs import from_list_to_str
from extra_funcs import in_eq_domain
from extra_funcs import eq_domain
from extra_funcs import diff
import matplotlib.pyplot as plt


### main function
def calcul(eq, var_list):

    try:
        eq = eq.replace(" ", "")
        eq_list = tokenize(eq, var_list)

        if eq_list[0] == 'sig':
            sig_eq = ''
            for n in range(4, len(eq_list)-6):
                sig_eq += str(eq_list[n])

            return sigma(eq_list[2], sig_eq, eq_list[-5], eq_list[-3], var_list)

        else:
            E = Parser(eq_list, var_list)
            ans = E.eval()
            domain, in_domain = E.get_domain()

            eq_diff = []
            for n in range(len(var_list)):
                eq_diff.append(from_list_to_str('', diff(ans, var_list[n])))

            # print('f =', eq)
            # print('tokens:', eq_list)
            # print('tree: ', str(E))

            return [from_list_to_str('', ans), eq_diff, domain, in_domain]

    except Exception as e:
        print('Error: ', e)
        return 'Error', 0, 0, 0


def change_x_to_num(eq, var_list, string):
    try:
        eq = eq.replace(" ", "")
        eq_list = tokenize(eq, var_list)

        variable = []
        value = []
        string = string.replace(" ", "")
        string = string.split(',')

        for n in range(len(string)):
            temp = string[n].split('=')
            variable.append(temp[0])
            value.append(temp[1])

        for n in range(len(variable)):
            eq_temp = []

            for m in range(len(eq_list)):
                if eq_list[m] == variable[n]:
                    eq_temp.append(float(value[n]))
                else:
                    eq_temp.append(eq_list[m])

            eq_list = eq_temp

        if eq_list[0] == 'sig':
            sig_eq = ''
            for n in range(4, len(eq_list)-6):
                sig_eq += str(eq_list[n])

            ans, a, b, c = sigma(eq_list[2], sig_eq, eq_list[-5], eq_list[-3], var_list)

            return ans

        E = Parser(eq_list, var_list)
        # print('tree: ', str(E))

        ans = E.eval()
        
        return from_list_to_str('', ans)

    except Exception as e:
        print('Error: ', e)
        return 'Error'


def plot_graph(eq, domain, in_domain, var_list, ran):
    var = var_list[0]

    ipt = []
    opt = []
    plt.clf()

    for n in range(int((ran[1]-ran[0])/0.1)):
        value = ran[0] + 0.1 * n
        
        if check_domain(domain, in_domain, var_list, var+'='+str(value)):
            ans = change_x_to_num(eq, var_list, var + '=' + str(value))

            ipt.append(value)
            opt.append(float(ans))
        else:
            plt.plot(ipt, opt, 'b')
            ipt = []
            opt = []


    plt.plot(ipt, opt, 'b')
    name = 'graph.png'
    plt.savefig(name)
    
    return name


def differentiable(eq, eq_diff, string):
    try:
        variable = []
        value = []
        string = string.replace(" ", "")
        string = string.split(',')

        for n in range(len(string)):
            temp = string[n].split('=')
            variable.append(temp[0])
            value.append(temp[1])

    except Exception as e:
        print('Error: ', e)
        return 'Error'
    return 0


def sigma(k, equation, start, end, var_list = None):

    check = 0
    if var_list:
        for n in range(len(var_list)):
            if var_list[n] in equation:
                check = 1
                continue
    
    if check:
        ap_var_list = var_list.copy()
        ap_var_list.append(k)
        eq, a, b, c = calcul(equation, ap_var_list)
        ans = 'sig(' + k + ', ' + eq + ', ' + str(start) + ', ' + str(end) + ')'

        eq_diff = []

        for n in range(len(var_list)):
            eq_diff.append('sig(' + k + ', ' + a[n] + ', ' + str(start) + ', ' + str(end) + ')')
        
        return [ans, eq_diff, b, c]
    
    else:
        ans = 0
        eq, a, b, c = calcul(equation, [k])

        for n in range(int(start), int(end)+1):
            string = k + '=' + str(n)
            ans += float(change_x_to_num(eq, [k], string))

    return [ans, 0, 0, 0]


def check_domain(domain, in_domain, var_list, input):
    domain = eq_domain(domain, var_list)
    in_domain = in_eq_domain(in_domain, var_list)

    for n in range(len(domain)):
        if float(change_x_to_num(domain[n], var_list, input)) == 0:
            return 0
    
    for n in range(len(in_domain)):
        if float(change_x_to_num(in_domain[n], var_list, input)) <= 0:
            return 0

    return 1