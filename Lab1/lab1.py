import math
import pprint
import random
import sys
import time

import numpy as np
import matplotlib.pyplot as plt


from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)
from matplotlib.figure import Figure

c1 = 1 / math.factorial(3)
c2 = 1 / math.factorial(5)
c3 = 1 / math.factorial(7)
c4 = 1 / math.factorial(9)
c5 = 1 / math.factorial(11)
c6 = 1 / math.factorial(13)


def ex1():
    print('Exercitiul 1')
    print('============')

    u = 10
    d = 1.0
    m = 0

    while (d + u != d):
        u = math.pow(10, -m)
        m = m + 1

    print('u = {}'.format(u))
    print('')

    return u


def ex2(u):
    print('Exercitiul 2')
    print('============')

    for_gui = []

    x = 1.0
    y = u
    z = u
    if (x + y) + z != x + (y + z):
        print(">>> ({x} + {y}) + {z} != {x} + ({y} + {z})"
              .format(x=x, y=y, z=z))
        print((x + y) + z != x + (y + z))
        print('')

    for_gui.append((x, y, z))

    x = math.pow(10, -random.randint(1, 16))
    y = math.pow(10, -random.randint(1, 16))
    z = math.pow(10, -random.randint(1, 16))

    while (x * y) * z == x * (y * z):
        x = math.pow(10, -random.randint(1, 16))
        y = math.pow(10, -random.randint(1, 16))
        z = math.pow(10, -random.randint(1, 16))

    print(">>> ({x} * {y}) * {z} == {x} * ({y} * {z})"
          .format(x=x, y=y, z=z))
    print((x * y) * z == x * (y * z))
    print('')

    for_gui.append((x, y, z))

    return for_gui


def compute_polynomial(n, x):
    y = x ** 2
    p = 1
    if n == 1:
        p = x * (1 + y * (-c1 + y * c2))
    elif n == 2:
        p = x * (1 + y * (-c1 + y * (c2 - c3 * y)))
    elif n == 3:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * c4))))
    elif n == 4:
        p = x * (1 + y * (-0.166 + y * (0.00833 + y * (-c3 + y * c4))))
    elif n == 5:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * (c4 - c5 * y)))))
    elif n == 6:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * (c4 + y * (-c5 + y * c6))))))
    return p


def ex3():
    print('Exercitiul 3')
    print('============')

    nums = [random.uniform(-math.pi / 2, math.pi / 2) for x in range(10000)]

    best = {}
    best_each = [0, ] * 6
    for num in nums:
        results = [compute_polynomial(i, num) for i in range(1, 7)]
        errors = [(r, abs(res - math.sin(num)))
                  for r, res in enumerate(results, 1)]

        best_three = sorted(errors, key=lambda x: x[1])[:3]
        best[num] = best_three
        best_each[best_three[0][0] - 1] += 3
        best_each[best_three[1][0] - 1] += 2
        best_each[best_three[2][0] - 1] += 1

    # pprint.pprint(best)
    print('Cele mai bune polinoame: {}'.format(best_each))
    print('')

    nums = [random.uniform(-math.pi / 2, math.pi / 2) for x in range(100000)]
    for polynomial in range(1, 7):
        start_time = time.time()
        [compute_polynomial(polynomial, num) for num in nums]
        print("P{}: {:.5f} sec".format(polynomial, time.time() - start_time))

    return best_each


class GUIApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.canvas = None
        self.ax = None

    def create_widgets(self):
        self.nb = Notebook(self)
        self.nb.enable_traversal()

        self.btn_ex1 = Button(self)
        self.btn_ex1['text'] = 'Exercitiul 1'
        self.btn_ex1['command'] = self.cmd_btn_ex1
        self.btn_ex1.pack(side='top')

        self.btn_ex2 = Button(self)
        self.btn_ex2['text'] = 'Exercitiul 2'
        self.btn_ex2['command'] = self.cmd_btn_ex2
        self.btn_ex2.pack(side='top')

        self.btn_ex3 = Button(self)
        self.btn_ex3['text'] = 'Exercitiul 3'
        self.btn_ex3['command'] = self.cmd_btn_ex3
        self.btn_ex3.pack(side='top')

        self.tab1f = Frame(self.nb)
        self.scrolled_text = ScrolledText(self.tab1f, bg='white', height=10)
        self.scrolled_text.pack()
        self.nb.add(self.tab1f, text='Exercitiile 1 si 2')

        self.tab3f = Frame(self.nb)
        self.nb.add(self.tab3f, text='Exercitiul 3')

        self.nb.pack()

    def cmd_btn_ex1(self):
        self.u = ex1()
        self.scrolled_text.insert(END, 'Exercitiul 1\n')
        self.scrolled_text.insert(END, '============\n')
        self.scrolled_text.insert(END, 'u = {}\n\n'.format(self.u))

    def cmd_btn_ex2(self):
        if self.u is None:
            self.u = ex1()

        ex2_res = ex2(self.u)

        self.scrolled_text.insert(END, 'Exercitiul 2\n')
        self.scrolled_text.insert(END, '============\n')
        x, y, z = ex2_res[0]
        self.scrolled_text.insert(END,
                                  ('>>> ({x} + {y}) + {z} != {x} + ({y} + {z})\n'
                                   .format(x=x, y=y, z=z)))
        self.scrolled_text.insert(END, str((x + y) + z != x + (y + z)))
        self.scrolled_text.insert(END, '\n\n')
        x, y, z = ex2_res[1]
        self.scrolled_text.insert(END,
                                  ('>>> ({x} * {y}) * {z} == {x} * ({y} * {z})\n'
                                   .format(x=x, y=y, z=z)))
        self.scrolled_text.insert(END, str((x * y) * z == x * (y * z)))
        self.scrolled_text.insert(END, '\n\n')

    def cmd_btn_ex3(self):
        best_each = ex3()
        n = np.arange(len(best_each))
        w = 0.35

        if not self.ax:
            self.fig, self.ax = plt.subplots()
        self.ax.clear()
        rects1 = self.ax.bar(n, best_each, w, color='r')
        self.ax.set_ylabel('Scor')
        self.ax.set_xticklabels(range(0, 7))

        if not self.canvas:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab3f)
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


if __name__ == '__main__':
    if sys.argv[-1] == 'nogui':
        u = ex1()
        ex2(u)
        ex3()
    else:
        root = Tk()
        app = GUIApp(master=root)
        app.mainloop()
