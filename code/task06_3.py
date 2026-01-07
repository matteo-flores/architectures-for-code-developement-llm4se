from typing import List

def odd_position(nums: List[int]) -> bool:
    result = True
    for i in range(len(nums)):
        if i % 2 == 1 and nums[i] % 2 == 0:
            result = False
            break
    return result
