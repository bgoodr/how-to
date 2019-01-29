# From http://www.scipy-lectures.org/intro/scipy.html#finding-the-minimum-of-a-scalar-function

from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x**2 + 10 * np.sin(x)


x = np.arange(-10, 10, 0.1)
plt.plot(x, f(x))
plt.show()

result = optimize.minimize(f, x0=0)
print("\n{}\nresult\n{}".format('-' * 80, result))
