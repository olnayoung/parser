from extra_funcs import is_digit

def tokenize(eq, var_list):
    eq_list = []
    funcs_list = ['log', 'sin', 'cos', 'tan', 'sig']
    op_list = ['+', '-', '*', '/', '^', '(', ')', ',']
    temp = '0'

    for n in range(len(eq)):
        if n == len(eq) - 1:
            if is_digit(eq[n]) or eq[n] == '.':
                temp += str(eq[n])
                eq_list.append(float(temp))
            elif eq[n] in var_list:
                eq_list.append(eq[n])
            elif eq[n-1:n+1] == 'pi':
                eq_list.pop()
                eq_list.append(eq[n-1:n+1])
            elif eq[n] in op_list:
                if temp != '0':
                    eq_list.append(float(temp))
                eq_list.append(eq[n])
            else:
                eq_list.append(eq[n])

        elif n == 0:
            if is_digit(eq[n]) or eq[n] == '.':
                temp += str(eq[n])
                if n == len(eq)-1:
                    eq_list.append(float(temp))
            elif eq[n] in var_list or eq[n] in op_list:
                eq_list.append(eq[n])
            else:
                eq_list.append(eq[n])

        elif n == (1 or 2):
            if is_digit(eq[n]) or eq[n] == '.':
                temp += str(eq[n])
            elif eq[n-1:n+1] == 'pi':
                eq_list.pop()
                eq_list.append(eq[n-1:n+1])
            elif eq[n] in var_list or eq[n] in op_list:
                if is_digit(eq[n-1]) or eq[n-1] == '.':
                    eq_list.append(float(temp))
                    temp = '0'
                eq_list.append(eq[n])
            else:
                eq_list.append(eq[n])

        else:
            if is_digit(eq[n]) or eq[n] == '.':
                temp += str(eq[n])
            elif eq[n-1:n+1] == 'pi':
                eq_list.pop()
                eq_list.append(eq[n-1:n+1])
            elif eq[n-2:n+1] in funcs_list:
                eq_list.pop()
                eq_list.pop()
                eq_list.append(eq[n-2:n+1])
            elif eq[n] in var_list or eq[n] in op_list:
                if is_digit(eq[n-1]) or eq[n-1] == '.':
                    eq_list.append(float(temp))
                    temp = '0'
                eq_list.append(eq[n])
            else:
                eq_list.append(eq[n])

    eq_list.append('$')

    return eq_list