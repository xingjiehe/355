import numpy as np
from queen_board import gen_winning_move, get_legal_move_points, gen_random_move
from winning_move import find_winning_moves
import random

'''
transition between the player coordinate and the program coordinate
for the size 3 with inital point 3, initial point c1
   a      b     c 
1 (0,0) (0,1) (0,2)
2 (1,0) (1,1) (1,2)
3 (2,0) (2,1) (2,2)
'''

'''
for the size 3 with inital point 3, initial point c1
the showboard would be
 *   *   Q
 *   *   *
 *   *   *
'''


# Print the main menu, welcome the player and prompt the player to choose one of four modes.
# Before the player chooses mode, ask the player to choose the size of the board and
# the original position of the board.
def main_menu():
    print("Welcome to QUEEN.\n")
    print("MAIN MENU")

    rule = input("--If you want to have a look at game rule, please enter r/R."
                 "\nElse, press 'Enter' to continue.\n")
    if rule in ['r', 'R']:
        show_rule()

    size = input("--Please choose the size of the board "
                 "\n(an integer between 2 and 26): ")

    # Check whether the size that the player input is an integer between 2 and 26
    while not (size.isdigit() and int(size) in range(2, 27)):
        print("--Wrong input, please enter one integer in the range between 2 and 26 ")
        size = input("Please choose the size of the board: ")
    size = int(size)
    show_board(None, size)
    position = input("--Please choose the position of the queen"
                     "\n(Format: letter + integer, for example: a1): ")
    # Check whether the origin position player chooses has the correct format
    while not valid_format(position, size):
        position = input("--Wrong format, please enter again,"
        "\nPlease choose the position of the queen:"
        "\n(Format: letter + integer, for example: a1): ")

    final = 'a' + str(size)
    # Deny if the player want to choose the winning field as the original position
    while position == final:
        position = input("--Wrong input, you cannot put the queen on the goal position,"
        "\nPlease choose the position of the queen:")
    position = transition(position)
    show_board(position, size)

    # Prompt the player to choose mode, or they can check the game rule or choose to quit the game.
    mode = input("--Please choose a mode.\nEnter 1 for 2 players mode,"
                 "\nenter 2 to play with computer,\nenter 3 to play with a random player."
                 "\nEnter 4 to show computer versus a random player mode."
                 "\nEnter r/R to check the game rule."
                 "\nEnter q/Q to quit.\n")
    while mode not in ['1', '2', '3', '4', 'q', 'Q', 'r', 'R']:
        mode = input("--Wrong input, please enter again.\nEnter 1 for 2 players mode,"
                 "\nenter 2 to play with computer,\nenter 3 to play with a random player."
                     "\nEnter 4 to show computer versus a random player mode."
                     "\nEnter r/R to check the game rule."
                     "\nEnter q/Q to quit.\n")
    if mode in ['r', 'R']:
        show_rule()
    return size, position, mode


# Check whether the player wants to quit, and return their decision
def quit_game(mode):
    # mode is the input that we get from the player in main_menu()
    quit = False
    if mode in ['q', 'Q']:
        quit = True
    return quit


# Run the whole game, and the function gives a brief and necessary structure for the game
def main():
    quit = False
    while not quit:
        size, position, mode = main_menu()
        quit = quit_game(mode)
        if not quit:
            if mode == '1':
                mode1(mode, size, position)
            elif mode == '2':
                mode2(mode, size, position)
            elif mode == '3':
                mode3(mode, size, position)
            elif mode == '4':
                mode4(mode, size, position)


# Mode 1: two-players mode. This mode has two players. Players input move in turns.
def mode1(mode, size, position):
    # mode is the input that we get from the player.
    # size is the size of the board
    # position is the original position that the player chooses
    player, player1, player2 = initial_set_players(mode)
    history = [position]
    end = False
    # If one player wins, the game ends.
    while not end:
        q_position = get_move(size, player, history)
        history.append(q_position)
        end = game_end(q_position, player, size)
        player = change_player(player, player1, player2)
        if not end:
            history, player = undo(history, player, player1, player2, size)


