import math
import random

import matrix


NUM_ELEM_MAX = 61000
KMAX = 1000000


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


def power_method(A):

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

    print('Valoare Proprie: {}'.format(l))
    print('Vector Propriu: [{}, {}, ..., {}, {}]'
          .format(v[0], v[1], v[-2], v[-1]))


def main():
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


if __name__ == '__main__':
    main()
