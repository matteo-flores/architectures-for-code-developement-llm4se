def odd_position(nums):
    if len(nums) < 2:
        return True
    for i in range(1, len(nums), 2):
        if nums[i] % 2 == 0:
            return False
    return True