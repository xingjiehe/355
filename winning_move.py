

# Given size of the board and the position, the function returns a list of positions that can go to the input pos
def find_parents(size, pos):
    # size is an integer representing board size
    # pos is a tuple of the position
    parents = []
    (row_number, column_number) = pos
    row_number_copy = row_number
    column_number_copy = column_number

    # add the positions to the right of input pos
    while 0 <= column_number < size - 1:
        column_number += 1
        parents.append((row_number, column_number))

    # add the positions to the up of input pos
    while 0 < row_number <= size - 1:
        row_number -= 1
        parents.append((row_number, column_number_copy))

    # add all positions to the up and right diagonally
    while 0 < row_number_copy <= size - 1 and 0 <= column_number_copy < size - 1:
        row_number_copy -= 1
        column_number_copy += 1
        parents.append((row_number_copy, column_number_copy))

    return parents


# When the values of a dictionary is a list containing many tuples,
# the function concatenates all the tuples into a list and return it.
def value_of_dictionary(dict):
    # dic is the dict to be calculated
    tuples = []
    for value in dict.values():
        tuples.extend(value)
    return tuples


# Note that the goal position for queen is in the bottom left corner,
# and the player can only move the queen to the left, down or diagonal(left & down) direction
# Therefore, the column, row and diagonal(up and right) of the goal position(8a) are hot positions
# If we search diagonally(from bottom left to upwards), we can know 6b and 7c are cold positions
# since any move from these two positions will go to hot positions.
# Using this pattern, we can observe every position for it is hot or cold.
# And a corresponding cold position that any hot position can go to to win the game.

# In this game the goal position is always the bottom left corner, so the diagonal search starts here,
# goes upwards until reach the border, and then go to right until reach the border
def find_hot_cold_position(size):
    # size is an integer representing board size
    diagonal_search_start = []
    for i in range(size - 1, -1, -1):
        diagonal_search_start.append((i, 0))
    for i in range(1, size):
        diagonal_search_start.append((0, i))

    queen_pos = diagonal_search_start.pop(0)
    queen_parents = find_parents(size, queen_pos)
    cold_parents_dict = {queen_pos: queen_parents}
    tuples = value_of_dictionary(cold_parents_dict)
    for search_pos in diagonal_search_start:
        while True:
            if search_pos not in tuples:
                cold_parents_dict[search_pos] = find_parents(size, search_pos)
                tuples = value_of_dictionary(cold_parents_dict)
            if search_pos[0] + 1 < size and search_pos[1] + 1 < size:
                search_pos = (search_pos[0] + 1, search_pos[1] + 1)
            else:
                break
    return cold_parents_dict


def find_winning_moves(size, pos):
    cold_parents_dict = find_hot_cold_position(size)
    winning_move = []
    for move, parents in cold_parents_dict.items():
        if pos in parents:
            winning_move.append(move)
    return winning_move
