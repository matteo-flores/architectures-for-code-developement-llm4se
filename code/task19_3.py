from typing import List

def count_colors(colors: List[int]) -> int:
    """Counts the number of unique colors in a list of integers.

    Args:
      colors (List[int]): A list of integers representing different colors.

    Returns:
      int: The number of unique colors in the list.
    """
    color_count = {}
    for color in colors:
        color_count[color] = color_count.get(color, 0) + 1
    return len(color_count)