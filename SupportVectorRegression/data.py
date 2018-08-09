import matplotlib.pyplot as plt
import numpy as np
import math
import random
import sys

ori_stdout = sys.stdout
f = file('data.txt', 'w')
sys.stdout = f

tot_value = 350
mean = 0
variance = 0.5
lower_limit = 0
upper_limit = 10

Y = []
X = []
X.append(lower_limit)
for i in range(tot_value - 1):
    X.append(X[-1] + float(upper_limit - lower_limit) / tot_value)
for i in X:
    Y.append(math.sin(float(i)) + np.random.normal(mean, variance))

print tot_value
for i in range(len(X)):
    print(X[i])
    print(Y[i])

sys.stdout = ori_stdout
f.close()