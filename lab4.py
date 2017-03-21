import math
import os.path
import sys

import matrix

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.scrolledtext import *


KMAX = 10000
DELTA_UPPER = 10 ** 8
EPSILON = 0.000000000000000001
DATA_DIR = 'data'


class GUIApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.num = None

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        grid_cfg = {'padx': 5, 'pady': 5, 'row': 1}

        self.lb = Combobox(self, values=[1, 2, 3, 4])
        self.lb.grid(column=1, **grid_cfg)

        (Button(self, text='Gauss-Seidel', command=self.gs)
         .grid(column=2, **grid_cfg))

        (Button(self, text='BiCGSTAB', command=self.bicgstab)
         .grid(column=3, **grid_cfg))

        self.out_buffer = ScrolledText(self, bg='white', height=10)
        self.out_buffer.grid({'row': 8, 'columnspan': 6})

    def gs(self):
        gauss_seidel(int(self.lb.get()), self.out_buffer)
        # self.out_buffer.see(END)

    def bicgstab(self):
        bicgstab(int(self.lb.get()), self.out_buffer)
        # self.out_buffer.see(END)


def max_norm(x1, x2):
    """
    ||x||inf = max({|x1|, |x2|, ..., |xn|})

    Calculam ||x1 - x2||
    """
    res = max(zip(x1, x2), key=lambda x: abs(x[0] - x[1]))
    return abs(res[0] - res[1])


def dot(a, b):
    return sum(x1 * x2 for (x1, x2) in zip(a, b))


def vecaddv(a, b):
    return [x + y for (x, y) in zip(a, b)]


def vecmulv(a, b):
    return [x * y for (x, y) in zip(a, b)]


def vecsubv(a, b):
    return [x - y for (x, y) in zip(a, b)]


def vecmuls(v, s):
    return [x * s for x in v]


def vecadds(v, s):
    return [x + s for x in v]


def bicgstab(num=1, buffer=None):
    mat = matrix.Matrix(os.path.join(DATA_DIR,
                                     'm_rar_2017_{}.txt'.format(str(num))))

    x = [0, ] * mat.n
    nb = math.sqrt(sum(i ** 2 for i in mat.b))

    r0 = [b - e for (b, e) in zip(mat.b, matrix.matmulv(mat, x))]

    r = [b - e for (b, e) in zip(mat.b, matrix.matmulv(mat, x))]

    for k in range(KMAX):
        rho1 = dot(r0, r)

        if rho1 == 0:
            print('Method fails')
            return

        if k == 0:
            p = r
        else:
            beta = (rho1 / rho0) * (alpha / omega)
            p = vecaddv(r, vecmuls(vecsubv(p, vecmuls(v, omega)), beta))

        v = matrix.matmulv(mat, p)
        alpha = rho1 / dot(r0, v)
        s = vecsubv(r, vecmuls(v, alpha))

        x = vecaddv(x, vecmuls(p, alpha))

        if math.sqrt(sum(i ** 2 for i in s)) / nb < EPSILON:
            break

        t = matrix.matmulv(mat, s)
        omega = dot(t, s) / dot(t, t)
        x = vecaddv(x, vecmuls(s, omega))
        r = vecsubv(s, vecmuls(t, omega))

        if math.sqrt(sum(i ** 2 for i in x)) / nb < EPSILON:
            break

        rho0 = rho1

    msg = ('matricea {}: {} iteratii: '.format(num, k + 1))
    if buffer:
        buffer.insert(END, msg)
    else:
        print(msg)

    if (math.sqrt(sum(i ** 2 for i in x)) / nb < EPSILON or
            math.sqrt(sum(i ** 2 for i in s)) / nb):
        msg = ('{}\n||A*x - b|| = {}'
               .format(str(x), max_norm(matrix.matmulv(mat, x), mat.b)))
        if buffer:
            buffer.insert(END, msg)
        else:
            print(msg)
    else:
        if buffer:
            buffer.insert(END, 'divergenta\n')
        else:
            print('divergenta')


def gauss_seidel(num=1, buffer=None):
    mat = matrix.Matrix(os.path.join(DATA_DIR,
                                     'm_rar_2017_{}.txt'.format(str(num))))

    if not all(mat.diag):
        print('0 pe diagonala in matricea {}'.format(str(num)))
        return

    xgs = [0, ] * mat.n

    for k in range(KMAX):

        delta = 0

        for i in range(len(xgs)):
            s = 0

            start = mat.pointers[i + 1]
            end = mat.pointers[i + 2] - 1
            slice = mat.non_diag[start:end]

            for elem in slice:
                s += elem[0] * xgs[elem[1]]

            new_val = (mat.b[i] - s) / mat.diag[i]
            delta += (new_val - xgs[i]) ** 2
            xgs[i] = new_val

        delta = math.sqrt(delta)
        if not EPSILON <= delta <= DELTA_UPPER:
            break

    msg = ('matricea {}: {} iteratii: '.format(num, k + 1))
    if buffer:
        buffer.insert(END, msg)
    else:
        print(msg)

    if delta < EPSILON:
        msg = ('{}\n||A*xgs - b|| = {}'
               .format(str(xgs), max_norm(matrix.matmulv(mat, xgs), mat.b)))
        if buffer:
            buffer.insert(END, msg)
        else:
            print(msg)
    else:
        if buffer:
            buffer.insert(END, 'divergenta\n')
        else:
            print('divergenta')


def gui():
    root = Tk()
    root.geometry('800x600')
    app = GUIApp(master=root)
    app.mainloop()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == 'gs':
            gauss_seidel(int(sys.argv[2]))
        else:
            bicgstab(int(sys.argv[2]))
    else:
        gui()
