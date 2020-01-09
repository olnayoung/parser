# def is_digit(num):
#     return num.__class__ in [float, int]

def is_digit(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def is_oper(oper):
    return oper in ['+', '-', '*', '/']

def from_list_to_str(input):
    if type(input) == (int or float):
        return str(input)

    for n in range(len(input)):
        input[n] = str(input[n])
    output = ''.join(input)

    return output


def is_gathered(left):

    if isinstance(left[0], list):
        return True
    else:
        return False


def many_mul(ans, left, sequence, var_list):
    if is_gathered(left):
        for n in range(len(left)):
            many_mul(ans, left[n], sequence, var_list)
    
    else:
        if is_gathered(sequence):
            for n in range(len(sequence)):
                many_mul(ans, left, sequence[n], var_list)
        else:
            temp = multiply(left, sequence, var_list)

            check = 0
            if ans != []:
                for n in range(len(ans)):
                    if ans[n][1] == temp[1] and ans[n][2] == temp[2]:
                        check = 1
                        ans[n][0] += temp[0]
            if not check:
                ans.append(temp)
                
    return ans


def multiply(left, sequence, var_list):
    if isinstance(left[1], list) and isinstance(sequence[1], list):
        if left[1] == sequence[1]:
            for n in range(int(len(left[1])/2)+1):
                left[2][n] += sequence[2][n]
    elif isinstance(left[1], list) and not isinstance(sequence[1], list):
        for n in range(int(len(left)/2)+1):
            if left[1][n*2] == sequence[1]:
                left[2][n] += sequence[2]
        left[0] *= sequence[0]
    elif not isinstance(left[1], list) and isinstance(sequence[1], list):
        for n in range(int(len(sequence)/2)+1):
            if sequence[1][n*2] == left[1]:
                sequence[2][n] += left[2]
    else:
        if left[2] > 0 and sequence[2] > 0:
            if left[1] == sequence[1]:
                left[2] += sequence[2]
            else:
                if left[1] != var_list[0]:
                    temp = sequence
                    sequence = left
                    left = temp

                if not isinstance(left[1], list):
                    left[1] = [left[1]]
                    left[2] = [left[2]]
                left[1].append('*')
                left[1].append(sequence[1])
                left[2].append(sequence[2])
                left[0] *= sequence[0]

        elif left[2] > 0 and sequence[2] == 0:
            left[0] *= sequence[0]
        elif left[2] == 0 and sequence[2] > 0:
            left[0] *= sequence[0]
            left[1] = sequence[1]
            left[2] = sequence[2]
        elif left[2] == 0 and sequence[2] == 0:
            left[0] *= sequence[0]

    return left


def div(left, sequence, var_list):
    if isinstance(left[1], list) and isinstance(sequence[1], list):
        if left[1] == sequence[1]:
            for n in range(int(len(left[1])/2)+1):
                left[2][n] -= sequence[2][n]
    elif isinstance(left[1], list) and not isinstance(sequence[1], list):
        for n in range(int(len(left)/2)+1):
            if left[1][n*2] == sequence[1]:
                left[2][n] -= sequence[2]
        left[0] /= sequence[0]
    elif not isinstance(left[1], list) and isinstance(sequence[1], list):
        for n in range(int(len(sequence)/2)+1):
            if sequence[1][n*2] == left[1]:
                sequence[2][n] -= left[2]
    else:
        if left[2] > 0 and sequence[2] > 0:
            if left[1] == sequence[1]:
                left[2] -= sequence[2]
            else:
                sequence[2] *= -1
                if left[1] != var_list[0]:
                    temp = sequence
                    sequence = left
                    left = temp

                if not isinstance(left[1], list):
                    left[1] = [left[1]]
                    left[2] = [left[2]]
                left[1].append('*')
                left[1].append(sequence[1])
                left[2].append(sequence[2])
                left[0] /= sequence[0]

        elif left[2] > 0 and sequence[2] == 0:
            left[0] /= sequence[0]
        elif left[2] == 0 and sequence[2] > 0:
            left[0] /= sequence[0]
            left[1] = sequence[1]
            left[2] = sequence[2]
        elif left[2] == 0 and sequence[2] == 0:
            left[0] /= sequence[0]

    return left