from math import log, sin, cos, tan, pi, e

# def is_digit(num):
#     return num.__class__ in [float, int]

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


def plus(left, sequence):
    delete = []

    if not is_gathered(left):
        left = [left]

    if not is_gathered(sequence):
        check = 0
        for m in range(len(left)):
            if sequence[1:] == left[m][1:]:
                left[m][0] += sequence[0]
                check = 1

                if left[m][0] == 0:
                    delete.append(m)

                continue
        
        if not check:
            left.append(sequence)
    
    else:
        for n in range(len(sequence)):
            check = 0
            for m in range(len(left)):
                if sequence[n][1:] == left[m][1:]:
                    left[m][0] += sequence[n][0]
                    check = 1

                    if left[m][0] == 0:
                        delete.append(m)
                    
                    continue
            
            if not check:
                left.append(sequence[n])

    while delete:
        t = delete.pop()
        del left[t]

    if not left:
        left.append([0])

    return left


def minus(left, sequence):
    delete = []

    if not is_gathered(left):
        left = [left]

    if not is_gathered(sequence):
        check = 0
        for m in range(len(left)):
            if sequence[1:] == left[m][1:]:
                left[m][0] -= sequence[0]
                check = 1

                if left[m][0] == 0:
                    delete.append(m)
                
                continue
        
        if not check:
            sequence[0] *= -1
            left.append(sequence)
    
    else:
        for n in range(len(sequence)):
            check = 0
            for m in range(len(left)):
                if sequence[n][1:] == left[m][1:]:
                    left[m][0] -= sequence[n][0]
                    check = 1

                    if left[m][0] == 0:
                        delete.append(m)
                    
                    continue
            
            if not check:
                sequence[0] *= -1
                left.append(sequence[n])

    while delete:
        t = delete.pop()
        del left[t]

    if not left:
        left.append([0])

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
    ans.append(left[0] * sequence[0])

    for n in range(1, len(left)):
        ans.append(left[n])

    for n in range(int(len(sequence)/2)):
        s_idx = 2*n+1

        if sequence[s_idx] in ans:
            a_idx = ans.index(sequence[s_idx])

            if is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
                ans[a_idx+1] += sequence[s_idx+1]
            elif not is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
                ans[a_idx+1] = plus(ans[a_idx+1], [sequence[s_idx+1]])
            elif is_digit(ans[a_idx+1]) and not is_digit(sequence[s_idx+1]):
                ans[a_idx+1] = plus([ans[a_idx+1]], sequence[s_idx+1])
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
            # ans.append([1])

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
    ans.append(left[0] / sequence[0])

    for n in range(1, len(left)):
        ans.append(left[n])

    for n in range(int(len(sequence)/2)):
        s_idx = 2*n+1

        if sequence[s_idx] in ans:
            a_idx = ans.index(sequence[s_idx])

            if is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
                ans[a_idx+1] -= sequence[s_idx+1]
            elif not is_digit(ans[a_idx+1]) and is_digit(sequence[s_idx+1]):
                ans[a_idx+1] = minus(ans[a_idx+1], [sequence[s_idx+1]])
            elif is_digit(ans[a_idx+1]) and not is_digit(sequence[s_idx+1]):
                ans[a_idx+1] = minus([ans[a_idx+1]], sequence[s_idx+1])
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
        ans.append([1, left, sequence])
    else:
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