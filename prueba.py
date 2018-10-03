import numpy as np

w = 10.0
x = 501
next_x = (x + w*(int(np.abs(x)/w)+1)) % w
print(next_x)