from initialize import tokenize
from parsing import Parser
from extra_funcs import is_gathered
from extra_funcs import many_mul
from calculator import calcul
from calculator import change_x_to_num
from extra_funcs import multiply
from extra_funcs import plus
from extra_funcs import from_list_to_str
from extra_funcs import power
from extra_funcs import many_div
from extra_funcs import divide
from extra_funcs import minus
from extra_funcs import in_eq_domain
from extra_funcs import eq_domain
from extra_funcs import diff

print(calcul('x^2^(y+20)/x+1'))

# n = 0
# correct = 0

# f = open('/home/ny/t_codes/test_case.txt', 'r')
# ff = open('/home/ny/t_codes/answer.txt', 'r')


# line = f.read().splitlines()
# answers = ff.read().splitlines()

# for n in range(len(line)):
#     print('////',n+1,'////')
#     ans = calcul(line[n])
#     print('mine:', ans, ', answer:', answers[n])

#     if ans is not 'Error' and str(ans) == answers[n]:
#         correct += 1
    
#     # if ans is not 'Error':
#     #     correct += 1
#     print()
#     n += 1
    
# f.close()

# print('total:',  correct, '/', len(line))