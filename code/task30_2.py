from typing import List

def get_max_triples(n):
    """Calculates the maximum number of triples whose sum is divisible by 3."""
    if n < 3:
        return 0

    # Precompute the sequence a_i = i^2 - i + 1 for i from 1 to n.
    a = [i * i - i + 1 for i in range(1, n + 1)]
    # Determine the remainder when each element is divided by 3.
    remainders = [x % 3 for x in a]

    count0 = remainders.count(0)
    count1 = remainders.count(1)
    count2 = remainders.count(2)

    triples = 0

    # Combinations of three numbers with the same remainder modulo 3.
    # This uses the combination formula nC3 = n * (n-1) * (n-2) / 6.
    triples += count0 * (count0 - 1) * (count0 - 2) // 6
    triples += count1 * (count1 - 1) * (count1 - 2) // 6
    triples += count2 * (count2 - 1) * (count2 - 2) // 6

    # Combinations of three numbers with remainders 0, 1, and 2.
    # The sum of such a triple will be divisible by 3.
    triples += count0 * count1 * count2

    return triples
