from winning_move import find_winning_moves
import random


# return all the legal moves from current position(Q_position)
# the legal moves followed by the rule is directed to the final goal, and we can make any step of move 
# row, column or diagoanl, but we can't stay in the original point.
# each element in the return list is a integer tuple, formatted in the main.py
def get_legal_move_points(size, Q_position):
    # size is an integer representing board size
    # Q_position is the current queen's position
    row_number = Q_position[0]
    column_number = Q_position[1]
    row_number_change = row_number
    column_number_change = column_number
    legal_l = []

    size = size - 1
    # add all legal row
    while size >= column_number > 0:
        column_number -= 1
        legal_l.append((row_number, column_number))

    # add all legal column
    while size > row_number >= 0:
        row_number += 1
        legal_l.append((row_number, column_number_change))

    # add all legal diagonal
    while size > row_number_change >= 0 and size >= column_number_change > 0:
        legal_l.append((row_number_change + 1, column_number_change - 1))
        row_number_change += 1
        column_number_change -= 1

    # return whole row/column/diagonal
    return legal_l


# generate a winning move followed by the winning strategy
def gen_winning_move(size, Q_position):
    # generate one winning move, for computer's turn
    # if we can find the wining move, return a random winning move
    if find_winning_moves(size, Q_position):
        return random.choice(find_winning_moves(size, Q_position))
    # if we can't find the wining move, return a random move
    else:
        return gen_random_move(size, Q_position)


# generate a random move from all legal moves
def gen_random_move(size, Q_position):
    # generate one random  move, for random player
    return random.choice(get_legal_move_points(size,Q_position))
