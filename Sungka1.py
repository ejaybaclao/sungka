



# Include directives
import sys
import time

if __debug__:
    from pprint import pprint as pp
    import md5

# Global variables
BOARD_SIZE = 12  # default nb cups, "houses"
INITIAL_SEEDS = 4  # initial seeds by cups
ALL_SEEDS = BOARD_SIZE * INITIAL_SEEDS

SOUTH_PLAYER = 0  # player
NORTH_PLAYER = 1  # computer
SOUTH_CUPS = range(BOARD_SIZE / 2)
NORTH_CUPS = range(BOARD_SIZE / 2, BOARD_SIZE)
PLAYER_CUPS = (SOUTH_CUPS, NORTH_CUPS)

HUMAN_CUPS = ('A', 'B', 'C', 'D', 'E', 'F', 'G')  # south
COMPUTER_CUPS = ('a', 'b', 'c', 'd', 'e', 'f', 'g')  # north

ALGO_TYPES = ('bfs', 'minimax', 'maxi', 'negamax', 'alphabeta')
ALGO_DEPTH=3  # depth of the tree


#
# Awale Exceptions.
#
class AwaleError(Exception):
    """Base class for Awale exceptions."""

    pass

class InvalidSown(AwaleError):
    """Invalid input."""

    pass

class NoMoreMove(AwaleError):
    """No move available."""

    pass

class EndOfGame(AwaleError):
    """End of game?"""

    pass


#
# Awale board.
#
class Awale(object):
    """Awale board class.
	
    Usage:
    >>> awale = Awale()
    >>> awale
    {'board': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 'score': [0, 0]}
    >>> awale.sow_and_capture(3)
    >>> awale.sow_and_capture(6)
    >>> awale.sow_and_capture(2)
    >>> awale.sow_and_capture(6)
    >>> print awale
                 f    e    d    c    b    a
    North ( 0) [ 5] [ 5] [ 5] [ 5] [ 7] [ 0]
               [ 4] [ 4] [ 0] [ 1] [ 6] [ 6] ( 0) South
                 A    B    C    D    E    F
    >>> awale.sow_and_capture(1)
    >>> awale.best_sown(1)
    10
    >>> awale.sow_and_capture(10)
    >>> print awale
                 f    e    d    c    b    a
    North ( 5) [ 6] [ 0] [ 5] [ 5] [ 7] [ 0]
               [ 5] [ 1] [ 0] [ 0] [ 7] [ 7] ( 0) South
                 A    B    C    D    E    F
    """

    def __init__(self, board=[INITIAL_SEEDS]*BOARD_SIZE, score=[0, 0], algo=ALGO_TYPES[1], depth=ALGO_DEPTH):
        """Initialize the board game and player scores.

        By default BOARD_SIZE cups with INITIAL_SEEDS inside each houses;
        South (human) and north (computer) players begin with a score of 0.
        """
        
	# Awale board
	self.board = board
        self.score = score
        self.turn = 0  # store nb turns
        
	# Params/settings
	self.algo_type = algo
	self.algo_depth = depth

    def __repr__(self):
        """Friendly representation of Awale data: board + score."""

        #return str(self.__dict__)
        return "{'board': %s, 'score': %s}" % (str(self.board), str(self.score))
        
  

       
if __name__ == "__main__":
    _test()
