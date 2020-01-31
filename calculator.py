from initialize import tokenize
from parsing import Parser
from extra_funcs import from_list_to_str
from extra_funcs import domain_to_string
from extra_funcs import diff
from extra_funcs import is_digit
from extra_funcs import is_same
from math import nan, e
from copy import deepcopy


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
                eq_diff.append(from_list_to_str('', diff(ans, var_list[n], var_list)))

            return [from_list_to_str('', ans), eq_diff, domain, in_domain]

    except Exception as e:
        return 'Error', e, 0, 0


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
            if temp[0] not in var_list:
                raise Exception('%s is not in current variable list' % (temp[0]))
            if len(temp) != 2 or not is_digit(temp[1]):
                raise Exception('Wrong input')
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

            ans, _, _, _ = sigma(eq_list[2], sig_eq, eq_list[-5], eq_list[-3], var_list)

            return ans

        E = Parser(eq_list, var_list)
        # print('tree: ', str(E))

        ans = E.eval()
        
        return from_list_to_str('', ans)

    except Exception as e:
        return '*Error* ' + str(e)


def plot_2D(eq, domain, in_domain, var_list, ran, interval):
    var = var_list[0]

    ipts = []
    opts = []
    ipt = []
    opt = []

    for n in range(int((ran[1]-ran[0])/interval)):
        value = ran[0] + interval * n
        
        if check_domain(domain, in_domain, var_list, var+'='+str(value)):
            ans = change_x_to_num(eq, var_list, var + '=' + str(value))

            if is_digit(ans):
                ipt.append(value)
                opt.append(float(ans))
            else:
                ipts.append(ipt)
                opts.append(opt)
                ipt = []
                opt = []
        else:
            ipts.append(ipt)
            opts.append(opt)
            ipt = []
            opt = []

    ipts.append(ipt)
    opts.append(opt)

    
    return [ipts, opts]


def plot_3D(eq, domain, in_domain, var_list, ran1, ran2, interval_x, interval_y):
    var1 = var_list[0]
    var2 = var_list[1]

    ipt1 = []
    ipt2 = []
    opt = []

    for n in range(int((ran1[1]-ran1[0])/interval_x)):
        value1 = ran1[0] + interval_x * n

        for m in range(int((ran2[1]-ran2[0])/interval_y)):
            value2 = ran2[0] + interval_y * m

            if check_domain(domain, in_domain, var_list, var1+'='+str(value1) +','+ var2+'='+str(value2)):
                ans = change_x_to_num(eq, var_list, var1+'='+str(value1) +','+ var2+'='+str(value2))
                ipt1.append(value1)
                ipt2.append(value2)

                if is_digit(ans):
                    opt.append(float(ans))
                else:
                    opt.append(nan)
            else:
                ipt1.append(value1)
                ipt2.append(value2)
                opt.append(nan)

    return [ipt1, ipt2, opt]


def differentiable_1D(eq, eq_diff, domain, in_domain, string, var_list):
    try:

        epsilon = 10 ** -5

        var = []
        value = []
        string1 = string.replace(" ", "")
        string1 = string1.split(',')

        for n in range(len(string1)):
            temp = string1[n].split('=')
            if temp[0] not in var_list:
                raise Exception('%s is not in current variable list' % (temp[0]))
            if len(temp) != 2 or not is_digit(temp[1]):
                raise Exception('Wrong input')
            var.append(temp[0])
            value.append(temp[1])
        
        if len(var) != 1:
            raise Exception('Expected 1 variable but got %d' % (len(var)))
        else:
            var = var[0]
            value = value[0]

        if check_domain(domain, in_domain, [var], var+'='+str(float(value)+epsilon)):
            ans_l_p = change_x_to_num(eq, [var], var+'='+str(float(value)+epsilon))
            ans_d_l_p = change_x_to_num(eq_diff[0], [var], var+'='+str(float(value)+epsilon))
        else:
            return 0

        if check_domain(domain, in_domain, [var], var+'='+str(float(value)-epsilon)):
            ans_l_m = change_x_to_num(eq, [var], var+'='+str(float(value)-epsilon))
            ans_d_l_m = change_x_to_num(eq_diff[0], [var], var+'='+str(float(value)-epsilon))
        else:
            return 0

        if check_domain(domain, in_domain, [var], var+'='+str(value)):
            ans = change_x_to_num(eq, [var], var+'='+value)
            ans_d = change_x_to_num(eq_diff[0], [var], var+'='+value)
        else:
            return 0

        epsilon = epsilon * 1000

        if is_same([ans_l_p, ans_l_m, ans], epsilon) and is_same([ans_d_l_p, ans_d_l_m, ans_d], epsilon):
            return 1
        else:
            return 0

    except Exception as e:
        print('Error: ', e)
        return '*Error* ' + str(e)

