import ast              # pentru parsat expresia functiei
import os.path
import random
import sys

import numpy as np
import matplotlib.pyplot as plt

from math import *      # pentru functii gen sin(x) in expresia functiei
from tkinter import *
from tkinter.scrolledtext import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

DATA_DIR = 'data'
X0_DEFAULT = 1.0
XN_DEFAULT = 5.0
FINI_DEFAULT = 'x**4 - 12 * x**3 + 30 * x**2 + 12'


class GUIApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.fname = StringVar()
        self.x = DoubleVar()
        self.interp_f = None
        self.fig = self.ax = self.canvas = None

        self.pack()
        self.create_widgets()

    def create_first_row(self):
        grid_cfg = {'padx': 5, 'pady': 5, 'row': 1}

        (Entry(self, textvariable=self.fname, width=35)
         .grid(column=1, **grid_cfg))

        (Button(self, text='Newton Interpolation',
                command=lambda: self.make_interp_f(0))
         .grid(column=2, **grid_cfg))

        (Button(self, text='Trigonometric Interpolation',
                command=lambda: self.make_interp_f(1))
         .grid(column=3, **grid_cfg))

    def create_second_row(self):
        grid_cfg = {'padx': 5, 'pady': 5, 'row': 2}

        (Entry(self, textvariable=self.x, width=35)
         .grid(column=1, **grid_cfg))

        (Button(self, text='Solve', command=self.solve)
         .grid(column=2, **grid_cfg))

        (Button(self, text='Plot', command=self.plot)
         .grid(column=3, **grid_cfg))

    def make_interp_f(self, which):
        self.interp_f = newton_interp if which == 0 else trigon_interp

    def solve(self):
        self.x0, self.xn, self.fini = solve_one(self.fname.get(),
                                                self.interp_f,
                                                self.x.get(),
                                                self.out_buffer)

    def plot(self):
        if not self.ax:
            self.fig, self.ax = plt.subplots()
        self.ax.clear()

        # plot f(x)
        xs = []
        ys = []

        x = self.x0
        while x <= self.xn:
            xs.append(x)
            ys.append(eval(self.fini))
            x += 0.1

        # plot interp_f(x)
        xsi = []
        ysi = []
        values = generate_values(self.x0, self.xn, self.fini, int(self.xn))

        x = self.x0
        while x <= self.xn:
            xsi.append(x)
            ysi.append(self.interp_f(values)(x))
            x += 0.1

        self.ax.clear()
        self.ax.plot(xs, ys, label='f(x)')
        self.ax.plot(xsi, ysi, label='aprox(x)')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(column=1, row=4)

    def create_widgets(self):
        self.create_first_row()
        self.create_second_row()

        self.out_buffer = ScrolledText(self, bg='white', height=10)
        self.out_buffer.grid({'row': 3, 'columnspan': 6})


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


def solve_one(fname, interp_f, x, buffer=None):
    x0, xn, fini = read_file(fname)
    values = generate_values(x0, xn, fini, int(xn))

    ya = interp_f(values)(x)
    y = eval(fini)

    f_str = 'L^(n)' if interp_f == newton_interp else 'Tn'

    if buffer is None:
        print()
        print('{}({}) = {}'.format(f_str, x, ya))
        print('|{}({}) - f({})| = {}'.format(f_str, x, x, abs(ya - y)))
    else:
        buffer.insert(END, '\n{}({}) = {}\n'.format(f_str, x, ya))
        buffer.insert(END, ('|{}({}) - f({})| = {}\n'
                            .format(f_str, x, x, abs(ya - y))))

    return x0, xn, fini


def nogui():
    solve_one('faprox1.txt', newton_interp, 2)
    solve_one('faprox2.txt', trigon_interp, 63 * pi / 32)


def gui():
    pass


def gui():
    root = Tk()
    root.geometry('800x600')
    app = GUIApp(master=root)
    app.mainloop()


if __name__ == '__main__':
    if sys.argv[-1] == 'nogui':
        nogui()
    else:
        gui()
