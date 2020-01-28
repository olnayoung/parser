from math import log, sin, cos, tan, pi, e, inf
from copy import deepcopy

def is_digit(value):
  try:
    float(value)
    return True
  except:
    return False


def is_oper(oper):
    return oper in ['+', '-', '*', '/']


def is_gathered(left):

    if isinstance(left[0], list):
        return True
    else:
        return False


def is_same(values, epsilon):
    for n in range(len(values)):
        for m in range(n, len(values)):
            if n != m:
                if abs(float(values[n]) - float(values[m])) > epsilon:
                    return 0

    return 1

def double_bracket(temp):
    if is_gathered(temp) and len(temp) == 1:
        temp = temp[0]
    return temp

def is_same_variable(left, sequence):
    out = 1
    for n in range(int(len(sequence)/2)):
        s_idx = 2*n+1

        for t in range(int(len(left)/2)):
            l_idx = 2*t+1

            if sequence[s_idx:s_idx+2] == left[l_idx:l_idx+2]:
                break

            if l_idx == len(left)-2:
                out = 0
                break
        
        if not out:
            break

    return out

def plus_sep(left, sequence, delete):
    check = 0
    for m in range(len(left)):
        if sequence[1:] == left[m][1:]:
            left[m][0] += sequence[0]
            check = 1
        
        elif len(sequence) == len(left[m]):
            if is_same_variable(left[m], sequence):
                left[m][0] += sequence[0]
                check = 1

        if left[m][0] == 0:
            delete.append(m)

            continue
    
    if not check and sequence[0] != 0:
        left.append(sequence)

    return left, delete


def plus(left, sequence):
    delete = []

    if not is_gathered(left):
        left = [left]

    if not is_gathered(sequence):
        left, delete = plus_sep(left, sequence, delete)
    
    else:
        for n in range(len(sequence)):
            left, delete = plus_sep(left, sequence[n], delete)

    while delete:
        t = delete.pop()
        del left[t]

    if not left:
        left.append([0])

    left = double_bracket(left)

    return left

def minus_sep(left, sequence, delete):
    check = 0
    for m in range(len(left)):
        if sequence[1:] == left[m][1:]:
            left[m][0] -= sequence[0]
            check = 1

        elif len(sequence) == len(left[m]):
            if is_same_variable(left[m], sequence):
                left[m][0] -= sequence[0]
                check = 1

        if left[m][0] == 0:
            delete.append(m)
            
            continue
    
    if not check:
        sequence[0] *= -1
        left.append(sequence)

    return left, delete

def minus(left, sequence):
    delete = []

    if not is_gathered(left):
        left = [left]

    if not is_gathered(sequence):
        left, delete = minus_sep(left, sequence, delete)
    
    else:
        for n in range(len(sequence)):
            left, delete = minus_sep(left, sequence[n], delete)

    while delete:
        t = delete.pop()
        del left[t]

    if not left:
        left.append([0])

    left = double_bracket(left)

    return left


def many_mul(ans, left, sequence):
    if is_gathered(left):
        for n in range(len(left)):
            ans = many_mul(ans, left[n], sequence)
    
    else:
        if is_gathered(sequence):
            for n in range(len(sequence)):
                ans = many_mul(ans, left, sequence[n])
        else:
            temp = multiply(left, sequence)

            if ans != []:
                ans = plus(ans, temp)

            else:
                for n in range(len(temp)):
                    ans.append(temp[n])
                
    return ans


def multiply(left, sequence):
    ans = []
    
    if left[0] * sequence[0] == 0:
        return [0]
    ans.append(left[0] * sequence[0])

    for n in range(1, len(left)):
        ans.append(left[n])

    for n in range(int(len(sequence)/2)):
        s_idx = 2*n+1

        if sequence[s_idx] in ans:
            a_idx = ans.index(sequence[s_idx])

            if is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
                ans[a_idx+1] += sequence[s_idx+1]
            # elif not is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
            #     ans[a_idx+1] = plus(ans[a_idx+1], [sequence[s_idx+1]])
            # elif is_digit(ans[a_idx+1]) and not is_digit(sequence[s_idx+1]):
            #     ans[a_idx+1] = plus([ans[a_idx+1]], sequence[s_idx+1])
            else:
                ans[a_idx+1] = plus(ans[a_idx+1], sequence[s_idx+1])
            
            if ans[a_idx+1] == 0:
                del ans[a_idx]
                del ans[a_idx]

        else:
            ans.append(sequence[s_idx])
            ans.append(sequence[s_idx+1])

    return ans


