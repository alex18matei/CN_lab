import math
import random
import sys

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import *

import numpy as np
from scipy import linalg

import matrix


NUM_ELEM_MAX = 61000
KMAX = 1000000


class GUIApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.rand_rows = IntVar()
        self.power_fname = StringVar()
        self.svd_fname = StringVar()
        self.mat_rand = None
        self.mat_read = None
        self.mat_svd = None

        self.pack()
        self.create_widgets()

    def create_rand_row(self):
        grid_cfg = {'padx': 5, 'pady': 5, 'row': 1}

        (Entry(self, textvariable=self.rand_rows, width=35)
         .grid(column=1, **grid_cfg))

        (Button(self, text='Generate Matrix', command=self.gen_mat)
         .grid(column=2, **grid_cfg))

        (Button(self, text='Verify Symmetry', command=lambda: self.verify(1))
         .grid(column=3, **grid_cfg))

        (Button(self, text='Compute Vectors', command=lambda: self.compute(1))
         .grid(column=4, **grid_cfg))

    def create_read_row(self):
        grid_cfg = {'padx': 5, 'pady': 5, 'row': 2}

        (Entry(self, textvariable=self.power_fname, width=35)
         .grid(column=1, **grid_cfg))

        (Button(self, text='Read Matrix', command=lambda: self.read_mat(2))
         .grid(column=2, **grid_cfg))

        (Button(self, text='Verify Symmetry', command=lambda: self.verify(2))
         .grid(column=3, **grid_cfg))

        (Button(self, text='Compute Vectors', command=lambda: self.compute(2))
         .grid(column=4, **grid_cfg))

    def create_svd_row(self):
        grid_cfg = {'padx': 5, 'pady': 5, 'row': 3}

        (Entry(self, textvariable=self.svd_fname, width=35)
         .grid(column=1, **grid_cfg))

        (Button(self, text='Read Matrix', command=lambda: self.read_mat(3))
         .grid(column=2, **grid_cfg))

        (Button(self, text='Decompose', command=self.decompose)
         .grid(column=3, **grid_cfg))

    def create_widgets(self):

        self.create_rand_row()
        self.create_read_row()
        self.create_svd_row()

        self.out_buffer = ScrolledText(self, bg='white', height=10)
        self.out_buffer.grid({'row': 8, 'columnspan': 6})

    def gen_mat(self):
        self.mat_rand = gen_rand_mat(self.rand_rows.get())

    def read_mat(self, num):
        if num == 2:
            self.mat_read = matrix.Matrix(self.power_fname.get(), False)
        elif num == 3:
            self.mat_svd = read_mat(self.svd_fname.get())

    def decompose(self):
        if self.mat_svd is not None:
            do_svd(self.mat_svd, int(sys.argv[-1]), self.out_buffer)

    def verify(self, num):
        if num == 1:
            if self.mat_rand is not None:
                self.out_buffer.insert(END, '>>> mat_rand.is_symmetrical()\n')
                self.out_buffer.insert(END,
                                       str(self.mat_rand.is_symmetrical()) + '\n\n')
        elif num == 2:
            if self.mat_read is not None:
                self.out_buffer.insert(END, '>>> mat_read.is_symmetrical()\n')
                self.out_buffer.insert(END,
                                       str(self.mat_read.is_symmetrical()) + '\n\n')

    def compute(self, num):
        if num == 1:
            power_method(self.mat_rand, self.out_buffer)
        elif num == 2:
            power_method(self.mat_read, self.out_buffer)


def gen_rand_mat(n=501):
    """
    Returneaza o matrice patratica, rara si simetrica
    construita aleator, pentru prima parte din enunt.
    """
    A = matrix.Matrix()
    A.n = n
    A.init_helpers()

    for _ in range(NUM_ELEM_MAX):
        val = random.uniform(1, NUM_ELEM_MAX + 1)
        row = random.randrange(n)
        col = random.randrange(n)

        # pentru simetrie
        A.add_item(val, row + 1, col)
        A.add_item(val, col + 1, row)

    A.diag = [random.uniform(1, NUM_ELEM_MAX + 1) for _ in range(n)]

    return A


