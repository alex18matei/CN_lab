from numpy import linalg as np


def cholesky(A):
    n = len(A)
    L = [[0 for x in range(n)] for y in range(n)]
    D = [0] * 3

    for p in range(n):
        temp_sum = 0
        for k in range(p):
            temp_sum += D[k] * L[p][k] ** 2

        D[p] = A[p][p] - temp_sum

        for i in range(n):
            temp_sum = 0
            for k in range(p):
                temp_sum += D[k] * L[i][k] * L[p][k]

            L[i][p] = (A[i][p] - temp_sum) / D[p]

    return L, D


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


def invers_substitution(L, b):
    x = [0] * len(L)
    for i in range(len(L) - 1, -1, -1):

        temp_sum = 0
        for j in range(i + 1, len(L), +1):
            temp_sum += L[i][j] * x[j]
        x[i] = b[i] - temp_sum

    return x


def solve_system(A, b):
    L, D = cholesky(A)

    z = direct_substitution(L, b)
    y = [z[i] / D[i] for i in range(len(D))]
    x = invers_substitution([list(i) for i in zip(*L)], y)

    return x


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
    A = [[1, 2.5, 3], [2.5, 8.25, 15.5], [3, 15.5, 43]]
    # A = [[1, -1, 2], [-1, 5, -4], [2, -4, 6]]
    L, D = cholesky(A)

    print('Exercitiul 1')
    print('============')
    print("A: ", A)
    print("L: ", L)
    print("D: ", D)

    print('\n\nExercitiul 2')
    print('============')
    # det(A) = det(D) deoarece det(L) = det(L transpus) = 1
    print("Det(A) : ", det(D))
    # print(numpy.linalg.det(A))

    # print(matmult(A, [[1], [1], [1]]))

    print('\n\nExercitiul 3')
    print('============')
    print("X : ", solve_system(A, [6.5, 26.25, 61.5]))

    print('\n\nExercitiul 4')
    print('============')
    print("Ax = b \nX = \n", np.solve(A, [[6.5], [26.25], [61.5]]))
    print("L: \n", np.cholesky(A))
