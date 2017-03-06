from numpy import linalg as np
import math
import copy


def cholesky(A):
    n = len(A)
    # L = [[1 if x == y else 0 for x in range(n)] for y in range(n)]
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

            A[i][p] = (A[i][p] - temp_sum) / D[p]
            # L[i][p] = A[i][p]
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
    y = [z[i] / D[i] for i in range(len(D))]
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


if __name__ == '__main__':
    A_init = [[1, 2.5, 3], [2.5, 8.25, 15.5], [3, 15.5, 43]]
    A = copy.deepcopy(A_init)
    # A = [[1, -1, 2], [-1, 5, -4], [2, -4, 6]]

    print("A init: ", A_init)

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
