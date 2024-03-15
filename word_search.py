LEFT_TO_RIGHT = 1
RIGHT_TO_LEFT = -1

def is_outside_list(letter_list, index):
    """
    (list, num) -> bool
    Indicates whether the index is out of bounds with regards to the length of
    the list
    >>> is_outside_list(['A', 'B'], 2)
    True
    >>> is_outside_list(['A', 'B'], 1)
    False
    >>> is_outside_list(['A', 'B'], -1)
    True
    """
    # return True if the index is out of the list or if it is negative
    return not 0 <= index < len(letter_list)


def letter_positions(letter_list, character):
    """
    (list, str) -> list
    Returns all the positive indices where the given character is found in the
    list
    >>> letter_positions(['A', 'B'], 'A')
    [0]
    >>> letter_positions(['A', 'B', 'A'], 'A')
    [0, 2]
    >>> letter_positions(['A', 'B', 'A'], 'C')
    []
    """
    position_list = []
    for i in range(len(letter_list)):
        if character == letter_list[i]:
            position_list.append(i)
    return position_list


def valid_word_pos_direction(letter_list, word, index, direction):
    """
    (list, str, num, +/-1) -> bool
    Validates if a word is found at a specific location at a specified
    direction
    >>> valid_word_pos_direction(['A', 'I', 'B', 'M'], 'IBM', 1, 1)
    True
    >>> valid_word_pos_direction(['A', 'I', 'B', 'M'], 'IA', 1, -1)
    True
    >>> valid_word_pos_direction(['A', 'I', 'B', 'M'], 'IAM', 1, -1)
    False
    """
    first_letter = letter_positions(letter_list, word[0])
    if not index in first_letter:
        return False

    for j in range(len(first_letter)):
        for i in range(len(word)):
            if index == first_letter[j]:
                # increase the indices in a given direction and compare if 
                # each letter in the list is equal to the one in the word  
                new_index = first_letter[j] + i * direction
                if is_outside_list(letter_list, new_index) or \
                    letter_list[new_index] != word[i]:
                    return False
    return True


def direction_word_given_position(letter_list, word, index):
    """
    (list, str, num) -> list
    Searches in both directions to find the given word
    >>> direction_word_given_position(['A', 'B', 'C'], 'AB', 1)
    []
    >>> direction_word_given_position(['A', 'B', 'C'], 'AB', 0)
    [1]
    >>> direction_word_given_position(['A', 'B', 'C'], 'BA', 1)
    [-1]
    """
    # word is found with the given direction
    if valid_word_pos_direction(letter_list, word, index, LEFT_TO_RIGHT) and \
        valid_word_pos_direction(letter_list, word, index, RIGHT_TO_LEFT):
        return [-1,1] 
    elif valid_word_pos_direction(letter_list, word, index, LEFT_TO_RIGHT):
        return [1] 
    elif valid_word_pos_direction(letter_list, word, index, RIGHT_TO_LEFT):
        return [-1] 
    # return an empty list if the word is not found
    else: 
        return []


def position_direction_word(letter_list, word):
    """
    (list, str) -> list
    Returns a list of positions and directions of the word
    >>> position_direction_word(['A', 'D', 'C', 'D', 'D', 'C'], 'CD')
    [[2, -1], [2, 1], [5, -1]]
    >>> position_direction_word(['A', 'C', 'D', 'D', 'C'], 'DC')
    [[2, -1], [3, 1]]
    >>> position_direction_word(['A', 'D', 'C'], 'DC')
    [[1, 1]]
    """
    # find all the indices of the first character of the word in the list
    index = letter_positions(letter_list, word[0])
    position_direction = []
    new_pos_dir = []

    for i in range(len(index)):
        # if the word is found at a given position
        if direction_word_given_position(letter_list, word, index[i]) != []:
            direction = direction_word_given_position(letter_list, word, 
                index[i])
            for j in range(len(direction)):
                # append position and direction to the sublist
                new_pos_dir.append(index[i])
                new_pos_dir.append(direction[j])
                # append the sub-list to the final list
                position_direction.append(new_pos_dir)
                # reset the temporary list for the next iteration
                new_pos_dir = []
            else:
                position_direction = position_direction
    return position_direction