# Ask whether the player wants to undo one step, if they want to undo, we undo one step
# for the player
def undo(history, player, player1, player2, size):
    # history is a list that saves all positions that the players have chosen in order
    # player is the player who has just finish his / her step
    # player1 is the first player's name that we save for this game
    # player2 is the second player's name that we save for this game
    undo_or_not = input("--If you want to undo, enter u/U; or press 'Enter' to continue.\n")
    if undo_or_not in ['u', 'U']:
        # Undo
        history.pop()
        show_board(history[-1],size)
        print('Undone.')
        player = change_player(player, player1, player2)
        return history, player
    else:
        return history, player


# This function sets up players' name initially for each mode
def initial_set_players(mode):
    # mode is the mode that the player choose to play
    if mode == '1':
        player1 = 'Player 1'
        player2 = 'Player 2'
    elif mode == '2':
        player = go_first_or_second()
        if player == '1':
            player1 = 'Player'
            player2 = 'Computer'
        else:
            player1 = 'Computer'
            player2 = 'Player'
    elif mode == '3':
        player = go_first_or_second()
        if player == '1':
            player1 = 'Player'
            player2 = 'Random Player'
        else:
            player1 = 'Random Player'
            player2 = 'Player'
    else:
        player1 = 'Random Player'
        player2 = 'Computer'
    player = player1
    return player, player1, player2


# In mode 2 and mode 3, we ask the player if they want to play first or not
# and then we set the first player according to player's choice. This function
# return the name of the player who goes first
def go_first_or_second():
    player = input("--Do you want to go first or second?"
                    "\nEnter 1 for going first,\nenter 2 for going second.\n")
    while player not in ['1', '2']:
        player = input("--Wrong input, please enter again."
                       "\nEnter 1 for going first,\nenter 2 for going second.\n")
    return player


# Mode 2: Player versus Computer. Computer has a winning strategy and it will always
# give the smartest move (if has).
def mode2(mode, size, position):
    # mode is the mode that the player has chosen, which is 2 here
    # size is the size of the board
    # position is the original position that the player has chosen
    player, player1, player2 = initial_set_players(mode)
    history = [position]
    end = False
    while not end:
        # Player's turn
        if player == 'Player':
            q_position = get_move(size, player, history)
        # Computer's turn
        else:
            print(player + "'s turn.")
            q_position = gen_winning_move(size, history[len(history) - 1])
            show_board(q_position, size)
        history.append(q_position)
        end = game_end(q_position, player, size)
        player = change_player(player, player1, player2)
        if not end and player == 'Computer':
            history, player = undo(history, player, player1, player2, size)


# Mode 3: Player versus Random Player. Random player gives a random legal move.
def mode3(mode, size, position):
    # mode is the mode that the player has chosen, which is 3 here
    # size is the size of the board
    # position is the original position that the player has chosen
    player, player1, player2 = initial_set_players(mode)
    history = [position]
    end = False
    while not end:
        if player == 'Player':
            q_position = get_move(size, player, history)
        else:
            print(player + "'s turn.")
            q_position = gen_random_move(size,history[len(history) - 1])
            show_board(q_position,size)
        history.append(q_position)
        end = game_end(q_position, player, size)
        player = change_player(player, player1, player2)
        if not end and player == 'Random Player':
            history, player = undo(history, player, player1, player2, size)


# Mode 4: Computer versus Random Player. In this mode, the player is not involved.
# The function will show one situation that the computer plays with a random player.
# It returns the player who loses the game.
def mode4(mode, size, position):
    # mode is the mode that the player has chosen, which is 4 here
    # size is the size of the board
    # position is the original position that the player has chosen
    player, player1, player2 = initial_set_players(mode)
    history = [position]
    end = False
    while not end:
        print(player + "'s turn.")
        if player == 'Random Player':
            q_position = gen_random_move(size,history[len(history) - 1])
            show_board(q_position,size)
        else:
            q_position = gen_winning_move(size, history[len(history) - 1])
            show_board(q_position, size)
        history.append(q_position)
        end = game_end_for_test(q_position, player, size)
        player = change_player(player, player1, player2)
    return player


# When one player finish to move the Queen, or when they choose to undo,
# we change the player's turn.
def change_player(player, player1, player2):
    # player is the name of the player who has chance to play now
    # player1 is the name of the first player
    # player2 is the name of the second player
    if player == player1:
        player = player2
    else:
        player = player1
    return player


# Check if any player wins and the game ends
def game_end(q_position, player, size):
    # q_position is the position of the last postion
    # player is the name of the player who put the last position
    # size is the size of the board
    if q_position == (size - 1, 0):
        input("--" + player + " wins!\nGame end.\nPress 'Enter' to go back to the main menu.\n")
        return True
    return False