def many_div(ans, left, sequence):
    if is_gathered(left):
        for n in range(len(left)):
            ans = many_div(ans, left[n], sequence)
    
    else:
        if len(left) != 1:

            if is_gathered(sequence):
                ans.append(left)
                ans[-1].append(sequence)
                ans[-1].append(-1)
            else:
                temp = divide(left, sequence)
                ans.append(temp)
            
        else:
            if is_gathered(sequence):
                ans.append([left[0], sequence, -1])
            else:
                temp = divide(left, sequence)
                ans.append(temp)
                
    return ans


def divide(left, sequence):
    ans = []

    if left[0] == 0:
        return [0]

    ans = deepcopy(left)
    ans[0] /= sequence[0]

    for n in range(int(len(sequence)/2)):
        s_idx = 2*n+1

        if sequence[s_idx] in ans:
            a_idx = ans.index(sequence[s_idx])

            if is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
                ans[a_idx+1] -= sequence[s_idx+1]
            # elif not is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
            #     ans[a_idx+1] = minus(ans[a_idx+1], [sequence[s_idx+1]])
            # elif is_digit(ans[a_idx+1]) and not is_digit(sequence[s_idx+1]):
            #     ans[a_idx+1] = minus([ans[a_idx+1]], sequence[s_idx+1])
            else:
                ans[a_idx+1] = minus(ans[a_idx+1], sequence[s_idx+1])
            
            if ans[a_idx+1] == 0:
                del ans[a_idx]
                del ans[a_idx]

        else:
            ans.append(sequence[s_idx])
            ans.append(sequence[s_idx+1] * -1)

    return ans


def power(left, sequence):
    ans = []
    if is_gathered(left):
        if not is_gathered(sequence) and len(sequence) == 1:
            sequence = sequence[0]
        ans.append([1, left, sequence])
    else:
        sequence = double_bracket(sequence)
        if len(left) == 1:
            if left[0] != 1:
                if is_gathered(sequence):
                    ans.append([1, left, sequence])
                else:
                    if len(sequence) == 1:
                        ans.append(left[0] ** sequence[0])
                    else:
                        ans.append([1, left, sequence])
            else:
                ans.append(1)
        else:
            if not is_gathered(sequence) and len(sequence) == 1:
                ans.append(left[0] ** sequence[0])
            else:
                ans.append(1)
                if left[0] != 1:
                    ans.append(left[0])
                    ans.append(sequence)

            for n in range(int(len(left)/2)):
                l_idx = 2*n + 1

                ans.append(left[l_idx])

                if not is_gathered(sequence) and len(sequence) == 1 and is_digit(left[l_idx+1]):
                    ans.append(left[l_idx+1] * sequence[0])
                else:
                    ans.append(many_mul([], [left[l_idx+1]], sequence))

    return ans



def from_list_to_str(output, input):
    if is_gathered(input):
        for n in range(len(input)):
            if is_gathered(input[n]):
                output += '('
                output = from_list_to_str(output, input[n])
                output += ')'
            else:
                if n > 0:
                    if input[n][0] > 0:
                        output += '+'
                
                output = list_2_str(output, input[n])

    else:
        output = list_2_str(output, input)

    return output


def list_2_str(output, input):
    funcs_list = ['log', 'sin', 'cos', 'tan']

    check = 1
    if input[0] == 1:
        if len(input) == 1:
            output += '1'
        else:
            check = 0
    elif input[0] == -1:
        if len(input) == 1:
            output += '-1'
        else:
            output += '-'
            check = 0
    elif input[0] in funcs_list:
        output += input[0]
        check = 0
    else:
        output += str(input[0])
    
    for m in range(int(len(input)/2)):
        if check:
            output += '*'
        else:
            check = 1
        
        if input[0] == 'log':
            output += '('
            output = from_list_to_str(output, input[1])
            output += ','
            output = from_list_to_str(output, input[2])
            output += ')'
        elif input[0] in funcs_list:
            output += '('
            output = from_list_to_str(output, input[1])
            output += ')'
        else:
            idx = 2*m + 1

            if isinstance(input[idx], list):
                if len(input[idx]) == 1:
                    output += str(input[idx][0])
                elif input[idx][0] in funcs_list:
                    output = from_list_to_str(output, input[idx])
                else:
                    output += '('
                    output = from_list_to_str(output, input[idx])
                    output += ')'
            else:
                if input[idx+1] != 0:
                    output += str(input[idx])
                else:
                    output += '1'

            if input[idx+1] != 1 and input[idx+1] != 0:
                output += '^'

                if isinstance(input[idx+1], list):
                    output += '('
                    output = from_list_to_str(output, input[idx+1])
                    output += ')'
                else:
                    output += str(input[idx+1])

    return output


