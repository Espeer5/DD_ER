################################################################################
#                                                                              #
#  gamespace.py                                                                #
#                                                                              #
#  This module contains the class definition for the GameSpace class, which    #
#  represents each grid cell in the swamp adventure game world. The class      #
#  includes the type of cell, its coordinated, and potentially a function      #
#  that can be executed when the player enters the cell.                       #
#                                                                              #
#  Author: Edward Speer                                                        #
#  Revised: 04/07/2025                                                         #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

from enum import Enum

################################################################################
#  CLASS DEFINITIONS                                                           #
################################################################################

"""
CellType Enum

Represents the type of cell in the game space.
"""
class CellType(Enum):
    EMPTY  = 0
    WALL   = 1
    ACTION = 2


"""
GameSpace class

Represents a cell in the game space. Each cell has a type, coordinates, and
potentially a function that can be executed when the player enters the cell.
Each space also contains a flag which dictates whether the player has previously
visited the space.
"""
class GameSpace:
    def __init__(self, cell_type: CellType, x: int, y: int, action=None):
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.action = action
        self.visited = False
