from typing import List

def can_form_1974(digits: List[int]) -> str:
    """
    Determines if a given list of digits can form the number 1974.
    
    Args:
    digits (List[int]): A list of integers representing the digits to check.
    
    Returns:
    str: 'YES' if the digits can form 1974, 'NO' otherwise.
    """
    # Sort the digits in ascending order
    sorted_digits = sorted(digits)
    # Check if the sorted digits are exactly [1, 9, 7, 4]
    if sorted_digits == [1, 9, 7, 4]:
        return "YES"
    # Check if there is any zero in the digits
    elif 0 in sorted_digits:
        return "NO"
    # Check if the length of the set of unique digits is less than 4
    elif len(set(sorted_digits)) < 4:
        return "NO"
    else:
        return "YES"