def eq_domain(eq, var_list):
    domain = []

    for n in range(len(eq)):
        st = from_list_to_str('', eq[n])

        domain.append(st)

    return domain

def in_eq_domain(in_eq, var_list):
    domain = []

    for n in range(len(in_eq)):
        st = from_list_to_str('', in_eq[n])
        domain.append(st)
            
    return domain


def diff(input, var):
    funcs_list = ['sin', 'cos', 'tan']
    output = []

    if is_gathered(input):                  # if it is polynomial
        for t in range(len(input)):
            temp = diff(input[t], var)

            if temp != [0]:
                if not output:
                    output = deepcopy(temp)
                else:
                    output = plus(output, temp)
                # output.append(temp)

    else:
        for n in range(int(len(input)/2)):

            input_rep = deepcopy(input)
            idx = 2*n + 1

            if input[idx] == var:
                if is_digit(input[idx+1]):
                    input_rep[0] *= input[idx+1]    
                    input_rep[idx+1] -= 1

                    if input_rep[idx+1] == 0:
                        del input_rep[idx]
                        del input_rep[idx]

                else:
                    input_rep[idx+1] = minus(deepcopy(input_rep[idx+1]), [1])
                    input_rep = many_mul([], input_rep, input[idx+1])

                output.append(input_rep)

            elif isinstance(input[idx], list) and len(input[idx]) > 1:
                if input[idx][0] in funcs_list:
                    if input[idx+1] == 1:
                        if input[idx][0] == 'sin':
                            input_rep[idx][0] = 'cos'
                        elif input[idx][0] == 'cos':
                            input_rep[idx][0] = 'sin'
                            input_rep[0] *= -1
                        else:
                            input_rep[idx][0] = 'cos'
                            input_rep[idx+1] = -2

                        temp = diff(input[idx][1], var)
                        
                        if temp == [0]:
                            continue
                        elif temp != [1]:
                            input_rep.append(temp)
                            input_rep.append(1)
                        
                        output.append(input_rep)
                    
                    else:
                        input_rep[0] *= input_rep[idx+1]
                        input_rep[idx+1] -= 1

                        temp = diff([1, input_rep[idx], 1], var)

                        input_rep[0] *= temp[0]
                        if input_rep[0] == 0:
                            continue

                        for m in range(1, len(temp)):
                            input_rep.append(temp[m])

                        output.append(input_rep)

                elif input[idx][0] == 'log':
                    if input_rep[idx+1] == 1:
                        inside = deepcopy(input_rep[idx][1])
                        temp = diff(input_rep[idx][1], var)
                        
                        if temp == [0]:
                            continue
                        elif temp != [1]:
                            input_rep.append(temp)
                            input_rep.append(1)

                        if len(input_rep[idx][2]) == 1 and is_digit(input_rep[idx][2][0]):
                            input_rep[0] *= (log(input_rep[idx][2][0], e) ** -1)
                            del input_rep[idx]
                            del input_rep[idx]

                        else:
                            input_rep[idx+1] = -1
                            input_rep[idx] = ['log', input_rep[idx][1], [e]]

                        input_rep = many_div([], input_rep, inside)
                        input_rep = double_bracket(input_rep)

                        output.append(input_rep)
                    
                    else:
                        input_rep[0] *= input_rep[idx+1]
                        input_rep[idx+1] -= 1

                        temp = diff([1, input_rep[idx], 1], var)

                        input_rep[0] *= temp[0]
                        if input_rep[0] == 0:
                            continue

                        for m in range(1, len(temp)):
                            input_rep.append(temp[m])

                        output.append(input_rep)

                else:
                    temp = diff(input[idx], var)

                    if temp == [0]:
                        continue

                    else:
                        input_rep[0] *= input_rep[idx+1]
                        input_rep[idx+1] -= 1

                        if input_rep[idx+1] == 0:
                            del input_rep[idx]
                            del input_rep[idx]

                        if temp != [1]:
                            input_rep.append(temp)
                            input_rep.append(1)

                    if input_rep != [0]:
                        output.append(input_rep)
            
            elif isinstance(input[idx+1], list):
                if input[idx] != [e]:
                    if len(input[idx]) == 1 and is_digit(input[idx][0]):
                        input_rep[0] *= log(input[idx][0], e)
                    else:
                        input_rep.append(['log', input[idx], [e]])
                        input_rep.append(1)
                
                temp = diff(input[idx+1], var)
                
                if temp == [0]:
                    continue

                input_rep.append(temp)
                input_rep.append(1)

                output.append(input_rep)

    if not output:
        output = [0]
    
    output = double_bracket(output)

    return output