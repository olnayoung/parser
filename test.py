from initialize import tokenize
from parsing import Parser
from extra_funcs import is_gathered
from extra_funcs import many_mul
from calculator import calcul

n = 0

f = open('/home/ny/t_codes/test_case.txt', 'r')
line = f.read().splitlines()

for n in range(len(line)):
    print('////',n+1,'////')
    print(calcul(line[n]), end='\n\n')
    n += 1
    
f.close()