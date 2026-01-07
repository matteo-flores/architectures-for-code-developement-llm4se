from typing import List

def can_form_1974(digits: List[int]) -> str:
    # Step 1: Sort the input list of digits
    sorted_digits = sorted(digits)

    # Step 2: Check if the sorted list contains the sequence 1974
    if sorted_digits == [1, 4, 7, 9]:
        return "YES"

    # Step 4: If the sequence is not found and the list contains a 0, return "NO"
    if 0 in digits:
        return "NO"

    # Step 5: If the sequence is not found and the list does not contain a 0, return "YES"
    return "YES"