import copy
import os.path

DATA_DIR = 'data'
LIMIT = 10
EPSILON = 10**(-9)


class Matrix:
    def __init__(self, fname=None):
        self.b = []
        self.diag = []
        self.non_diag = []
        self.above_limit = []
        self.fname = fname
        self.pointers = []
        if fname:
            self.parse(fname)

    def init_helpers(self):
        self.above_limit = [False, ] * self.n
        self.non_diag = [(0, -i) for i in range(1, self.n + 2)]
        self.pointers = [i for i in range(self.n + 2)]
        self.diag = [0, ] * self.n

    def verify(self):
        if self.fname is None:
            return
        for i in range(1, self.n + 1):
            starta = self.pointers[i]
            enda = self.pointers[i + 1] - 1
            if len(self.non_diag[starta:enda]) > LIMIT:
                print('Mai mult de {} elemente pe linia {} din matricea din '
                      'fisierul {}'.format(LIMIT, i, self.fname))

    def add_item(self, val, row, col):
        found = False
        for i in range(self.pointers[row], self.pointers[row + 1]):
            if self.non_diag[i][0] == 0:
                break
            elif self.non_diag[i][1] == col:
                found = True
                self.non_diag[i][0] += val
                break

        if not found:
            self.non_diag.insert(self.pointers[row], [val, col])
            for i in range(row + 1, self.n + 2):
                self.pointers[i] += 1

    def parse(self, fname):
        with open(fname) as fp:
            self.n = int(fp.readline())
            fp.readline()

            self.init_helpers()

            for n in fp:
                if n == '\n':
                    break
                self.b.append(float(n))

            for line in fp:
                n, i, j = line.split(',')
                if int(i) == int(j):
                    self.diag[int(j)] = float(n)
                else:
                    self.add_item(float(n), int(i) + 1, int(j))

    def __str__(self):
        return '{}\n{}'.format(self.non_diag, self.diag)


def matadd(A, B):
    R = copy.deepcopy(A)

    row = 0
    for elem in B.non_diag:
        if elem[0] == 0:
            row += 1
        else:
            R.add_item(elem[0], row, elem[1])

    for i, elem in enumerate(B.diag):
        R.diag[i] += elem

    return R


def matcmp(A, B):
    if A.diag != B.diag:
        print('Diag not equal')
        return False

    for elem in A.non_diag:
        start, to = (), ()
        if elem[0] == 0:
            if elem == A.non_diag[-1]:
                break

            starta = A.pointers[-elem[1]]
            enda = A.pointers[-elem[1] + 1] - 1

            startb = B.pointers[-elem[1]]
            endb = B.pointers[-elem[1] + 1] - 1

            slicea = A.non_diag[starta:enda]
            sliceb = B.non_diag[startb:endb]

            if len(slicea) != len(sliceb):
                print('Slice not equal {} {}'.format(str(slicea), str(sliceb)))
                return False

            sorteda = sorted(slicea)
            sortedb = sorted(sliceb)

            for i, e in enumerate(sorteda):
                if abs(sortedb[i][0] - e[0]) >= EPSILON:
                    print('Elems not equal')
                    return False

    return True


def matmulv(A, t):
    R = []

    for row in range(1, A.n + 1):

        starta = A.pointers[row]
        enda = A.pointers[row + 1] - 1
        res = A.diag[row - 1] * t[row - 1]
        for elem in A.non_diag[starta:enda]:
            res += elem[0] * t[elem[1]]

        R.append(res)

    return R


def matmul(A, B):
    R = Matrix()
    R.diag = []
    R.non_diag = [(0, -i) for i in range(1, A.n + 2)]
    R.pointers = [i for i in range(A.n + 2)]
    R.n = A.n

    for col in range(B.n):
        v = [0, ] * B.n
        v[col] = B.diag[col]

        for row in range(1, B.n + 1):
            start = B.pointers[row]
            end = B.pointers[row + 1] - 1
            slice = B.non_diag[start:end]
            for elem in slice:
                if elem[1] == col:
                    v[row - 1] = elem[0]


        res = matmulv(A, v)
        for row, e in enumerate(res, 1):
            if e != 0:
                if row - 1 != col:
                    R.add_item(e, row, col)
                else:
                    R.diag.append(e)

    return R


if __name__ == '__main__':
    a = Matrix(os.path.join(DATA_DIR, 'a.txt'))
    b = Matrix(os.path.join(DATA_DIR, 'b.txt'))
    aplusb = Matrix(os.path.join(DATA_DIR, 'aplusb.txt'))
    aorib = Matrix(os.path.join(DATA_DIR, 'aorib.txt'))

    R = matadd(a, b)
    print(matcmp(R, aplusb))
    S = matmul(a, b)
    print(matcmp(S, aorib))

    print(matmulv(a, [i for i in range(2017, 0, -1)]) == a.b)
    print(matmulv(b, [i for i in range(2017, 0, -1)]) == b.b)