def power_method(A, buffer=None):

    w = [random.random() for _ in range(A.n)]

    for k in range(KMAX):
        n = 1 / math.sqrt(sum(i * i for i in w))
        v = [n * i for i in w]

        w = matrix.matmulv(A, v)
        l = sum(x1 * x2 for (x1, x2) in zip(w, v))

        def done():
            lv = [x * l for x in v]
            s = [a - b for (a, b) in zip(w, lv)]
            d = math.sqrt(sum(i * i for i in s))
            return d <= A.n * matrix.EPSILON

        if done():
            break
    else:       # nu s-a gasit
        print('Nu s-a gasit')
        return

    if buffer is None:
        print('Valoare Proprie: {}'.format(l))
        print('Vector Propriu: [{}, {}, ..., {}, {}]'
              .format(v[0], v[1], v[-2], v[-1]))
    else:
        buffer.insert(END, 'Valoare Proprie: {}\n'.format(l))
        buffer.insert(END, ('Vector Propriu: [{}, {}, ..., {}, {}]\n\n'
                            .format(v[0], v[1], v[-2], v[-1])))



def do_svd(mat, nf, buffer=None):
    if buffer is None:
        print('Descompunerea dupa valori singulare')
        print('===================================')
        print('')
    else:
        buffer.insert(END, 'Descompunerea dupa valori singulare\n')
        buffer.insert(END, '===================================\n')
        buffer.insert(END, '\n')

    A = np.array(mat)
    m, n = A.shape
    U, s, Vt = linalg.svd(A)
    S = linalg.diagsvd(s, m, n)

    smax = 0
    smin = 1000000
    for elem in s:
        if elem > 0:
            if elem < smin:
                smin = elem
            if elem > smax:
                smax = elem

    md = np.subtract(A, U.dot(S.dot(Vt)))
    try:
        ds = int(sys.argv[-1])
    except ValueError:
        ds = 2

    As = np.zeros((m, n))
    for i, elem in enumerate(s[:nf]):
        Uu = U[:, i].reshape(m, 1)
        Vtv = Vt[:, i].reshape(1, n)
        As = np.add(As, elem * (Uu.dot(Vtv)))

    if buffer is None:
        print('Valori singulare:', end=' ')
        print(s)

        print('Rang matrice: {}'.format(len([i for i in s if i > 0])))

        print('Numar de conditionare: {}'.format(smax / smin))

        print('||A - USVt||inf = {}'.format(md.max()))

        print('As')
        print(As)

        print('||A - As||inf = {}'.format(np.subtract(A, As).max()))
    else:
        buffer.insert(END, 'Valori singulare: ')
        buffer.insert(END, s)
        buffer.insert(END, '\n')

        buffer.insert(END, 'Rang matrice: ')
        buffer.insert(END, len([i for i in s if i > 0]))
        buffer.insert(END, '\n')

        buffer.insert(END, 'Numar de conditionare: ')
        buffer.insert(END, smax / smin)
        buffer.insert(END, '\n')

        buffer.insert(END, '||A - USVt||inf = ')
        buffer.insert(END, md.max())
        buffer.insert(END, '\n')

        buffer.insert(END, 'As\n')
        buffer.insert(END, As)
        buffer.insert(END, '\n')

        buffer.insert(END, '||A - As||inf = ')
        buffer.insert(END, np.subtract(A, As).max())
        buffer.insert(END, '\n')


def read_mat(fname=None):
    mat = []
    fname = 'test_svd.txt' if fname is None else fname
    with open(os.path.join('data', fname)) as fp:
        for line in fp:
            mat.append([float(i) for i in line.split()])

    return mat


def nogui():
    """
    mat_rand = gen_rand_mat()
    mat_read = matrix.Matrix('m_rar_sim_2017.txt', False)

    print('Matricea Generata')
    print('=================')
    print('>>> mat_rand.is_symmetrical()')
    print(mat_rand.is_symmetrical())
    print('')
    power_method(mat_rand)
    print('')

    print('Matricea Citita')
    print('===============')
    print('>>> mat_read.is_symmetrical()')
    print(mat_read.is_symmetrical())
    print('')
    power_method(mat_read)
    print('')
    """

    do_svd(read_mat(), int(sys.argv[-1]))


def gui():
    root = Tk()
    root.geometry('800x600')
    app = GUIApp(master=root)
    app.mainloop()


if __name__ == '__main__':
    if sys.argv[-2] == 'nogui':
        nogui()
    else:
        gui()
