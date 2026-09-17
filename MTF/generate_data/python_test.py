import math
import numpy as np
from sympy import sin, cos, pi
import sympy

k=100
a=0
b=0
for i in range(1,k+1):
    a += sympy.sin(2*sympy.pi*i/k)
    b += sympy.sin(4*sympy.pi*i/k)
print(a)
print(b)
# print(math.sin(2*np.pi))
# print(np.sin(2*np.pi))

# print(sin(2*pi))