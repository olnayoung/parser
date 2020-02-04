from math import log, sin, cos, tan, pi, e, inf
from copy import deepcopy
import math

# check if it is digit
def is_digit(value):
  try:
    float(value)
    return True
  except:
    return False

# check if it is polynomial
def is_gathered(left):

    if isinstance(left[0], list):
        return True
    else:
        return False

# used when checking differentiable
def is_same(values, epsilon):
    for n in range(len(values)):
        for m in range(n, len(values)):
            if n != m:
                if abs(float(values[n]) - float(values[m])) > epsilon*(10**3):
                    return 0

    return 1

# (x - x = 0) or (x + -x = 0) -> delete
def delete_zero(left):
    delete = []
    for n in range(len(left)):
        if left[n][0] == 0:
            delete.append(n)

    while delete:
        t = delete.pop()
        del left[t]

    return left

# [[x]] -> [x]
def double_bracket(temp):
    if is_gathered(temp) and len(temp) == 1:
        temp = temp[0]
    return temp

# variables -> sin -> cos -> tan -> log -> digit
def get_priority(var_list):
    priority = {}
    num = 0

    for n in range(len(var_list)):
        priority[var_list[n]] = num
        num += 1
    
    priority['sin'] = num
    num += 1
    priority['cos'] = num
    num += 1
    priority['tan'] = num
    num += 1
    priority['log'] = num
    num += 1

    return priority

# canonicalization when multiply
def mul_idx(one, additional, var_list):
    priority = get_priority(var_list)

    for n in range(int(len(one)/2)):
        idx = 2*n+1

        # get priority
        if is_gathered(one[idx]):
            a = multi_idx(one[idx], additional, var_list)
            if a == 0:
                return idx
            elif a == 1:
                return len(one)
        else:
            if isinstance(one[idx], list):
                if is_digit(one[idx][0]):
                    pri_1 = len(priority)
                else:
                    pri_1 = priority[one[idx][0]]
            else:
                pri_1 = priority[one[idx]]

        if is_gathered(additional):
            a = multi_idx(one[idx], additional, var_list)
            if a == 0:
                return idx
            elif a == 1:
                return len(one)
        else:
            if isinstance(additional, list):
                if is_digit(additional[0]):
                    pri_2 = len(priority)
                else:
                    pri_2 = priority[additional[0]]
            else:
                pri_2 = priority[additional]

        # get order with priority
        if pri_1 > pri_2:
            return idx

        elif pri_1 == pri_2:
            if pri_1 == len(priority):
                if one[idx][0] > additional[0]:
                    return idx

            elif pri_1 == priority['log']:
                if one[idx][2] == additional[2]:
                    if multi_idx(one[idx][1], additional[1], var_list) == 0:
                        return idx
                else:
                    if multi_idx(one[idx][2], additional[2], var_list) == 0:
                        return idx

            else:
                if multi_idx(one[idx][1], additional[1], var_list) == 0:
                    return idx

    return len(one)

# canonicalization when doing plus
def plus_idx(many, additional, var_list):
    priority = get_priority(var_list)

    if not isinstance(many, list) and not isinstance(additional, list):
        if many > additional:
            return 1
        else:
            return 0
    
    if not isinstance(many, list):
        many = [many]
    if not is_gathered(many):
        many = [many]
    if not isinstance(additional, list):
        additional = [additional]

    for n in range(len(many)):
        if len(many[n]) > len(additional):
            continue
        elif len(many[n]) < len(additional):
            return n
        
        if is_gathered(many[n][1]):
            a = multi_idx(many[n][1], additional[1], var_list)
            if a == 0:
                return n
            elif a == 1:
                return len(many)
        else:
            if isinstance(many[n][1], list):
                if is_digit(many[n][1][0]):
                    pri_1 = len(priority)
                else:
                    pri_1 = priority[many[n][1][0]]
            else:
                pri_1 = priority[many[n][1]]

        if is_gathered(additional[1]):
            a = multi_idx(many[n][1], additional[1], var_list)
            if a == 0:
                return n
            elif a == 1:
                return len(many)
        else:
            if isinstance(additional[1], list):
                if is_digit(additional[1][0]):
                    pri_2 = len(priority)
                else:
                    pri_2 = priority[additional[1][0]]
            else:
                pri_2 = priority[additional[1]]

        if pri_1 == pri_2:
            if pri_1 < priority['sin']:
                if plus_idx(many[n][2], additional[2], var_list) == 0:
                    return n

                if multi_idx(deepcopy(many[n][3:]).insert(0,many[n][0]), deepcopy(additional[3:]).insert(0, additional[0]), var_list) == 0:
                    return n
                else:
                    continue

            elif pri_1 == priority['log']:
                if many[n][1][2] == additional[1][2]:
                    first = many[n][1][1]
                    second = additional[1][1]

                else:
                    first = many[n][1][2]
                    second = additional[1][2]

            else:
                first = many[n][1][1]
                second = additional[1][1]

            if len(first) == 1 and len(second) == 1:
                if first[0] < second[0]:
                    return n
            elif len(first) == 1:
                return n
            elif len(second) == 1:
                continue
            else:
                a = multi_idx(first, second, var_list)
                if a == 0:
                    return n
                elif a == 1:
                    return len(many)

        elif pri_1 > pri_2:
            return n
    
    return len(many)

