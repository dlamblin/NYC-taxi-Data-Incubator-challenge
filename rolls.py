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


def answers(string, pairs, function, sep=' '):
    for pair in pairs:
        print(string.format(pair[0]), function(pair[1]), sep=sep)


def main(total_rolls=20000):
    rolls_list = rolls(total_rolls, 1, 6)
    sliced_sum20 = slicedSums(20, rolls_list)
    sums20 = sums(sliced_sum20, -20)
    rollcount20 = lens(sliced_sum20)
    sliced_sum10k = slicedSums(10000, rolls_list)
    sums10k = sums(sliced_sum10k, -10000)
    rollcount10k = lens(sliced_sum10k)
    pairedsums = [(20, sums20), (10000, sums10k)]
    pairedrolls = [(20, rollcount20), (10000, rollcount10k)]

    answers("Mean of the sum - {0} when M is {0}:",
            pairedsums, lambda s: statistics.mean(s))
    answers("Mean of the number of rolls when M is {0}:",
            pairedrolls, lambda s: statistics.mean(s))
    answers("Standard deviation of the sum - {0} when M is {0}:",
            pairedsums, lambda s: statistics.stdev(s))
    answers("Standard deviation of the number of rolls when M is {0}:",
            pairedrolls, lambda s: statistics.stdev(s))
    answers("\nView of the rolls summing to {0}\n" +
            format("Count", ">7") + " " + format("Sum", ">7") + " Rolls\n",
            [(20, sliced_sum20), (10000, sliced_sum10k)],
            lambda ss: ''.join(
                format(len(s[1]), ">7") + " " + format(s[0], ">7") + " " +
                format(s[1]) + "\n" for s in ss)
            , sep=''
            )


main(100000)
