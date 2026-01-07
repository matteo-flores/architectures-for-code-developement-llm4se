from typing import List

def odd_position(nums: List[int]) -> bool:
    """
    Check if every odd index (1-based) contains an odd number.
    
    Args:
    nums (List[int]): A list of integers.
    
    Returns:
    bool: True if every odd index contains an odd number, False otherwise.
    """
    if len(nums) == 0:
        return True
    if len(nums) == 1:
        return True
    for i in range(1, len(nums), 2):
        if nums[i] % 2 == 0:
            return False
    return True
