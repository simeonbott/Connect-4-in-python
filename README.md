# Connect-4-in-python
2 Player Connect 4 in python

A machine learning based project. The objective was to create a Monte-Carlo Tree Search and an Evaluation Function, driven by a machine learning process which could be a decent challenge to a human opponent. The computer is shown all possible outcomes after the next 4 moves (2 by Yellow and 2 by Red), and it is shown each row, column and diagonal independently, and must use that information in order to determine how good it thinks that position is. At the end of each game played on the program, the computer replays the game and makes changes to its opinion on the rows, columns and diagonals appearing in the game, based on which side won or lost or drew.

Files:
Connect4.py - A connect4 GUI for two human players to play.
Connect4Computer.py - Can also have computer players play.
Training.py - An executable to generate an untrained computer player. Doesn't know anything about the game.
Training2.py - An executable to generate an untrained computer player that already know how to get 4 in a row. (its likely that further training will not improve it)

Training.py and Training2.py both create a text file containing ~4000 variable values. This file is read by Connect4Computer.py and used to calculate the ~2000 variable values used to determine the strength of each row, column and diagonal configuration. To half the number of values, I chose to recognise horizontally reflected rows, columns and diagonals as identical. In particular:

There are 7 columns (4 by reflection), each with 16 possible legal configurations. (64)
There are 6 rows, each is different due to height, and has a total 289 unique legal configurations (up to reflection). (1734)
There are 12 diagonals (6 by reflection), from shortest to longest, they have 17, 65 and 177 legal configurations. (518)

Overall this makes 2316 values, each is given a total score and total number of games.
This approach is one step removed from the naive approach of letting the computer evaluate based on all of the pieces on the board independently, where the computer would likely never discover the meaning of 4 in a row. It's likely that a more human-tactics-oriented model would surpass this one easily.

The code is designed so that the training methodology can be modified easily, but the computer will always be limited by the input information, making it unable to find correlations or patterns between different rows and diagonals. For example, a 3-in-a-row with nothing on either side on the lowest row will be recognised as a strong winning configuration, and the same structure higher up on the game board will, correctly, be identified as different, however the computer will be unable to tell whether the columns on either side of the 3-in-a-row are filled up enough, in which case the scenario would be the same after all. This problem is hard to notice when watching the computer play, because the Monte-Carlo Tree Search can help it find these patterns during a game. In this particular case, the most interesting training results would probably be derived from an evolutionary model instead of unsupervised.
