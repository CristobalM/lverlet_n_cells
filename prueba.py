import numpy as np

w = 10.0
x = 501
next_x = (x + w*(int(np.abs(x)/w)+1)) % w
print(next_x)

a = np.linspace(1, 11, 10)
b = np.copy(a)
b[0]  = 1000
print(a)
print(b)