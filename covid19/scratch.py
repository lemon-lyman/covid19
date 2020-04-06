import numpy as np
import matplotlib.pyplot as plt


def foo(x, p_0):
    y = np.zeros(x.shape)
    for idx, _x in enumerate(x):
        for n, pp in enumerate(p_0):
            y[idx] += pp*(_x**n)
    return y

if __name__ == "__main__":
    x_0 = np.arange(100)
    y_0 = foo(x_0, [0, 0, 2])

    out = np.polyfit(x_0, y_0, 2)

    poly = np.poly1d(out)

    x_hypo = np.aran
    # fig, ax = plt.subplots()
    # ax.plot(x_0, y_0)
    # plt.show()