# canonicalization ex) sin(x+1) & sin(y) -> compare (x+1) & y
def multi_idx(many, additional, var_list):      # return 0: append prev, return 1: append after, return 2: same
    if many == additional:
        return 2

    if not is_gathered(many) and not is_gathered(additional):
        if len(many) > len(additional):
            return 0
        elif len(many) < len(additional):
            return 1

        a = mul_idx(many, additional[1], var_list)
        if a == len(many):
            return 1
        else:
            return 0

    if not is_gathered(many):
        many = [many]
    if not is_gathered(additional):
        additional = [additional]

    if len(many) > len(additional):
        return 0
    elif len(many) < len(additional):
        return 1
    else:
        for n in range(len(many)):
            if len(many[n]) > len(additional[n]):
                return 0
            elif len(many[n]) < len(additional[n]):
                return 1
            else:
                if multi_idx(many[n], additional[n], var_list) == len(many[n]):
                    return 1
                else:
                    return 0

    return 1


def plus_sep(left, sequence, var_list):
    check = 0
    for m in range(len(left)):
        if sequence[1:] == left[m][1:]:
            left[m][0] += sequence[0]
            check = 1
    
    if not check and sequence[0] != 0:
        num = plus_idx(left, sequence, var_list)
        left.insert(num, sequence)

    return left


def plus(left, sequence, var_list):
    if not is_gathered(left):
        left = [left]

    if not is_gathered(sequence):
        left = plus_sep(left, sequence, var_list)
    
    else:
        for n in range(len(sequence)):
            left = plus_sep(left, sequence[n], var_list)

    left = delete_zero(left)

    if not left:
        left.append([0])

    left = double_bracket(left)

    return left

def minus_sep(left, sequence, var_list):
    check = 0
    for m in range(len(left)):
        if sequence[1:] == left[m][1:]:
            left[m][0] -= sequence[0]
            check = 1
    
    if not check:
        sequence[0] *= -1
        num = plus_idx(left, sequence, var_list)
        left.insert(num, sequence)

    return left

def minus(left, sequence, var_list):
    if not is_gathered(left):
        left = [left]

    if not isinstance(sequence, list):
        sequence = [sequence]

    if not is_gathered(sequence):
        left = minus_sep(left, sequence, var_list)
    else:
        for n in range(len(sequence)):
            left = minus_sep(left, sequence[n], var_list)

    left = delete_zero(left)

    if not left:
        left.append([0])

    left = double_bracket(left)

    return left


def many_mul(ans, left, sequence, var_list):
    if is_gathered(left):
        for n in range(len(left)):
            ans = many_mul(ans, left[n], sequence, var_list)
    
    else:
        if is_gathered(sequence):
            for n in range(len(sequence)):
                ans = many_mul(ans, left, sequence[n], var_list)
        else:
            temp = multiply(left, sequence, var_list)

            if ans != []:
                ans = plus(ans, temp, var_list)

            else:
                for n in range(len(temp)):
                    ans.append(temp[n])
                
    return ans


