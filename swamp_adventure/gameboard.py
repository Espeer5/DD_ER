################################################################################
#                                                                              #
#  gameboard.py                                                                #
#                                                                              #
#  This module contains the class definition for the GameBoard class. The      #
#  GameBoard is a collection of GameSpace objects arranged in a regular grid,  #
#  representing the full game world. The GameBoard class includes methods for  #
#  initializing the board, moving the player and the Shrek around on it, and   #
#  displaying it in any given configuration.                                   #
#                                                                              #
#  Author: Edward Speer                                                        #
#  Revised: 04/14/2025                                                         #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import random

from gamespace import GameSpace, CellType
from minigames import *

################################################################################
#  CONSTANTS                                                                   #
################################################################################

# Map of cell positions to their executables
MINIGAMES = {
    (2, 0): pub,
    (3, 2): lily_pads,
    (2, 4): troll,
    (0, 3): cheese_nearby,
    (1, 2): cheese,
    (4, 3): base_three,
    (7, 1): deadend,
    (9, 2): wizard,
}

################################################################################
#  CLASS DEFINITIONS                                                           #
################################################################################

"""
GameBoard class

Represents the game board for the Swamp Adventure game. The board is a grid of
GameSpace objects, each representing a cell in the game world. The GameBoard
class includes methods for initializing the board, moving the player and Shrek
around on it, and displaying the board in any given configuration.
"""
class GameBoard:
    def __init__(self, width: int, height: int, src=None):
        self.width = width
        self.height = height
        self.has_cheese = False
        self.has_whistle = False
        self.board = [[GameSpace(CellType.EMPTY, x, y) for y in
                        range(height)] for x in range(width)]
        if src is not None:
            # Read in the types of cells from the source file
            with open(src, "r") as f:
                for x, line in enumerate(f.readlines()):
                    for y, char in enumerate(line.strip()):
                        if char == "E":
                            self.board[x][y] = GameSpace(CellType.EMPTY, x, y)
                        elif char == "W":
                            self.board[x][y] = GameSpace(CellType.WALL, x, y)
                        elif char == "A":
                            self.board[x][y] = GameSpace(CellType.ACTION, x, y)
                        else:
                            raise ValueError(f"Unknown cell type: {char}")
        for x, y in MINIGAMES:
            self.board[x][y].action = MINIGAMES[(x, y)]
        self.player_pos = (0, 0)
        self.shrek_pos = (round(width / 2), height - 1)
        self.board[self.player_pos[0]][self.player_pos[1]].visited = True

    def move_player(self, dx: int, dy: int):
        old_pos = self.player_pos
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if self.board[new_x][new_y].cell_type == CellType.WALL:
                self.board[new_x][new_y].visited = True
                print("You can't go that way! The foliage is too thick...")
            else:
                self.player_pos = (new_x, new_y)
                if (self.board[new_x][new_y].cell_type == CellType.ACTION and
                   not self.board[new_x][new_y].visited):
                    result = self.board[new_x][new_y].action()
                    self.board[new_x][new_y].visited = True
                    match result:
                        case ReturnCode.DEATH:
                            print("You died! Game over.")
                            raise ValueError("Death")
                        case ReturnCode.BACK:
                            self.board[new_x][new_y].visited = False
                            self.player_pos = old_pos
                        case ReturnCode.SPELL:
                            self.player_pos = (0, 0)
                        case ReturnCode.CHEESE:
                            self.has_cheese = True
                        case ReturnCode.SHREK_WHISTLE:
                            self.has_whistle = True
                else:
                    self.board[new_x][new_y].visited = True
            if self.player_pos == self.shrek_pos:
                res = shrek_encounter(self.has_whistle)
                if res == ReturnCode.DEATH:
                    print("You died! Game over.")
                    raise ValueError("Death")
                elif res == ReturnCode.SPELL:
                    self.player_pos = (0, 0)
            if self.player_pos == (9, 0):
                if self.has_cheese:
                    print("You have made it to the exit with the cheese! You have escaped the swamp. Congratulations.")
                    return True
                else:
                    print("You have made it to the exit without the cheese! You have not escaped the swamp. Go back and find your cheese.")

        else:
            print("Are you stupid? Do you know how to read a map?\n")

    def move_shrek_step(self, dx: int, dy: int):
        new_x = self.shrek_pos[0] + dx
        new_y = self.shrek_pos[1] + dy
        if (0 <= new_x < self.width and 0 <= new_y < self.height and
                           self.board[new_x][new_y].cell_type != CellType.WALL):
            self.shrek_pos = (new_x, new_y)

    def move_shrek(self):
        # Generate a movement of the shrek which is either a step towards the
        # player in the x or y direction, or a random step, with probability
        # 60/40 for each.
        if random.random() < 0.6:
            if (abs(self.shrek_pos[0] - self.player_pos[0]) >
                                   abs(self.shrek_pos[1] - self.player_pos[1])):
                if self.shrek_pos[0] < self.player_pos[0]:
                    self.move_shrek_step(1, 0)
                else:
                    self.move_shrek_step(-1, 0)
            else:
                if self.shrek_pos[1] < self.player_pos[1]:
                    self.move_shrek_step(0, 1)
                else:
                    self.move_shrek_step(0, -1)
        else:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            self.move_shrek_step(dx, dy)

    def __str__(self):
        board_str = ""
        for y in range(self.height - 1, -1, -1):
            board_str += "=" * (self.width * 6 + 1) + "\n"
            board_str += "|     " * self.width + "|\n"
            for x in range(self.width):
                board_str += "|"
                if (x, y) == self.player_pos:
                    board_str += "  ■  "
                elif (x, y) == self.shrek_pos:
                    board_str += "  S  "
                elif self.board[x][y].visited:
                    if self.board[x][y].cell_type == CellType.WALL:
                        board_str += "  X  "
                    elif self.board[x][y].cell_type == CellType.ACTION:
                        board_str += "  ✓  "
                    elif self.board[x][y].cell_type == CellType.EMPTY:
                        board_str += "     "
                else:
                    board_str += "  ?  "
            board_str += "|\n"
            board_str += "|     " * self.width + "|\n"
        board_str += "=" * (self.width * 6 + 1) + "\n"
        return board_str
