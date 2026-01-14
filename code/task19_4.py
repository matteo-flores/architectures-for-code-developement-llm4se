from typing import List

def count_colors(colors: List[int]) -> int:
    """
    Counts the number of unique colors in a list of integers.

    Args:
    colors (List[int]): A list of integers representing the colors.

    Returns:
    int: The number of unique colors in the list.
    """
    return len(set(colors))