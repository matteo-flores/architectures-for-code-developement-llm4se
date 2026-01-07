from typing import List

def can_form_1974(digits: List[int]) -> str:
    """
    Determines if a given list of four digits can form the number 1974.
    
    Args:
    digits (List[int]): A list of four integers representing the digits to check.
    
    Returns:
    str: 'YES' if the digits can form 1974, 'NO' otherwise.
    """
    # Check if the length of the digits list is exactly 4
    if len(digits) != 4:
        # If not, return 'NO'
        return "NO"
    
    # Convert the list of digits into a set to remove duplicates and check if it contains all the required digits
    digit_set = set(digits)
    if digit_set == {1, 4, 7, 9}:
        # If the set contains all the required digits, return 'YES'
        return "YES"
    else:
        # Otherwise, return 'NO'
        return "NO"