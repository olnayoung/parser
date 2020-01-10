from initialize import tokenize
from parsing import Parser
from extra_funcs import is_gathered
from extra_funcs import many_mul
from calculator import calcul

n = 0
correct = 0

f = open('/home/ny/t_codes/test_case.txt', 'r')
ff = open('/home/ny/t_codes/answer.txt', 'r')
line = f.read().splitlines()
answers = ff.read().splitlines()

for n in range(len(line)):
    print('////',n+1,'////')
    ans = calcul(line[n])
    print('mine:', ans, ', answer:', answers[n])

    if ans is not 'Error' and str(ans) == answers[n]:
        correct += 1
    print()
    n += 1
    
f.close()

print('total:',  correct, '/', len(line))