__author__ = 'dlamblin'
import random
import sys

if sys.version_info < ( 3, 4):
    sys.exit("This script requires Python 3.4 or newer!")


def rolls(n, low, high):
    random.seed(__author__)  # Keeping it reproducible for ease of development
    r = []
    for i in range(n):
        r.append(random.randint(low, high))
    return r


def slicedSums(m, r):
    ss, i, s = [], 0, 0
    for j in range(len(r)):
        s += r[j]
        if s >= m:
            ss.append([s, r[i:j]])
            i, s = j + 1, 0
    return ss


def main(total_rolls=20000):
    print("start up")
    rolls_list = rolls(total_rolls, 1, 6)
    sliced_sum20 = slicedSums(20, rolls_list)


main(100000)