def multiply(left, sequence, var_list):
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
            else:
                ans[a_idx+1] = plus([ans[a_idx+1]], [sequence[s_idx+1]], var_list)
            
            if ans[a_idx+1] == 0:
                del ans[a_idx]
                del ans[a_idx]

        else:
            if len(ans) == 1:
                ans.append(sequence[s_idx])
                ans.append(sequence[s_idx+1])
            else:
                num = mul_idx(ans, sequence[s_idx], var_list)
                ans.insert(num, sequence[s_idx+1])
                ans.insert(num, sequence[s_idx])

    return ans


def many_div(ans, left, sequence, var_list):
    if is_gathered(left):
        for n in range(len(left)):
            ans = many_div(ans, left[n], sequence, var_list)
    
    else:
        if len(left) != 1:
            if is_gathered(sequence):
                ans.append(left)

                if sequence in ans:
                    idx = ans.index(sequence)
                    ans[idx] -= 1
                else:
                    ans[-1].append(sequence)
                    ans[-1].append(-1)
            else:
                temp = divide(left, sequence, var_list)
                ans.append(temp)
            
        else:
            if is_gathered(sequence):
                ans.append([left[0], sequence, -1])
            else:
                temp = divide(left, sequence, var_list)
                ans.append(temp)
                
    return ans


def divide(left, sequence, var_list):
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
            else:
                ans[a_idx+1] = minus(ans[a_idx+1], sequence[s_idx+1], var_list)
            
            if ans[a_idx+1] == 0:
                del ans[a_idx]
                del ans[a_idx]

        else:
            if len(ans) == 1:
                ans.append(sequence[s_idx])
                ans.append(sequence[s_idx+1] * -1)
            else:
                num = mul_idx(ans, sequence[s_idx], var_list)
                ans.insert(num, sequence[s_idx+1] * -1)
                ans.insert(num, sequence[s_idx])

    return ans


def power(left, sequence, var_list):
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
                    ans.append(sequence[0])

            for n in range(int(len(left)/2)):
                l_idx = 2*n + 1

                if not is_gathered(sequence) and len(sequence) == 1 and is_digit(left[l_idx+1]):
                    if left[l_idx+1] * sequence[0] == 1 and left[l_idx+1] > 1 and 0 < sequence[0] < 1:
                        ans.append(left)
                        ans.append(sequence[0])
                    else:
                        ans.append(left[l_idx])
                        ans.append(left[l_idx+1] * sequence[0])
                else:
                    ans.append(left[l_idx])
                    ans.append(many_mul([], [left[l_idx+1]], sequence, var_list))

    return ans

# notation
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
                        output += ' + '
                
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


def domain_to_string(eq, var_list):
    domain = []

    for n in range(len(eq)):
        st = from_list_to_str('', eq[n])

        domain.append(st)

    return domain

# x^n, define domain with n
def add_domain(eq, in_eq, domain_1, domain_2):      # x^n -> (≠ 0, ≥ 0, x, n)
    if is_digit(domain_2):
        if domain_2 < 0 and domain_1 not in eq and domain_1 not in in_eq:
            eq.append(domain_1)
        elif 0 < domain_2 < 1 and domain_1 not in in_eq:
            in_eq.append(domain_1)
            if domain_1 in eq:
                eq.remove(domain_1)
    else:
        if len(domain_2) == 1:
            if domain_2[0] < 0 and domain_1 not in eq and domain_1 not in in_eq:
                eq.append(domain_1)
            elif 0 < domain_2[0] < 1 and domain_1 not in in_eq:
                in_eq.append(domain_1)
                if domain_1 in eq:
                    eq.remove(domain_1)
    return eq, in_eq

