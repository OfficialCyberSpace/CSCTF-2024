from challenge.out import enc, R
from math import prod
import numpy as np

def value_in_list(n):
    return sum(int(i) for i in np.base_repr(n, base=3))

flag = ''
for i in range(355):
    if i%5 == 0:
        flag += chr(enc[i//5] ^ prod([value_in_list(_) for _ in R[i//5]]))
print(flag)
