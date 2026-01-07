from typing import List

def is_odd_product(a: int, b: int) -> str:
    """
    Determines whether the product of two integers is odd.
    
    Args:
    a (int): The first integer.
    b (int): The second integer.
    
    Returns:
    str: A string indicating whether the product is odd ("Yes") or even ("No").
    """
    # Check if either integer is 1
    if a == 1 or b == 1:
        return "Yes"
    # Check if both integers have the same parity (both odd or both even)
    elif a % 2 == b % 2:
        return "No"
    else:
        return "Yes"