# differentiate
def diff(input, var, var_list):
    try:
        funcs_list = ['sin', 'cos', 'tan']
        output = [0]

        if is_gathered(input):                          # if it is polynomial
            for t in range(len(input)):
                temp = diff(input[t], var, var_list)[0]

                if temp != [0]:
                    if not output:
                        output = deepcopy(temp)
                    else:
                        output = plus(output, temp, var_list)

        else:                                           # if it is monomial
            for n in range(int(len(input)/2)):

                input_rep = deepcopy(input)
                idx = 2*n + 1

                if input[idx] == var:                   # one variable and not exponential: ex) x^3
                    if is_digit(input[idx+1]):
                        input_rep[0] *= input[idx+1]    
                        input_rep[idx+1] -= 1

                        if input_rep[idx+1] == 0:
                            del input_rep[idx]
                            del input_rep[idx]

                    else:
                        input_rep[idx+1] = minus(deepcopy(input_rep[idx+1]), [1], var_list)
                        input_rep = many_mul([], input_rep, input[idx+1], var_list)
                    output = plus(deepcopy(output), input_rep, var_list)

                elif isinstance(input[idx], list) and len(input[idx]) > 1:
                    if input[idx][0] in funcs_list:             # trigonometric functions
                        if input[idx+1] == 1:
                            if input[idx][0] == 'sin':
                                input_rep[idx][0] = 'cos'
                            elif input[idx][0] == 'cos':
                                input_rep[idx][0] = 'sin'
                                input_rep[0] *= -1
                            else:
                                input_rep[idx][0] = 'cos'
                                input_rep[idx+1] = -2

                            temp = diff(input[idx][1], var, var_list)[0]
                            follwer = deepcopy(input_rep[idx:idx+2])
                            follwer.insert(0, 1)
                            del input_rep[idx]
                            del input_rep[idx]
                            input_rep = many_mul([], deepcopy(input_rep), follwer, var_list)
                            
                            if temp == [0]:
                                continue
                            elif temp != [1]:
                                input_rep = many_mul([], deepcopy(input_rep), temp, var_list)
                        
                        else:
                            save_idx = deepcopy(input_rep[idx])
                            if is_digit(save_idx):
                                save_idx = [save_idx]

                            save_idx_1 = deepcopy(input_rep[idx+1])
                            if is_digit(save_idx_1):
                                save_idx_1 = [save_idx_1]

                            input_rep[idx+1] = minus(deepcopy(save_idx_1), [1], var_list)
                            input_rep = many_mul([], deepcopy(input_rep), save_idx_1, var_list)

                            temp = diff([1, save_idx, 1], var, var_list)[0]
                            input_rep = many_mul([], deepcopy(input_rep), temp, var_list)

                            if input_rep[0] == 0:
                                continue

                    elif input[idx][0] == 'log':            # logarithmic function
                        if input_rep[idx+1] == 1:
                            inside = deepcopy(input_rep[idx])
                            temp = diff(input_rep[idx][1], var, var_list)[0]

                            if temp == [0]:
                                continue

                            del input_rep[idx]
                            del input_rep[idx]

                            if len(inside[1]) == 1 and is_digit(inside[1][0]):
                                input_rep[0] *= (log(inside[1][0], math.e) ** -1)

                            if not (len(inside[2]) == 1 and inside[2][0] == math.e):
                                input_rep = many_mul([], deepcopy(input_rep), [1, ['log', inside[2], [math.e]], -1], var_list)

                            input_rep = many_mul([], deepcopy(input_rep), temp, var_list)
                            input_rep = many_div([], input_rep, inside[1], var_list)
                            input_rep = double_bracket(input_rep)

                        else:
                            input_rep[0] *= input_rep[idx+1]
                            input_rep[idx+1] -= 1

                            temp = diff([1, input_rep[idx], 1], var, var_list)[0]
                            input_rep = many_mul([], deepcopy(input_rep), temp, var_list)
                    
                    else:                                               # more than one variable: ex) (x+1)^3
                        temp = diff(input[idx], var, var_list)[0]

                        if temp == [0]:
                            continue

                        input_rep[0] *= input_rep[idx+1]
                        input_rep[idx+1] -= 1

                        if input_rep[idx+1] == 0:
                            del input_rep[idx]
                            del input_rep[idx]

                        input_rep = many_mul([], deepcopy(input_rep), temp, var_list)

                    output = plus(deepcopy(output), input_rep, var_list)
                
                elif isinstance(input[idx+1], list):                    # exponential function
                    if input[idx] != [math.e]:
                        if len(input[idx]) == 1 and is_digit(input[idx][0]):
                            input_rep[0] *= log(input[idx][0], math.e)
                        else:
                            input_rep.append(['log', input[idx], [math.e]])
                            input_rep.append(1)
                    
                    temp = diff(input[idx+1], var, var_list)[0]
                    
                    if temp == [0]:
                        continue
                    elif temp != [1]:
                        input_rep.append(temp)
                        input_rep.append(1)

                    output = plus(deepcopy(output), input_rep, var_list)

        if not output:
            output = [0]
        
        output = double_bracket(output)

        return output, 0

    except Exception as e:
        return 'Error', e