def differentiable_2D(eq, eq_diff, domain, in_domain, string, var_list):
    try:
        dx = -1
        dy = -1

        epsilon = 10**(-10)

        var = []
        value = []
        string1 = string.replace(" ", "")
        string1 = string1.split(',')

        for n in range(len(string1)):
            temp = string1[n].split('=')
            if temp[0] not in var_list:
                raise Exception('%s is not in current variable list' % (temp[0]))
            if len(temp) != 2 or not is_digit(temp[1]):
                raise Exception('Wrong input')
            var.append(temp[0])
            value.append(temp[1])

        if len(var) != 2:
            raise Exception('Expected 2 variable but got %d' % (len(var)))

        PlusMinus_epsilon = [+epsilon, -epsilon]
        ans_l_x = []
        ans_l_dx = []
        ans_l_y = []
        ans_l_dy = []

        for n in range(len(PlusMinus_epsilon)):
            temp_string = var[0] + '=' + str(float(value[0])+PlusMinus_epsilon[n]) + ',' + var[1] + '=' + value[1]
            if check_domain(domain, in_domain, var, temp_string):
                ans_l_x.append(change_x_to_num(eq, var, temp_string))
                ans_l_dx.append(change_x_to_num(eq_diff[0], var, temp_string))
            else:
                dx = 0

        for n in range(len(PlusMinus_epsilon)):
            temp_string = var[0] + '=' + value[0] + ',' + var[1] + '=' + str(float(value[1])+PlusMinus_epsilon[n])
            if check_domain(domain, in_domain, var, temp_string):
                ans_l_y.append(change_x_to_num(eq, var, temp_string))
                ans_l_dy.append(change_x_to_num(eq_diff[0], var, temp_string))
            else:
                dy = 0

        if check_domain(domain, in_domain, var, string):
            ans = change_x_to_num(eq, var, string)
            ans_dx = change_x_to_num(eq_diff[0], var, string)
            ans_dy = change_x_to_num(eq_diff[1], var, string)
        else:
            dx = 0
            dy = 0

        epsilon = epsilon * 10

        if dx == -1 and is_same([ans_l_x[0], ans_l_x[1], ans], epsilon):
            if is_same([ans_l_dx[0], ans_l_dx[1], ans_dx], epsilon):
                dx = 1
            else:
                dx = 0
        else:
            dx = 0

        if dy == -1 and is_same([ans_l_y[0], ans_l_y[1], ans], epsilon):
            if is_same([ans_l_dy[0], ans_l_dy[1], ans_dy], epsilon):
                dy = 1
            else:
                dy = 0
        else:
            dy = 0
        

        return [dx, dy]

    except Exception as e:
        print('Error: ', e)
        return '*Error* ', str(e)


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

    return [str(ans), [], [], []]


def check_domain(domain, in_domain, var_list, input):
    if domain:
        domain = domain_to_string(domain, var_list)
    if in_domain:
        in_domain = domain_to_string(in_domain, var_list)

    for n in range(len(domain)):
        opt = change_x_to_num(domain[n], var_list, input)
        if is_digit(opt):
            if float(opt) == 0:
                return 0
        else:
            return 0
    
    for n in range(len(in_domain)):
        opt = change_x_to_num(in_domain[n], var_list, input)
        if is_digit(opt):
            if float(opt) <= 0:
                return 0
        else:
            return 0

    return 1