# This is a test function and is used to check whether any player wins and whether the game ends
def game_end_for_test(q_position, player, size):
    # q_position is the position of the last postion
    # player is the name of the player who put the last position
    # size is the size of the board
    if q_position == (size - 1, 0):
        print(player + " wins!\nGame end.\nPress 'Enter' to go back to the main menu.\n")
        return True
    return False


# Ask the player to enter their move and tell whether the move is legal, and return a coordinate
# format for the player's legal move
def get_move(size, player, history):
    # size is the size of the board
    # player is the name of the player who is going to play next
    # history is a list which contains all the past positions that players have chosen
    print(player + "'s turn.")
    last_position = history[len(history) - 1]
    solver(size, last_position)
    valid = False
    # Check whether the input move has proper format and is it legal
    while not valid:
        move = input("--Move format: letter + number (For example: a1)"
                          "\nPlease enter your move: ")
        valid1 = valid_format(move,size)
        if not valid1:
            print("Wrong format, please enter again.")
        else:
            q_position = transition(move)
            valid2 = valid_move(size, q_position, history)
            if not valid2:
                print("Invalid move, please enter again.")
            else:
                valid = True
    show_board(q_position, size)
    return q_position


# Show the board according to the position of the Queen
def show_board(q_position, size):
    # q_position is the last position that the Queen has been allocated
    # size is the size of the board
    queen = 1
    board = np.zeros((size, size), dtype=np.int32)
    if q_position is not None:
        board[q_position] = queen
    x = 'abcdefghijklmnopqrstuvwxyz'
    print('   ', end='')
    for i in range(size):
        print(x[i], end=' ')
    for i in range(size):
        print('\n{:>2}'.format(i + 1), end=' ')
        for j in range(size):
            if board[i, j] == queen:
                print('Q', end=' ')
            else:
                print('*', end=' ')
    print("\n")


# Check whether the format of the input move is valid
def valid_format(move, size):
    # move is the move that we get from the player
    # size is the size of the board
    x = 'abcdefghijklmnopqrstuvwxyz'
    if len(move) != 3 and len(move) != 2:
        return False
    f = move[0]
    s = move[1:]
    if f not in x[0:size]:
        return False
    if not s.isdigit():
        return False
    if int(s) not in range(1, size + 1):
        return False
    return True


# Show the game rule
def show_rule():
    print("Game Rule:\nTwo players move the queen in turns,"
          "\nwhere the movement of the queen follows the rules of chess."
          "\n(The queen can be moved horizontally / vertically / diagonally, as far as one wants."
          "\nThe queen is restricted to be moved to the left or downwards,"
          "\nor along the lower left diagonal)"
          "\nThe goal of the game is to move the queen to the winning field (the lower left corner)."
          "\nWhoever moves the queen to this field, wins the game.")
    input("--Press 'Enter' to go back to the main menu.\n")
    #main_menu()


# Transit the 'a1' format input into the coordinate format
def transition(move):
    # move is the 'a1' format move that we get from the player
    f = move[0]
    s = move[1:]
    y0 = 'abcdefghijklmnopqrstuvwxyz'.index(f)
    x0 = int(s)-1
    return (x0, y0)


# Tell whether the input is valid, that is whether it follows the rule
def valid_move(size, q_position, history):
    # size is the size of the board
    # q_position is the coordinate format of the move that we get from the player
    # history is a list of positions that players have chosen
    last = history[-1]
    valid_moves = get_legal_move_points(size, last)
    return q_position in valid_moves


# Ask the player whether they need help. If they need help, this function gives one step help
# with winning strategy.
def solver(size,position):
    # size is the size of the board
    # position is the last position that the player choose
    solver_choice = input("--Do you want a help?, enter Y/y for yes, else you will need to enter on your own.")
    if solver_choice in ["Y","y"]:
        if not find_winning_moves(size, position):
            print("No winning move in current position.")
        else:
            position = random.choice(find_winning_moves(size, position))
            print(transition_to_player(position))
    return


# This function turns the coordinate format move into a 'a1' format.
def transition_to_player(position):
    # position is the coordinate format that we get from our strategy
    row, column = position
    letter = 'abcdefghijklmnopqrstuvwxyz'[column]
    return letter + str(row + 1)

main()
