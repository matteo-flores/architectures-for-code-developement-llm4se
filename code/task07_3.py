from typing import List

def can_form_1974(digits: List[int]) -> str:
    sorted_digits = sorted(digits)
    if sorted_digits == [1, 9, 7, 4]:
        return "YES"
    elif 0 in sorted_digits:
        return "NO"
    else:
        return "YES"