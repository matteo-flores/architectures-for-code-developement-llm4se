from typing import List

def count_colors(colors: List[int]) -> int:
    """
    Counts the number of unique colors in a list of integers.

    Args:
    colors (List[int]): A list of integers representing different colors.

    Returns:
    int: The count of unique colors in the list.
    """
    color_count = {}
    for color in colors:
        if color in color_count:
            color_count[color] += 1
        else:
            color_count[color] = 1
    return len(color_count)