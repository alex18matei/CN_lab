import math
import random
import cmath

KMAX = 10000
EPSILON = 10 ** (-10)
DELTA_UPPER = 10 ** 8


def derivata2(polynom, x):
    h = 10 ** -6
    return (-horner(polynom, x + 2 * h) +
            16 * horner(polynom, x + h) -
            30 * horner(polynom, x) +
            16 * horner(polynom, x - h) -
            horner(polynom, x - 2 * h)
            ) / (12 * h ** 2)


def horner(polynom, x):
    acc = 0
    for coef, _ in polynom:
        acc = acc * x + coef
    return acc


def calculate_polynom2(polynom, x):
    return (eval(polynom))


def unique_elem(my_list):
    final_list = []
    for i in range(len(my_list)):
        test = 1
        for j in range(i + 1, len(my_list)):
            if abs(my_list[i] - my_list[j]) < EPSILON:
                test = 0
                break
        if test == 1:
            final_list.append(my_list[i])
    return final_list


class MinFunctionMethodBase:
    def __init__(self, polynom):
        self.polynom = polynom

    def metoda_secantei(self, x0, x1):
        k = 0
        delta = 0
        while k < KMAX:

            x0_derivat = self.derivata1(x0)
            x1_derivat = self.derivata1(x1)

            if EPSILON < abs(x1_derivat - x0_derivat):
                delta = ((x1 - x0) * x1_derivat
                         ) / (x1_derivat - x0_derivat)
            else:
                delta = 10 ** (-5)

            if not EPSILON <= abs(delta) <= DELTA_UPPER:
                break

            x0 = x1
            x1 = x0 - delta
            k += 1

        if abs(delta) < EPSILON:
            if derivata2(self.polynom, x1) > 0:
                return round(x1)
        else:
            return 'divergenta'

    def solve(self):
        res = []
        for i in range(100):
            x0 = random.randint(0, 100)
            x1 = random.randint(0, 100)
            res.append(self.metoda_secantei(x0, x1))

        return list(set(res))


class MinFunctionMethod1(MinFunctionMethodBase):
    def __str__(self):
        return 'Metoda 1'

    def derivata1(self, x):
        h = 10 ** -6
        return (3 * horner(self.polynom, x) -
                4 * horner(self.polynom, x - h) +
                horner(self.polynom, x - 2 * h)
                ) / (2 * h)


class MinFunctionMethod2(MinFunctionMethodBase):
    def __str__(self):
        return 'Metoda 2'

    def derivata1(self, x):
        h = 10 ** -6
        return (- horner(polynom, x + 2 * h) +
                8 * horner(polynom, x + h) -
                8 * horner(polynom, x - h) +
                horner(polynom, x - 2 * h)
                ) / (12 * h)


class PolynomSolutionsBase:
    def __init__(self, polynom):
        self.polynom = polynom

    def derivata1(self, x):
        h = 10 ** -6
        return (- self.eval(x + 2 * h) +
                8 * self.eval(x + h) -
                8 * self.eval(x - h) +
                self.eval(x - 2 * h)
                ) / (12 * h)

    def derivata2(self, x):
        h = 10 ** -6
        return (-self.eval(x + 2 * h) +
                16 * self.eval(x + h) -
                30 * self.eval(x) +
                16 * self.eval(x - h) -
                self.eval(x - 2 * h)
                ) / (12 * h ** 2)

    def get_interval(self):
        a0 = abs(self.polynom[0][0])
        max = 0
        for (i, _) in self.polynom:
            if max < abs(i):
                max = abs(i)
        R = (a0 + max) / a0
        return [-R, R]

    def h(self, x):
        n = self.polynom[0][1]
        return (n - 1) ** 2 * self.derivata1(x) ** 2 - \
               n * (n - 1) * self.eval(x) * \
               self.derivata2(x)

    def metoda_laguerre(self, interval):
        x = random.uniform(interval[0], interval[1])
        k = 0
        delta = 0
        while k < KMAX:
            h_res = self.h(x)

            if h_res < 0:
                return
            radical = math.sqrt(h_res)

            numitor_delta = self.derivata1(x) \
                            + self.semn(self.derivata1(x)) \
                              * radical

            if abs(numitor_delta) <= EPSILON:
                return

            delta = self.polynom[0][1] * self.eval(x) / \
                    numitor_delta

            x -= delta
            k += 1

            if not EPSILON <= abs(delta) <= DELTA_UPPER:
                break

        if abs(delta) < EPSILON:
            return x
        else:
            return 'divergenta'

    def solve(self):
        output = open("output.txt", "wt")
        interval = self.get_interval()
        output.write('Interval solutii: ')
        output.write('{}\n'.format(interval))
        res = set()
        for i in range(1000):
            sol = self.metoda_laguerre(interval)
            if type(sol) is not str and sol is not None:
                res.add(sol)

        final_result = unique_elem(list(res))
        output.write('Solutii: \n')
        for result in final_result:
            output.write('{}\n'.format(result))
        return final_result


