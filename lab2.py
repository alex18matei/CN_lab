from numpy import linalg as np
import math
import copy
import sys
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import *

eps = 10 ** (-10)
A_init = [[1, 2.5, 3], [2.5, 8.25, 15.5], [3, 15.5, 43]]
# A_init = [[1, -1, 2], [-1, 5, -4], [2, -4, 6]]
A = copy.deepcopy(A_init)


def cholesky(A):
    n = len(A)
    D = [0] * 3

    for p in range(n):
        temp_sum = 0
        for k in range(p):
            temp_sum += D[k] * A[p][k] ** 2

        D[p] = A[p][p] - temp_sum

        for i in range(p + 1, n, + 1):
            temp_sum = 0
            for k in range(p):
                temp_sum += D[k] * A[i][k] * A[p][k]

            if (abs(D[p]) > eps):
                A[i][p] = (A[i][p] - temp_sum) / D[p]
            else:
                print("nu se poate face impartirea")

    return A, D


def get_L_from_A(A):
    n = len(A)
    L = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    L = [[A[i][j] if i > j else L[i][j] for j in range(n)] for i in range(n)]
    return L


def det(D):
    return eval('*'.join(str(item) for item in D))


def direct_substitution(L, b):
    x = [0] * len(L)
    for i in range(len(L)):
        temp_sum = 0
        for j in range(i):
            temp_sum += L[i][j] * x[j]
        x[i] = b[i] - temp_sum
    return x


def invers_substitution(A, b):
    x = [0] * len(A)
    for i in range(len(A) - 1, -1, -1):

        temp_sum = 0
        for j in range(i + 1, len(A), +1):
            temp_sum += A[j][i] * x[j]
        x[i] = b[i] - temp_sum

    return x


def solve_system(A, D, b):
    z = direct_substitution(A, b)

    y = [0] * 3
    for i in range(len(D)):
        if (abs(D[i]) > eps):
            y[i] = z[i] / D[i]
        else:
            print("nu se poate face impartirea")
    # y = [z[i] / D[i] for i in range(len(D))]

    x = invers_substitution(A, y)

    return x


def norm(A, x, b):
    y = [0] * 3
    n = len(A)

    for i in range(n):
        for j in range(n):
            if i > j:
                y[i] += A[j][i] * x[j]
            else:
                y[i] += A[i][j] * x[j]

    res = 0
    for item in [x1 - x2 for (x1, x2) in zip(y, b)]:
        res += item * item

    if (math.sqrt(res) < 10 ** (-9)):
        return (math.sqrt(res))
    return None


def matmult(m1, m2):
    r = []
    m = []
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            sums = 0
            for k in range(len(m2)):
                sums = sums + (m1[i][k] * m2[k][j])
            r.append(sums)
        m.append(r)
        r = []
    return m


class GUIApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.D = None
        self.pack()
        self.create_widgets()
        self.cmd_btn_ex6()

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

        self.btn_ex4 = Button(self)
        self.btn_ex4['text'] = 'Exercitiul 4'
        self.btn_ex4['command'] = self.cmd_btn_ex4
        self.btn_ex4.pack(side='top')

        self.btn_ex5 = Button(self)
        self.btn_ex5['text'] = 'Exercitiul 5'
        self.btn_ex5['command'] = self.cmd_btn_ex5
        self.btn_ex5.pack(side='top')


        self.tab0f = Frame(self.nb)
        self.A_label = Label(self.tab0f, text="A")
        self.B_label = Label(self.tab0f, text="B")

        self.entry_A = Entry(self.tab0f)
        self.entry_b = Entry(self.tab0f)

        self.A_label.pack()
        self.entry_A.pack(expand=YES, fill=X)
        self.entry_A.insert(END, '[[1, 2.5, 3], [2.5, 8.25, 15.5], [3, 15.5, 43]]')
        self.B_label.pack()
        self.entry_b.pack(expand=YES, fill=X)
        self.entry_b.insert(END, '[6.5, 26.25, 61.5]')

        self.btn_ex6 = Button(self.tab0f)
        self.btn_ex6['text'] = 'Set input'
        self.btn_ex6['command'] = self.cmd_btn_ex6
        self.btn_ex6.pack(side='top')

        self.nb.add(self.tab0f, text='Input')


        self.tab1f = Frame(self.nb)
        self.scrolled_text1 = ScrolledText(self.tab1f, bg='white', height=10)
        self.scrolled_text1.pack()
        self.nb.add(self.tab1f, text='Exercitiul 1')

        self.tab2f = Frame(self.nb)
        self.scrolled_text2 = ScrolledText(self.tab2f, bg='white', height=10)
        self.scrolled_text2.pack()
        self.nb.add(self.tab2f, text='Exercitiul 2')

        self.tab3f = Frame(self.nb)
        self.scrolled_text3 = ScrolledText(self.tab3f, bg='white', height=10)
        self.scrolled_text3.pack()
        self.nb.add(self.tab3f, text='Exercitiul 3')

        self.tab4f = Frame(self.nb)
        self.scrolled_text4 = ScrolledText(self.tab4f, bg='white', height=10)
        self.scrolled_text4.pack()
        self.nb.add(self.tab4f, text='Exercitiul 4')

        self.tab5f = Frame(self.nb)
        self.scrolled_text5 = ScrolledText(self.tab5f, bg='white', height=10)
        self.scrolled_text5.pack()
        self.nb.add(self.tab5f, text='Exercitiul 5')

        self.nb.pack()

    def cmd_btn_ex1(self):
        self.cmd_btn_ex6()
        self.scrolled_text1.delete(1.0, END)
        self.scrolled_text1.insert(END, 'Exercitiul 1\n')
        self.scrolled_text1.insert(END, '============\n')
        self.scrolled_text1.insert(END, 'A init: {}\n'.format(self.A))
        self.A, self.D = cholesky(self.A)
        self.scrolled_text1.insert(END, 'A: {}\n'.format(self.A))
        self.scrolled_text1.insert(END, 'L: {}\n'.format(get_L_from_A(self.A)))
        self.scrolled_text1.insert(END, 'D: {}\n'.format(self.D))

    def cmd_btn_ex2(self):
        self.cmd_btn_ex6()
        self.scrolled_text2.insert(END, 'Exercitiul 2\n')
        self.scrolled_text2.insert(END, '============\n')

        if self.D is None:
            self.A, self.D = cholesky(self.A)
        # det(A) = det(D) deoarece det(L) = det(L transpus) = 1
        self.scrolled_text2.insert(END, 'Det(A): {}\n'.format(det(self.D)))

    def cmd_btn_ex3(self):
        self.cmd_btn_ex6()
        self.scrolled_text3.insert(END, '============\n')
        self.scrolled_text3.insert(END, 'A * [1, 1, 1]: {}\n'.format(matmult(self.A, [[1], [1], [1]])))

        # print("direct subs ", invers_substitution(A, [6.5, 26.25, 50.0]))

        self.scrolled_text3.insert(END, 'Exercitiul 3\n')
        self.scrolled_text3.insert(END, '============\n')
        if self.D is None:
            self.A, self.D = cholesky(self.A)
        self.scrolled_text3.insert(END, 'X: {}\n'.format(solve_system(self.A, self.D, [6.5, 26.25, 61.5])))

    def cmd_btn_ex4(self):
        self.cmd_btn_ex6()
        self.scrolled_text4.insert(END, 'Exercitiul 4\n')
        self.scrolled_text4.insert(END, '============\n')
        if self.D is None:
            self.A, self.D = cholesky(self.A)
        self.scrolled_text4.insert(END, 'Ax = b \nX:\n {}\n'.format(np.solve(A_init, [[6.5], [26.25], [61.5]])))
        self.scrolled_text4.insert(END, 'L:\n {}\n'.format(np.cholesky(A_init)))

    def cmd_btn_ex5(self):
        self.cmd_btn_ex6()
        self.scrolled_text5.insert(END, 'Exercitiul 5\n')
        self.scrolled_text5.insert(END, '============\n')
        self.scrolled_text5.insert(END, 'Norma: {}\n'.format(norm(A, [1, 1, 1], [6.5, 26.25, 61.5])))

    def cmd_btn_ex6(self):
        self.A = eval(self.entry_A.get())
        self.B = eval(self.entry_b.get())


if __name__ == '__main__':

    if sys.argv[-1] == 'nogui':

        print('\n\nExercitiul 1')
        print('============')
        A, D = cholesky(A)
        print("A: ", A)
        print("L: ", get_L_from_A(A))
        print("D: ", D)

        print('\n\nExercitiul 2')
        print('============')
        # det(A) = det(D) deoarece det(L) = det(L transpus) = 1
        print("Det(A) : ", det(D))
        # print(numpy.linalg.det(A))


        print('\n\n============')
        print("A * [1, 1, 1]: ", matmult(A, [[1], [1], [1]]))

        # print("direct subs ", invers_substitution(A, [6.5, 26.25, 50.0]))

        print('\n\nExercitiul 3')
        print('============')
        print("X : ", solve_system(A, D, [6.5, 26.25, 61.5]))

        print('\n\nExercitiul 4')
        print('============')
        print("Ax = b \nX = \n", np.solve(A_init, [[6.5], [26.25], [61.5]]))
        print("L: \n", np.cholesky(A_init))

        print('\n\nExercitiul 5')
        print('============')
        print("Norma: ", norm(A, [1, 1, 1], [6.5, 26.25, 61.5]))

    else:
        root = Tk()
        app = GUIApp(master=root)
        app.mainloop()
