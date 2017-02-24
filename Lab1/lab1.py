import math
import random
import time


def ex1():
    u = 10
    d = 1.0
    m = 0

    while (d + u != d):
        u = math.pow(10, -m)
        m = m + 1

    print(u)
    return u


def ex2(u):
    x = 1.0
    y = u
    z = u
    if (x + y) + z != x + (y + z):
        print("adunare neasociativa")

    x = math.pow(10, -random.randint(1, 16))
    y = math.pow(10, -random.randint(1, 16))
    z = math.pow(10, -random.randint(1, 16))

    while (x * y) * z == x * (y * z):
        x = math.pow(10, -random.randint(1, 16))
        y = math.pow(10, -random.randint(1, 16))
        z = math.pow(10, -random.randint(1, 16))
    else:
        print("inmultire neasociativa ", x, y, z)


c1 = 1 / math.factorial(3)
c2 = 1 / math.factorial(5)
c3 = 1 / math.factorial(7)
c4 = 1 / math.factorial(9)
c5 = 1 / math.factorial(11)
c6 = 1 / math.factorial(13)


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
        p = x * (1 + y * (-0.1666 + y * (0.00833 + y * (-c3 + y * c4))))
    elif n == 5:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * (c4 - c5 * y)))))
    elif n == 6:
        p = x * (1 + y * (-c1 + y * (c2 + y * (-c3 + y * (c4 + y * (-c5 + y * c6))))))
    return p


def ex3():
    number_list = [random.uniform(-math.pi / 2, math.pi / 2)
                   for x in range(10000)]
    count = {i: 0 for i in range(1, 7)}

    for number in number_list:
        results = [compute_polynomial(i, number) for i in range(1, 7)]
        errors = [abs(res - math.sin(number)) for res in results]

        best_polynomial = errors.index(min(errors)) + 1
        count[best_polynomial] += 1
    print(count)

    number_list = [random.uniform(-math.pi / 2, math.pi / 2)
                   for x in range(100000)]
    for polynomial in range(1, 7):
        start_time = time.time()
        for number in number_list:
            compute_polynomial(polynomial, number)
        print("polynomial {}: {}"
              .format(str(polynomial), str(time.time() - start_time)))


if __name__ == '__main__':
    u = ex1()
    ex2(u)
    ex3()
