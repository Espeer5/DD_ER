################################################################################
#                                                                              #
#  game_loop.py                                                                #
#                                                                              #
#  This module contains the main game loop for the Swamp Adventure text-based  #
#  adventure game.                                                             #
#                                                                              #
#  Author:  Edward Speer                                                       #
#  Revised: 04/02/2025                                                         #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import block_print as bp

################################################################################
#  CONSTANTS                                                                   #
################################################################################

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
