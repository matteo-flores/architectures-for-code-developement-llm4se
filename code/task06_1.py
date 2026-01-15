from typing import List

def odd_position(nums: List[int]) -> bool:
    for i in range(1, len(nums), 2):
        if nums[i] % 2 == 0:
            return False
    return True
