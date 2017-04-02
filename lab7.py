import ast              # pentru parsat expresia functiei
import os.path
import random
import sys

from math import *      # pentru functii gen sin(x) in expresia functiei

import numpy as np

DATA_DIR = 'data'
X0_DEFAULT = 1.0
XN_DEFAULT = 5.0
FINI_DEFAULT = 'x**4 - 12 * x**3 + 30 * x**2 + 12'


def read_file(fname):
    with open(os.path.join(DATA_DIR, fname)) as fp:
        x0_str, xn_str, fini_str = fp.readline().split(',', 2)

    try:
        x0, xn = eval(x0_str.strip()), eval(xn_str.strip())
        if x0 > xn:
            x0, xn = xn, x0
    except SyntaxError:
        x0, xn = X0_DEFAULT, XN_DEFAULT
        print('x0, xn incorecte: x0={}, xn={}'.format(x0, xn))

    try:
        ast.parse(fini_str.strip())
        fini = fini_str.strip()
    except SyntaxError:
        fini = FINI_DEFAULT

    return x0, xn, fini


def generate_values(x0, xn, fini, n):
    values = []
    x = x0
    for _ in range(n):
        values.append((x, eval(fini)))
        x = random.uniform(x, xn)

    x = xn
    values.append((x, eval(fini)))

    return values


def build_aitken(values):
    n = len(values)
    y = [val[1] for val in values]

    for step in range(1, n):
        prev_y = y[step - 1]
        for ddk in range(n - step):
            aux = y[step + ddk]
            y[step + ddk] = ((y[step + ddk] - prev_y) /
                             (values[step + ddk][0] - values[ddk][0]))
            prev_y = aux

    return y


def newton_interp(values):
    dd = build_aitken(values)

    def f(x):
        s = 0
        for i in range(len(values)):
            p = 1
            for j in range(i):
                p *= (x - values[j][0])
            s += dd[i] * p
        return s

    return f


def trigon_interp(values):
    n = len(values)

    T = []
    for val in values:
        row = [1, ]
        odd = True

        for j in range(1, n):
            row.append(sin(((j + 1) / 2) * val[0]) if odd
                       else cos((j / 2) * val[0]))
            odd = not odd

        T.append(row)

    T = np.matrix(T)
    Y = np.matrix([val[1] for val in values]).A1
    X = np.linalg.solve(T, Y)

    def f(x):
        s = 0
        for i, elem in enumerate(X):
            p = elem
            if i == 0:
                p *= 1
            elif i % 2 == 0:
                p *= cos((i / 2) * x)
            else:
                p *= sin(((i + 1) / 2) * x)
            s += p
        return s

    return f


def nogui_one(fname, interp_f, x):
    print()

    x0, xn, fini = read_file(fname)
    values = generate_values(x0, xn, fini, int(xn))

    ya = interp_f(values)(x)
    y = eval(fini)

    f_str = 'L^(n)' if interp_f == newton_interp else 'Tn'
    print('{}({}) = {}'.format(f_str, x, ya))
    print('|{}({}) - f({})| = {}'.format(f_str, x, x, abs(ya - y)))


def nogui():
    nogui_one('faprox1.txt', newton_interp, 2)
    nogui_one('faprox2.txt', trigon_interp, 63 * pi / 32)


def gui():
    pass


if __name__ == '__main__':
    if sys.argv[1] == 'nogui':
        nogui()
    else:
        gui()
