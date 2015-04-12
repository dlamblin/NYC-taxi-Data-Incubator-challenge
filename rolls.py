"""Answering https://www.thedataincubator.com/challenge.html (login required).

Answers question 1 on the challenge, by generating sample fair dice rolls and
looking at statistics across these rolls.

Question was (and for my generated rolls the answers are):

Q1: You roll a fair 6-sided dice iteratively until the sum of the dice rolls
is greater than or equal to M.
What is the mean of the sum minus M when M=20? (1.6663572224285184)
What is the mean of the sum minus M when M=10000? (1.4285714285714286)
What is the mean of the number of rolls when M=20? (6.188822874118084)
What is the mean of the number of rolls when M=10000? (2856.8)
What is the standard deviation of the sum minus M when M=20? (1.4921206223381762)
What is the standard deviation of the sum minus M when M=10000? (1.1952286093343936)
What is the standard deviation of the number of rolls when M=20? (1.2261439318861245)
What is the standard deviation of the number of rolls when M=10000? (23.2793773921191)

Usage Example:

      $ python3 rolls.py

"""
__author__ = 'dlamblin'
import random
import sys

if sys.version_info < (3, 4):
    sys.exit("This script requires Python 3.4 or newer!")

import statistics


def rolls(n, low, high):
    """Rolls generates a list of rolls of integer values inclusively
    between low and high arguments.

    Args:
        :param n (int): how many rolls to generate
        :param low (int): the lowest value a roll can be
        :param high (int): the highest value a roll can be

    Returns:
        :return: list: a n-length list of integers as rolled
    """
    random.seed(__author__)  # Keeping it reproducible for ease of development
    r = []
    for i in range(n):
        r.append(random.randint(low, high))
    return r


def sliced_sums(m, r):
    """For a given value M will progress through list r and return a list of
    lists which each have the first element as the sum of the second element,
    being a minimal list from in order elements in r which sums equal to or
    more than the value M, until the elements of r are exhausted.

    The tail elements of r which do not sum to M or greater will not be
    included.

    Args:
        :param m (int): The sum which elements from r should sum to or exceed
        :param r: The random rolls as a list.

    Returns:
        :return: list: like [
            [sum_list_a, [list_a_from_elements_in_r]],
            [sum_list_b, [list_b_from_next_elements_in_r]]]
    """
    ss, i, s = [], 0, 0
    for j in range(len(r)):
        s += r[j]
        if s >= m:
            ss.append([s, r[i:j + 1]])
            i, s = j + 1, 0
    return ss


def sums(ss, inc=0):
    """Returns just the sums from the lists in the style of the sliced_sums
    list. Each sum has increment inc added to it.

    Args:
        :param ss: A list like that which the sliced_sums function returns.
        :param inc (int, optional): How much to increment each sum from the
            input.

    Returns:
        :return: A simpler list of integers representing the sums in the input
            incremented by the optional inc value.
    """
    return [x[0] + inc for x in ss]


def lens(ss):
    """Returns just the count of the rolls from the lists in the style of the
    sliced_sums list.

    Args:
        :param ss: A list like that which the sliced_sums function returns.

    Returns:
        :return: A simpler list of integers representing the count of rolls
            in the input.
    """
    return [len(x[1]) for x in ss]


def answers(string, pairs, function, sep=' '):
    """For each pair, prints an answer string formatted using the first part
    of the pair followed by the result of applying the function to the second
    part.

    Args:
        :param string: To be printed for each pair, should contain '{}'
            or '{0}'.
        :param pairs: List of pairs with the substitute and function
            parameter.
        :param function: A function applied to each pairs second part.
        :param sep (string, optional): How to separate the formatted string
            and the function result.

    Returns:
        :return:
        :rtype : none
    """
    for pair in pairs:
        print(string.format(pair[0]), function(pair[1]), sep=sep)


def main(total_rolls=20000):
    rolls_list = rolls(total_rolls, 1, 6)
    sliced_sum20 = sliced_sums(20, rolls_list)
    sums20 = sums(sliced_sum20, -20)
    roll_count20 = lens(sliced_sum20)
    sliced_sum10k = sliced_sums(10000, rolls_list)
    sums10k = sums(sliced_sum10k, -10000)
    roll_count10k = lens(sliced_sum10k)
    paired_sums = [(20, sums20), (10000, sums10k)]
    paired_rolls = [(20, roll_count20), (10000, roll_count10k)]

    answers("Mean of the sum - {0} when M is {0}:",
            paired_sums, lambda s: statistics.mean(s))
    answers("Mean of the number of rolls when M is {0}:",
            paired_rolls, lambda s: statistics.mean(s))
    answers("Standard deviation of the sum - {0} when M is {0}:",
            paired_sums, lambda s: statistics.stdev(s))
    answers("Standard deviation of the number of rolls when M is {0}:",
            paired_rolls, lambda s: statistics.stdev(s))
    answers("\nView of the rolls summing to {0}\n" +
            format("Count", ">7") + " " + format("Sum", ">7") + " Rolls\n",
            [(20, sliced_sum20), (10000, sliced_sum10k)],
            lambda ss: ''.join(
                format(len(s[1]), ">7") + " " + format(s[0], ">7") + " " +
                format(s[1]) + "\n" for s in ss)
            , sep=''
            )


main(100000)