def cross_word_position_direction(bool_letter_list, length_word, index, 
    direction):
    """
    (list, num, num, +/-1) -> None
    Replaces the value of the items in bool_letter_list at the indicated index 
    and direction by the value True
    >>> bool_letter_list = [False, False]
    >>> cross_word_position_direction(bool_letter_list, 1, 0, 1)
    >>> bool_letter_list
    [True, False]
    >>> bool_letter_list = [False, False]
    >>> cross_word_position_direction(bool_letter_list, 1, 1, -1)
    >>> bool_letter_list
    [False, True]
    >>> bool_letter_list = [False, False, True]
    >>> cross_word_position_direction(bool_letter_list, 1, 1, -1)
    >>> bool_letter_list
    [False, True, True]
    """
    for i in range(length_word):
        bool_letter_list[index + i * direction] = True


def cross_word_all_position_direction(bool_letter_list, length_word, 
    list_position_direction):
    """
    (list, num, list) -> None
    For each pair of position and direction, the function calls 
    cross_word_position_direction to update bool_letter_list
    >>> bool_letter_list = [False, False]
    >>> cross_word_all_position_direction(bool_letter_list, 1, [[0, 1]])
    >>> bool_letter_list
    [True, False]
    >>> bool_letter_list = [False, False, False]
    >>> cross_word_all_position_direction(bool_letter_list, 2, [[1, -1]])
    >>> bool_letter_list
    [True, True, False]
    >>> bool_letter_list = [False, False, False, False, False]
    >>> cross_word_all_position_direction(bool_letter_list, 2, [[1, -1], [3,1]])
    >>> bool_letter_list
    [True, True, False, True, True]
    """
    for sub_list in range(len(list_position_direction)):
        index = list_position_direction[sub_list][0]
        direction = list_position_direction[sub_list][1]
        cross_word_position_direction(bool_letter_list, length_word, index, 
            direction)


def find_magic_word(letter_list, bool_letter_list):
    """
    (list, list) -> str
    Goes through letter_list from left to right and grouping all the 
    characters where their corresponding value in bool_letter_list is False
    to construct the magic word
    >>> find_magic_word(['A', 'B', 'C'], [True, False, True])
    'B'
    >>> find_magic_word(['A', 'B', 'C', 'D'], [True, False, True, False])
    'BD'
    >>> find_magic_word(['A', 'B'], [True, True])
    ''
    """
    if len(letter_list) != len(bool_letter_list):
        raise ValueError('Both lists should have the same size')
    
    magic_word = []
    for i in range(len(letter_list)):
        if not bool_letter_list[i]:
            magic_word.append(letter_list[i])   
    return ''.join(magic_word)
    

def word_search(letter_list, word_list):
    """
    (list, list) -> str
    Finds and crosses out all the words in the list, returns the magic word
    >>> word_search(['A', 'B', 'C', 'D'], ['ABC'])
    'D'
    >>> word_search(['A', 'B', 'O', 'C', 'D'], ['AB', 'DC'])
    'O'
    >>> word_search(['A', 'B', 'C'], ['ABC'])
    ''
    """
    bool_letter_list = [False] * len(letter_list)
    for word in word_list:
        list_position_direction = position_direction_word(letter_list, word)
        length_word = len(word)
        cross_word_all_position_direction(bool_letter_list, length_word, 
            list_position_direction)
    magic_word = find_magic_word(letter_list, bool_letter_list)
    return magic_word


def word_search_main(letters, words):
    """
    (str, str) -> str
    Converts letters into a list, creates word_list from words and returns the
    magic word
    >>> word_search_main('batmandnaironman', 'Batman-ANd')
    'IRONMAN'
    >>> word_search_main('loveyouthreethousand', 'Love-U-Three-Thousand')
    'YO'
    >>> word_search_main('hellopythonsjc++world', 'Python-C++-JS')
    'HELLOWORLD'
    """
    letter_list = list(letters.upper())
    word_list = list(words.upper().split('-'))
    magic_word = word_search(letter_list, word_list)
    return magic_word