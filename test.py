from initialize import tokenize
from parsing import Parser
from extra_funcs import is_gathered
from extra_funcs import many_mul
from calculator import calcul


input = ['-1', '3^2', '1+2', '-']

for n in range(len(input)):
    print('////',n+1,'////')
    print(calcul(input[n]), end='\n\n')