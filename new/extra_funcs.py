from math import log, sin, cos, tan, pi, e, inf
from copy import deepcopy

# check if it is digit
def is_digit(value):
  try:
    float(value)
    return True
  except:
    return False

def is_same(values, epsilon):
    for n in range(len(values)):
        for m in range(n, len(values)):
            if n != m:
                if abs(float(values[n]) - float(values[m])) > epsilon*(10**3):
                    return 0

    return 1