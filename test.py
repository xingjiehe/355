from main import mode4
# please comment the last line "main()" in the file main.py before executing this file

comp_win = 0
total_game = 0
for time in range(5): # iterate the whole experiment five times (each case five times) to make sure the test is reliable
    loser_list = []
    # iterate all possible size of board
    for size in range(2, 27):
        for row in range(size):
            for column in range(size):
                # iterate every possible starting position of queen
                if not(row == size - 1 and column == 0):
                    # if the position is not the goal position
                    # add this constraint because the queen starting position cannot be goal position
                    position = (row, column)
                    loser = mode4('4', size, position)
                    loser_list.append(loser)
    comp_win += loser_list.count('Random Player')
    total_game += len(loser_list)
print("The computer that uses the best possible winning strategy wins " + str(comp_win) + ' times out of ' + str(total_game) + 'games.')
print("The computer wins " + '{:.2f}'.format(comp_win * total_game) + ' percent of the time.')

# Result:
# The computer that uses the best possible winning strategy wins 29485times out of 30875 games.
# The computer wins 95.90 percent of the time.
