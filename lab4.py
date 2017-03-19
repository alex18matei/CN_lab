import math
import os.path

import matrix


KMAX = 10000
DELTA_UPPER = 10 ** 8


def max_norm(x1, x2):
    """
    ||x||inf = max({|x1|, |x2|, ..., |xn|})

    Calculam ||x1 - x2||
    """
    return max(zip(x1, x2), key=lambda x: abs(x[0] - x[1]))

def one_matrix(num=1):
    mat = matrix.Matrix(os.path.join(matrix.DATA_DIR,
                                     'testa.txt'))
                                     # 'm_rar_2017_{}.txt'.format(str(num))))

    if not all(mat.diag):
        print('0 pe diagonala in matricea {}'.format(str(num)))
        return

    xgs = [0, ] * mat.n
    print(mat.non_diag)

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

        print(xgs)
        print(delta)
        delta = math.sqrt(delta)
        print(delta)
        if not matrix.EPSILON <= delta <= DELTA_UPPER:
            break

    print('matricea {}: {} iteratii:'.format(num, k + 1), end=' ')
    if delta < matrix.EPSILON:
        print(xgs)
    else:
        print('divergenta')


if __name__ == '__main__':
    one_matrix(4)
