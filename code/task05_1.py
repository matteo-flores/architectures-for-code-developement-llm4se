def count_common(words):
    """ Write a function to count the most common words in a dictionary. """
    # Check if the input is a dictionary
    if not isinstance(words, dict):
        raise ValueError("Input must be a dictionary")
    
    # Extract all words from the dictionary values
    all_words = []
    for value in words.values():
        if isinstance(value, str):
            all_words.extend(value.split())
        elif isinstance(value, list):
            all_words.extend(value)
    
    # Count the occurrences of each word
    word_counts = Counter(all_words)
    
    # Find the most common word(s)
    most_common = word_counts.most_common(1)
