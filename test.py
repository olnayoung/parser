from initialize import tokenize
from parsing import Parser
from calculator import calcul
from calculator import change_x_to_num
from calculator import plot_2D
from calculator import plot_3D
from calculator import sigma
from extra_funcs import is_gathered
from extra_funcs import many_mul
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
from extra_funcs import mul_idx
from extra_funcs import plus_idx

print(mul_idx([1,'x',1,'z',1], 'y', ['x','y','z']))
# print(plus_idx([[1,'y',1]], [1,'x',1], ['x','y']))

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