import math
import copy
import random
import pprint
import numpy
import sys

KMAX = 10000
EPSILON = 10 ** (-10)
DELTA_UPPER = 10 ** 8


def derivata2(polynom, x):
    h = 10 ** -6
    return (-calculate_polynom(polynom, x + 2 * h) +
            16 * calculate_polynom(polynom, x + h) -
            30 * calculate_polynom(polynom, x) +
            16 * calculate_polynom(polynom, x - h) -
            calculate_polynom(polynom, x - 2 * h)
            ) / (12 * h ** 2)


def calculate_polynom(polynom, x):
    res = 0
    for tuple in polynom:
        res += tuple[0] * x ** tuple[1]
    return res


def calculate_polynom2(polynom, x):
    return (eval(polynom))


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
        return (3 * calculate_polynom(self.polynom, x) -
                4 * calculate_polynom(self.polynom, x - h) +
                calculate_polynom(self.polynom, x - 2 * h)
                ) / (2 * h)


class MinFunctionMethod2(MinFunctionMethodBase):
    def __str__(self):
        return 'Metoda 2'

    def derivata1(self, x):
        h = 10 ** -6
        return (- calculate_polynom(polynom, x + 2 * h) +
                8 * calculate_polynom(polynom, x + h) -
                8 * calculate_polynom(polynom, x - h) +
                calculate_polynom(polynom, x - 2 * h)
                ) / (12 * h)


if __name__ == '__main__':
    # x^2 − 4x^ + 3
    polynom = [(1, 2), (-4, 1), (3, 0)]
    # x^4 − 6x^3 + 13x^2 − 12^x + 4
    polynom = [(1, 4), (-6, 3), (13, 2), (-12, 1), (4, 0)]

    print(MinFunctionMethod1(polynom).solve())
    print(MinFunctionMethod2(polynom).solve())
