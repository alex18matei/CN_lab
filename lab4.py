import math
import os.path

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


def solve(num=1):
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
    solve(1)
