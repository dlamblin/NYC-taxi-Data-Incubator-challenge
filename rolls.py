__author__ = 'dlamblin'
import random
import sys

if sys.version_info < ( 3, 4):
    sys.exit("This script requires Python 3.4 or newer!")

import statistics


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
            ss.append([s, r[i:j + 1]])
            i, s = j + 1, 0
    return ss


def sums(ss, inc=0):
    return [x[0] + inc for x in ss]


def lens(ss):
    return [len(x[1]) for x in ss]


def main(total_rolls=20000):
    rolls_list = rolls(total_rolls, 1, 6)
    sliced_sum20 = slicedSums(20, rolls_list)
    sums20 = sums(sliced_sum20, -20)
    rollcount20 = lens(sliced_sum20)
    sliced_sum10k = slicedSums(10000, rolls_list)
    sums10k = sums(sliced_sum10k, -10000)
    rollcount10k = lens(sliced_sum10k)

    print("Mean of the sum - 20 when M is 20:",
          statistics.mean(sums20))

    print("Mean of the sum - 10000 when M is 10000:",
          statistics.mean(sums10k))

    print("Mean of the number of rolls when M is 20:",
          statistics.mean(rollcount20))

    print("Mean of the number of rolls when M is 10000:",
          statistics.mean(rollcount10k))

    print("Standard deviation of the sum - 20 when M is 20:",
          statistics.stdev(sums20))

    print("Standard deviation of the sum - 10000 when M is 10000:",
          statistics.stdev(sums10k))

    print("Standard deviation of the number of rolls when M is 20:",
          statistics.stdev(rollcount20))

    print("Standard deviation of the number of rolls when M is 10000:",
          statistics.stdev(rollcount10k))

    print("\nView of the rolls summing to 20")
    print(format("Count", ">7"), format("Sum", ">7"), "Rolls", sep='')
    for s in sliced_sum20:
        print(format(len(s[1]), ">8"), format(s[0], ">8"), s[1], sep='')

    print("\nView of the rolls summing to 10000")
    print(format("Count", ">7"), format("Sum", ">7"), "Rolls")
    for s in sliced_sum10k:
        print(format(len(s[1]), ">7"), format(s[0], ">7"), s[1])


main(100000)
