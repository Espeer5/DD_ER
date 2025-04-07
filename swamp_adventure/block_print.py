################################################################################
#                                                                              #
#  block_print.py                                                              #
#                                                                              #
#  This file contains helper functions for printing specific large blocks of   #
#  text that are used in the game, including ascii art drawn from external     #
#  files.                                                                      #
#                                                                              #
#  Author:  Edward Speer                                                       #
#  Revised: 04/02/2025                                                         #
#                                                                              #
################################################################################

################################################################################
#  CONSTANTS                                                                   #
################################################################################

# Paths to the ascii art files
ASCII_PATH      = "./ascii/"
ASCII_extension = "_ascii.txt"

# Paths to pre-written messages
TEXT_PATH       = "./msgs/"
TEXT_extension  = ".txt"

################################################################################
#  FUNCTIONS                                                                   #
################################################################################

"""
print_ascii_art(art_name)

Prints the ascii art from the file containing art by the given name. Ascii file
paths are constructed as ASCII_PATH + art_name + ASCII_extension.
"""
def print_ascii_art(art_name):
    with open(ASCII_PATH + art_name + ASCII_extension, "r") as f:
        print(f.read())


"""
print_msg(msg_name)

Prints the pre-written message from the file containing the message by the given
name. Message file paths are constructed as TEXT_PATH + msg_name +
TEXT_extension.
"""
def print_msg(msg_name):
    with open(TEXT_PATH + msg_name + TEXT_extension, "r") as f:
        print(f.read())
