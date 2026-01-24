from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """Parses a string of space-separated parenthesis groups and returns the maximum nesting depth for each group.

    Args:
        paren_string: A string containing one or more groups of parentheses,
                      separated by spaces. For example: "() (()) ((()))".

    Returns:
        A list of integers, where each integer represents the maximum nesting
        depth of the corresponding parenthesis group in the input string.
    """
    # Split the input string into individual parenthesis groups based on spaces.
    groups = paren_string.split()
    result = []
    # Iterate through each group of parentheses.
    for group in groups:
        max_depth = 0  # Initialize the maximum depth found so far for the current group.
        current_depth = 0  # Initialize the current nesting depth for the current group.
        # Iterate through each character in the current parenthesis group.
        for char in group:
            if char == '(':
                # If an opening parenthesis is encountered, increase the current depth.
                current_depth += 1
                # Update the maximum depth if the current depth is greater.
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                # If a closing parenthesis is encountered, decrease the current depth.
                current_depth -= 1
        # After processing all characters in a group, append its maximum depth to the result list.
        result.append(max_depth)
    return result