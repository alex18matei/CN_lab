import sys
import math
import copy

KMAX = 10000
EPSILON = 10 ** (-10)
DELTA_UPPER = 10 ** 10


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


def transpusa(A):
    return [list(i) for i in zip(*A)]


def norma_liniilor(A):
    n = len(A)
    max = sum = 0
    for i in range(n):
        for j in range(n):
            sum += abs(A[i][j])
        if sum > max:
            max = sum
        sum = 0
    return max


def norma_coloanelor(A):
    n = len(A)
    max = sum = 0
    for j in range(n):
        for i in range(n):
            sum += abs(A[i][j])
        if sum > max:
            max = sum
        sum = 0
    return max


def minus(A):
    n = len(A)
    return [[-A[i][j] for j in range(n)] for i in range(n)]


def sub(A, B):
    n = len(A)
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def norm(A):
    n = len(A)
    sum = 0.0
    for i in range(n):
        for j in range(n):
            sum += A[i][j] ** 2
    return math.sqrt(sum)


class ReverseMatrixMethod1():
    def __init__(self, dim):
        self.A = self.create_matrix(dim)

    def __str__(self):
        return 'Metoda 1'

    def create_matrix(self, n):
        return [[1 if i == j else 2 if i + 1 == j else 0 for j in range(n)] for i in range(n)]

    def get_V0(self):
        n = len(self.A)
        A_transpus = transpusa(self.A)
        num = norma_liniilor(self.A) * norma_coloanelor(self.A)

        return [[A_transpus[i][j] / num for j in range(n)] for i in range(n)]

    def method(self, V0):
        n = len(self.A)
        B = (matmult(minus(self.A), V0))
        C = [[B[i][j] + 2 if i == j else B[i][j] for j in range(n)] for i in range(n)]
        return matmult(V0, C)

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
            print('Inversa: ' + str(V1))
            B = matmult(self.A, V1)
            C = [[B[i][j] - 1 if i == j else B[i][j] for j in range(n)] for i in range(n)]
            print('Norma: ', norma_coloanelor(C))
        else:
            print('divergenta')


class ReverseMatrixMethod2(ReverseMatrixMethod1):
    def __str__(self):
        return 'Metoda 2'

    def method(self, V0):
        n = len(self.A)
        B = (matmult(minus(self.A), V0))
        C = [[B[i][j] + 3 if i == j else B[i][j] for j in range(n)] for i in range(n)]
        D = matmult(B, C)
        F = [[D[i][j] + 3 if i == j else D[i][j] for j in range(n)] for i in range(n)]
        return matmult(V0, F)


class ReverseMatrixMethod3(ReverseMatrixMethod1):
    def __str__(self):
        return 'Metoda 3'

    def method(self, V0):
        n = len(self.A)
        B = (matmult(minus(V0), self.A))
        C = [[B[i][j] + 3 if i == j else B[i][j] for j in range(n)] for i in range(n)]
        D = matmult(C, C)

        E = [[B[i][j] + 1 if i == j else B[i][j] for j in range(n)] for i in range(n)]
        F = matmult(E, D)

        G = [[F[i][j] * 0.25 + 1 if i == j else F[i][j] * 0.25 for j in range(n)] for i in range(n)]
        return matmult(G, V0)


if __name__ == '__main__':
    n = 3
    reverse_matrix1 = ReverseMatrixMethod1(n)
    reverse_matrix1.solve()

    reverse_matrix2 = ReverseMatrixMethod2(n)
    reverse_matrix2.solve()

    reverse_matrix3 = ReverseMatrixMethod3(n)
    reverse_matrix3.solve()