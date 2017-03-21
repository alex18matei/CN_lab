import math
import os.path
import sys

import matrix


KMAX = 10000
DELTA_UPPER = 10 ** 8
EPSILON = 0.000000000000000001
DATA_DIR = 'data'


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


def bicgstab(num=1):
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

    print('matricea {}: {} iteratii:'.format(num, k + 1), end=' ')
    if (math.sqrt(sum(i ** 2 for i in x)) / nb < EPSILON or
            math.sqrt(sum(i ** 2 for i in s)) / nb):
        print(x)
        print('||A*x - b|| = {}'.format(max_norm(matrix.matmulv(mat, x),
                                                 mat.b)))
    else:
        print('divergenta')



def gauss_seidel(num=1):
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

    print('matricea {}: {} iteratii:'.format(num, k + 1), end=' ')
    if delta < EPSILON:
        print(xgs)
        print('||A*xgs - b|| = {}'.format(max_norm(matrix.matmulv(mat, xgs),
                                                   mat.b)))
    else:
        print('divergenta')


if __name__ == '__main__':
    # gauss_seidel(int(sys.argv[1]))
    bicgstab(int(sys.argv[1]))
