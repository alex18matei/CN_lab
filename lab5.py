import copy
import math
import pprint
import numpy

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

        print('\n' + self.__str__())
        print('Iteratii: ', k)
        if delta < EPSILON:
            print('Inversa: ' + pprint.pformat(V1))
            B = numpy.dot(self.A, V1)
            n = len(B)
            m = len(B[0])
            C = [[B[i][j] - 1 if i == j else B[i][j] for j in range(m)]
                 for i in range(n)]
            print('Norma: ', norma_coloanelor(C))
        else:
            print('divergenta')


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


if __name__ == '__main__':
    n = 3
    m = 6
    A = create_matrix(n, m)
    print(A)
    # A = [[-1.086, 0.997],
    #      [0.283, -1.506],
    #      [-0.579, 1.651]]

    # A = [[-1.086, 0.283, -0.579], [0.997, -1.506, 1.651]]

    print("inversa")
    print(numpy.linalg.pinv(A))

    ReverseMatrixMethod1(A).solve()
    ReverseMatrixMethod2(A).solve()
    ReverseMatrixMethod3(A).solve()