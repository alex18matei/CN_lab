import math
import pprint
import random
import time


c1 = 1 / math.factorial(3)
c2 = 1 / math.factorial(5)
c3 = 1 / math.factorial(7)
c4 = 1 / math.factorial(9)
c5 = 1 / math.factorial(11)
c6 = 1 / math.factorial(13)


def ex1():
    print('Exercitiul 1')
    print('============')

    u = 10
    d = 1.0
    m = 0

    while (d + u != d):
        u = math.pow(10, -m)
        m = m + 1

    print('u = {}'.format(u))
    print('')

    return u


def ex2(u):
    print('Exercitiul 2')
    print('============')

    x = 1.0
    y = u
    z = u
    if (x + y) + z != x + (y + z):
        print(">>> ({x} + {y}) + {z} != {x} + ({y} + {z})"
              .format(x=x, y=y, z=z))
        print((x + y) + z != x + (y + z))
        print('')

    x = math.pow(10, -random.randint(1, 16))
    y = math.pow(10, -random.randint(1, 16))
    z = math.pow(10, -random.randint(1, 16))

    while (x * y) * z == x * (y * z):
        x = math.pow(10, -random.randint(1, 16))
        y = math.pow(10, -random.randint(1, 16))
        z = math.pow(10, -random.randint(1, 16))

    print(">>> ({x} * {y}) * {z} == {x} * ({y} * {z})"
          .format(x=x, y=y, z=z))
    print((x * y) * z == x * (y * z))
    print('')


def compute_polynomial(n, x):
    y = x ** 2
    p = 1
    if n == 1:
        p = x * (1 + y * (-c1 + y * c2))
    elif n == 2:
        p = x * (1 + y * (-c1 + y * (c2 - c3 * y)))
    elif n == 3:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * c4))))
    elif n == 4:
        p = x * (1 + y * (-0.166 + y * (0.00833 + y * (-c3 + y * c4))))
    elif n == 5:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * (c4 - c5 * y)))))
    elif n == 6:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * (c4 + y * (-c5 + y * c6))))))
    return p


def ex3():
    print('Exercitiul 3')
    print('============')

    nums = [random.uniform(-math.pi / 2, math.pi / 2) for x in range(10000)]

    best = {}
    best_each = [0, ] * 6
    for num in nums:
        results = [compute_polynomial(i, num) for i in range(1, 7)]
        errors = [(r, abs(res - math.sin(num)))
                  for r, res in enumerate(results, 1)]

        best_three = sorted(errors, key=lambda x: x[1])[:3]
        best[num] = best_three
        best_each[best_three[0][0] - 1] += 3
        best_each[best_three[1][0] - 1] += 2
        best_each[best_three[2][0] - 1] += 1

    # pprint.pprint(best)
    print('Cele mai bune polinoame: {}'.format(best_each))
    print('')

    nums = [random.uniform(-math.pi / 2, math.pi / 2) for x in range(100000)]
    for polynomial in range(1, 7):
        start_time = time.time()
        [compute_polynomial(polynomial, num) for num in nums]
        print("P{}: {:.5f} sec".format(polynomial, time.time() - start_time))


if __name__ == '__main__':
    u = ex1()
    ex2(u)
    ex3()
