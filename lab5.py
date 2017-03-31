import copy
import math
import pprint
import numpy
import sys

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.scrolledtext import *

KMAX = 10000
EPSILON = 10 ** (-10)
DELTA_UPPER = 10 ** 10


def matmult(m1, m2):
    r = []
    m = []
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            sums = 0
            for k in range(len(m1[0])):
                sums = sums + (m1[i][k] * m2[k][j])
            r.append(sums)
        m.append(r)
        r = []
    return m


def transpusa(A):
    return [list(i) for i in zip(*A)]


def norma_liniilor(A):
    n = len(A)
    m = len(A[0])
    max = sum = 0
    for i in range(n):
        for j in range(m):
            sum += abs(A[i][j])
        if sum > max:
            max = sum
        sum = 0
    return max


def norma_coloanelor(A):
    n = len(A)
    m = len(A[0])
    max = sum = 0
    for j in range(m):
        for i in range(n):
            sum += abs(A[i][j])
        if sum > max:
            max = sum
        sum = 0
    return max


def minus(A):
    n = len(A)
    m = len(A[0])
    return [[-A[i][j] for j in range(m)] for i in range(n)]


def sub(A, B):
    n = len(A)
    m = len(A[0])
    C = [[0] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            C[i][j] = A[i][j] - B[i][j]
    return C


def norm(A):
    n = len(A)
    m = len(A[0])
    sum = 0.0
    for i in range(n):
        for j in range(m):
            sum += A[i][j] ** 2
    return math.sqrt(sum)


def create_matrix(n, m):
    return [[1 if i == j else 2 if i + 1 == j else 0 for j in range(m)]
            for i in range(n)]


class ReverseMatrixMethodBase:
    def __init__(self, A):
        self.A = A

    def get_V0(self):

        A_transpus = transpusa(self.A)
        num = norma_liniilor(self.A) * norma_coloanelor(self.A)
        n = len(A_transpus)
        m = len(A_transpus[0])
        return [[A_transpus[i][j] / num for j in range(m)] for i in range(n)]

    def solve(self):
        V1 = self.get_V0()
        k = 0

        delta = 0
        while k < KMAX:

            V0 = copy.deepcopy(V1)
            V1 = self.method(V0)

            delta = norma_liniilor(sub(V1, V0))
            if not EPSILON <= delta <= DELTA_UPPER:
                break
            k += 1

        msg = ('\n' + self.__str__() + '\n')
        msg += ('Iteratii: {}\n'.format(k))
        if delta < EPSILON:
            msg += ('Inversa: {}\n'.format(pprint.pformat(V1)))
            B = numpy.dot(self.A, V1)
            n = len(B)
            m = len(B[0])
            C = [[B[i][j] - 1 if i == j else B[i][j] for j in range(m)]
                 for i in range(n)]
            msg += ('Norma: {}\n'.format(norma_coloanelor(C)))

            # B = numpy.dot(V1, self.A)
            # n = len(B)
            # m = len(B[0])
            # C = [[B[i][j] - 1 if i == j else B[i][j] for j in range(m)]
            #      for i in range(n)]
            # msg += ('Norma2: {}\n'.format(norma_coloanelor(C)))
        else:
            msg += ('divergenta')
        return msg


class ReverseMatrixMethod1(ReverseMatrixMethodBase):
    def __str__(self):
        return 'Metoda 1'

    def method(self, V0):
        n = len(self.A)
        B = numpy.dot(minus(self.A), V0)
        n = len(B)
        m = len(B[0])
        C = [[B[i][j] + 2 if i == j else B[i][j] for j in range(m)]
             for i in range(n)]
        return matmult(V0, C)


class ReverseMatrixMethod2(ReverseMatrixMethodBase):
    def __str__(self):
        return 'Metoda 2'

    def method(self, V0):
        n = len(self.A)
        B = (matmult(minus(self.A), V0))
        C = [[B[i][j] + 3 if i == j else B[i][j] for j in range(n)]
             for i in range(n)]
        D = matmult(B, C)
        F = [[D[i][j] + 3 if i == j else D[i][j] for j in range(n)]
             for i in range(n)]
        return matmult(V0, F)


class ReverseMatrixMethod3(ReverseMatrixMethodBase):
    def __str__(self):
        return 'Metoda 3'

    def method(self, V0):
        B = (matmult(minus(V0), self.A))

        n = len(B)
        m = len(B[0])
        C = [[B[i][j] + 3 if i == j else B[i][j] for j in range(m)]
             for i in range(n)]
        D = matmult(C, C)

        E = [[B[i][j] + 1 if i == j else B[i][j] for j in range(m)]
             for i in range(n)]
        F = matmult(E, D)

        n = len(F)
        m = len(F[0])
        G = [[F[i][j] * 0.25 + 1 if i == j else F[i][j] * 0.25
              for j in range(m)]
             for i in range(n)]
        return matmult(G, V0)


class GUIApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.num = None
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        grid_cfg = {'padx': 2, 'pady': 2, 'row': 1}

        self.lb = Combobox(self, values=[1, 2, 3])
        self.lb.grid(column=3, **grid_cfg)
        self.lb.insert(0, '1')

        self.n_label = Label(self, text="n").grid(column=0, **grid_cfg)
        self.entry_n = Entry(self)
        self.entry_n.grid(column=1, **grid_cfg)
        self.entry_n.insert(END, 3)
        self.m_label = Label(self, text="m").grid(column=0, **{'row': 2})
        self.entry_m = Entry(self)
        self.entry_m.insert(END, 3)
        self.entry_m.grid(column=1, **{'row': 2})

        (Button(self, text='Run', command=self.cmd_btn)
         .grid(column=4, **grid_cfg))

        self.out_buffer = ScrolledText(self, bg='white', height=20)
        self.out_buffer.grid({'row': 8, 'columnspan': 6})

    def cmd_btn(self):
        A = create_matrix(int(self.entry_n.get()), int(self.entry_m.get()))
        function = 'ReverseMatrixMethod' + self.lb.get() + '(A).solve()'
        self.out_buffer.insert(END, eval(function))


def gui():
    root = Tk()
    root.geometry('800x600')
    app = GUIApp(master=root)
    app.mainloop()


if __name__ == '__main__':

    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        m = int(sys.argv[2])
        A = create_matrix(n, m)
        print(A)

        # n > m
        A = [[-1.086, 0.997],
             [0.283, -1.506],
             [-0.579, 1.651]]

        # m > n
        A = [[-1.086, 0.283, -0.579], [0.997, -1.506, 1.651]]

        A = [[1, 1, -1 ],
        [2, 3, -1],
        [1, 4, 5]]

        print("inversa")
        print(numpy.linalg.pinv(A))

        print(ReverseMatrixMethod1(A).solve())
        print(ReverseMatrixMethod2(A).solve())
        print(ReverseMatrixMethod3(A).solve())
    else:
        gui()
