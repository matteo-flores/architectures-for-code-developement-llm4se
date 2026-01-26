from typing import List 


def is_odd_product(a: int, b: int) -> str: 
    """Statement 
You are given integers A and B, each between 1 and 3 (inclusive). 

Determine if there is an integer C between 1 and 3 (inclusive) such that A \times B \times C is an odd number.""" 

    # The product of three integers is odd if and only if all three integers are odd. 
    # We are given that A and B are between 1 and 3. 
    # If both a and b are odd, then we can choose an odd c (1 or 3) 
    # to make the product a * b * c odd. 
    if a % 2 != 0 and b % 2 != 0: 
        return "Yes" 
    else: # If either a or b is even, then the product a * b will be even. 
        return "No"
