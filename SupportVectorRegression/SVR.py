from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from numpy import diag, matrix, inf
from openopt import QP
import math

# kernel function
def kernel_value(x, y):
    a = math.exp(-1 * abs(x - y) ** 2)
    return a


def product(a, X, x):
    prod = 0.0
    for i in range(len(a)):
        prod = prod + a[i] * kernel_value(X[i], x)
    return prod

eps = 0.5
C = 100
X = []
Y = []

# taking input
tot_value = int(raw_input())
for i in range(tot_value):
    X.append(float(raw_input()))
    Y.append(float(raw_input()))

# kernel matrix
kernel = [[0.0 for i in range(2 * tot_value)] for j in range(2 * tot_value)]
for i in range(tot_value):
    for j in range(tot_value):
        kernel[i][j] = kernel_value(X[i], X[j])
        kernel[i + tot_value][j + tot_value] = kernel_value(X[i], X[j])

# negating the values for a-n'
for i in range(tot_value):
    for j in range(tot_value):
        kernel[i + tot_value][j] = (-1.0) * kernel_value(X[i], X[j])
        kernel[i][j + tot_value] = (-1.0) * kernel_value(X[i], X[j])

# coeff of 2nd term to minimize
f= [0.0 for i in range(2 * tot_value)]
for i in range(tot_value):
    f[i] = -float(Y[i]) + eps
for i in range(tot_value, 2 * tot_value):
    f[i] = float(Y[i - tot_value]) + eps

# constraints
lower_limit = [0.0 for i in range(2 * tot_value)]
upper_limit = [float(C) for i in range(2 * tot_value)]
Aeq = [1.0 for i in range(2 * tot_value)]
for i in range(tot_value, 2 * tot_value):
    Aeq[i] = -1.0
beq = 0.0

# coeff for 3rd constraint
eq = QP(np.asmatrix(kernel), np.asmatrix(f), lb = np.asmatrix(lower_limit), ub = np.asmatrix(upper_limit), Aeq = Aeq, beq = beq)
p = eq._solve('cvxopt_qp', iprint = 0)
f_optimized, x = p.ff, p.xf

support_vectors = []
support_vectors_Y = []
support_vector = []
support_vector_Y = []
coeff = []
b = 0.0

# support vectors: points such that an-an' != 0
for i in range(tot_value):
    if not((x[i] - x[tot_value + i]) == 0):
        support_vectors.append(X[i])
        support_vectors_Y.append(Y[i])
        coeff.append(x[i] - x[tot_value + i])

low = min(abs(x))
for i in range(tot_value):
    if not (abs(x[i] - x[tot_value + i] < low + 0.005)):
        support_vector.append(X[i])
        support_vector_Y.append(Y[i])


bias = 0.0
for i in range(len(X)):
    bias = bias + float(Y[i] - eps - product(coeff, support_vectors, X[i]))
bias = bias / len(X)


output_X = []
output_Y = []

output_X.append(0.0)

for i in range(350):
    output_X.append(output_X[-1] + float(10) / 300)
out_eps = []
out_eps1 = []
for i in output_X:
    output_Y.append(product(coeff, support_vectors, i) + b)
    out_eps.append(product(coeff, support_vectors, i) + b - eps)
    out_eps1.append(product(coeff, support_vectors, i) + b + eps)

plt.scatter(output_X, output_Y, c = 'red', marker = 'o')
plt.scatter(output_X, out_eps, marker = 'o')
plt.scatter(output_X, out_eps1, marker = 'o')

plt.scatter(X, Y, c = 'red', marker = '.')
print support_vector
print len(support_vectors)
plt.scatter(support_vector, support_vector_Y, c = 'yellow', marker = 'x')
print len(support_vector)
plt.show()
print low
