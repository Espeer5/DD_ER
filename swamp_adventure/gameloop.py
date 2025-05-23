################################################################################
#                                                                              #
#  gameloop.py                                                                 #
#                                                                              #
#  This module contains the main game loop for the Swamp Adventure text-based  #
#  adventure game.                                                             #
#                                                                              #
#  Author:  Edward Speer                                                       #
#  Revised: 04/14/2025                                                         #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import time

import block_print as bp
from gameboard import GameBoard

################################################################################
#  CONSTANTS                                                                   #
################################################################################

BOARD_WIDTH  = 10
BOARD_HEIGHT = 5

################################################################################
#  FUNCTIONS                                                                   #
################################################################################

"""
game_loop()

The main game loop for the Swamp Adventure text-based adventure game. Each turn
the player is presented with a prompt and their input is processed. The game
continues until the player reaches one of the possible ends of the game.
"""
def game_loop():
    # Print the game intro
    bp.print_ascii_art("shrek")
    bp.print_msg("intro")

    # Initialize the game board
    gb = GameBoard(BOARD_WIDTH, BOARD_HEIGHT, src="game_data/init.dat")

    # Main game loop
    while True:
        # Display the game board
        print(gb)

        # Move the shrek
        gb.move_shrek()

        # Get player input and move the player
        move = input("Enter your move (w/a/s/d): ").strip().lower()
        print()
        res = None
        if move == "w":
            res = gb.move_player(0, 1)
        elif move == "a":
            res = gb.move_player(-1, 0)
        elif move == "s":
            res = gb.move_player(0, -1)
        elif move == "d":
            res = gb.move_player(1, 0)
        else:
            print("Invalid input. Please enter w/a/s/d.")

        if res is not None:
            break


################################################################################
#  MAIN EXECUTABLE                                                             #
################################################################################

if __name__ == "__main__":
    success = False
    while not success:
        try:
            game_loop()
            success = True
        except ValueError:
            for _ in range(10):
                print("YOU LOOOSSSSSSEEEEEE\n")
                time.sleep(1)
            print("GAME OVER HAHAHAHAHA START OVER\n")
            time.sleep(2)
    print("SUCCESS. PASSWORD: SWISS")