from typing import List

def can_form_1974(digits: List[int]) -> str:
    """
    Given a list of four digits, determine whether they can be rearranged
    to form the sequence 1974.

    Return "YES" if possible, otherwise return "NO".
    """
    target = [1, 9, 7, 4]
    return "YES" if sorted(digits) == sorted(target) else "NO"