class PolynomRealSolutions(PolynomSolutionsBase):
    def __str__(self):
        return 'Radacini reale'

    def eval(self, x):
        return horner(self.polynom, x)

    def semn(self, x):
        return 1 if x >= 0 else -1


class PolynomComplexSolutions(PolynomSolutionsBase):
    def __str__(self):
        return 'Radacini complexe'

    def eval(self, x):
        c = x.real
        d = x.imag
        p = -2 * c
        q = c * c + d * d
        b0 = self.polynom[0][0]
        b1 = self.polynom[1][0] - p * b0
        for item in range(2, len(self.polynom)):
            aux = self.polynom[item][0] - p * b1 - q * b0
            b0 = b1
            b1 = aux

        return complex(b0 * (c + p) + b1, b0 * d)

    def semn(self, x):
        return 1 if x.real >= 0 else -1

    def metoda_laguerre(self, interval):

        re = random.uniform(interval[0], interval[1])
        im = random.uniform(interval[0], interval[1])
        x = complex(re, im)
        k = 0
        delta = 0
        while k < KMAX:
            h_res = self.h(x)

            radical = cmath.sqrt(h_res)

            numitor_delta = self.derivata1(x) \
                            + self.semn(self.derivata1(x)) \
                              * radical

            if abs(numitor_delta.real) <= EPSILON:
                return

            delta = self.polynom[0][1] * self.eval(x) / \
                    numitor_delta

            x -= delta
            k += 1

            if not EPSILON <= abs(delta.real) <= DELTA_UPPER:
                break

        if abs(delta.real) < EPSILON:
            return x
        else:
            return 'divergenta'


if __name__ == '__main__':
    polynoms = []
    # x^2 − 4x^ + 3
    polynoms.append([(1, 2), (-4, 1), (3, 0)])

    # x^3 − 6x^2 + 11x − 6
    polynoms.append([(1, 3), (-6, 2), (11, 1), (-6, 0)])

    # 42x^4 - 55x^3 - 42x^2 + 49x - 6
    polynoms.append([(42, 4), (-55, 3), (-42, 2), (49, 1), (-6, 0)])

    # 8x^4 - 38x^3 + 49x^2 - 22x + 3
    polynoms.append([(8, 4), (-38, 3), (49, 2), (-22, 1), (3, 0)])

    # x^4 − 6x^3 + 13x^2 − 12^x + 4
    polynoms.append([(1, 4), (-6, 3), (13, 2), (-12, 1), (4, 0)])

    # print(MinFunctionMethod1(polynom).solve())
    # print(MinFunctionMethod2(polynom).solve())

    # for polynom in polynoms:
    #     print(PolynomRealSolutions(polynom).solve())
    #     print(PolynomComplexSolutions(polynom).solve())

    # 4x^4 - 12x^3 - 12x – 4
    polynom = [(4, 4), (-12, 3), (0, 2), (-12, 1), (-4, 0)]

    # x^2 - 6x + 11
    # polynom = [(1,2), (-6, 1), (11, 0)]

    # x^4 + x^3 - 25x^2 + 41x + 66
    # polynom = [(1, 4), (1, 3), (-25, 2), (41, 1), (66, 1)]

    # x^4 - 4x^2 + 16
    # polynom = [(1, 4), (0, 3), (-4, 2), (0, 1), (16, 1)]

    print(PolynomRealSolutions(polynom).solve())
    print(PolynomComplexSolutions(polynom).solve())
