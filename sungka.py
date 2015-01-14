



# Include directives
import sys
import os
import time
import datetime

HAVE_PSYCO = True
try:  # Psyco optim
    import psyco
    psyco.profile(0.2)
except ImportError:
    HAVE_PSYCO = False

HAVE_CMD = True
try:  # CLI
    import cmd
except ImportError:
    HAVE_CMD = False

HAVE_PYGAME = True
try:  # PyGame
    import pygame
    from pygame.locals import *
except ImportError:
    HAVE_PYGAME = False

HAVE_ANDROID = True
try:  # Android
    import android
except ImportError:
    HAVE_ANDROID = False

#if __debug__: from pprint import pprint as pp
#import warnings

from sungka1 import sungka1
import sungka1

# Global variables
LIB_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(LIB_PATH, "images")
#print "Using graphics from", DATA_PATH

FONT_TTF = os.path.join(DATA_PATH, 'freesansbold.ttf')
FONT_SIZE = 16

FRAMES_PER_SECOND = 4
INTRO, HUMAN_TURN, COMPUTER_TURN, END_GAME = range(4)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BEIGE_COLOR = (245, 245, 220) #(201, 202, 167)
BROWN_COLOR = (88, 47, 27)

if HAVE_PSYCO:
    MAX_ALGO_DEPTH = 9  # algo max depth
else:
    MAX_ALGO_DEPTH = 6


#
# Global functions.
#

class Tee(object):
    """A small object which print to each given fileobjects."""
    
    def __init__(self, *fileobjects):
        self.fileobjects = fileobjects
        
    def write(self, string):
        for fileobject in self.fileobjects:
            fileobject.write(string)
            fileobject.flush()  # force display

def display(sungka1_board, title=""):
    """Display current board state / score."""

    if title:
        print "\r", title

    print sungka1_board

def human_sow(sungka1_board, player, cup, elapsed_time=None):
    """Human turn."""

    if cup not in sungka1.HUMAN_CUPS[:len(sungka1_board.board)/2]:
        raise sungka1.InvalidSown, "Invalid Cup"

    idx = list(awale.HUMAN_CUPS).index(cup)  # tuple has no index method!

    title = ""  # human turn
    if player == awale.SOUTH_PLAYER:
        title = "South player sown from '%s'" % cup
    elif player == awale.NORTH_PLAYER:
        title = "North player sown from '%s'" % cup
    if elapsed_time:
        title += " (in %fs)" % elapsed_time

    try:
        awale_board.sow_and_capture(idx)
    finally:
        display(awale_board, title)

    return idx  # cup idx played

def computer_sow(awale_board, player):
    """Computer turn."""

    print "Computer sown ...",
    start_time = time.time()
    idx = awale_board.best_sown(player);
    elapsed_time = time.time() - start_time
    print "\r",

    title = ""  # computer turn
    if player == awale.SOUTH_PLAYER:
        title = "South player sown from '%s' (in %fs)" % (awale.HUMAN_CUPS[idx], elapsed_time)
    elif player == awale.NORTH_PLAYER:
        title = "North player sown from '%s' (in %fs)" % (awale.COMPUTER_CUPS[idx-6], elapsed_time)

    try:
        awale_board.sow_and_capture(idx)
    finally:
        display(awale_board, title)

    return (idx, elapsed_time)  # cup idx (+ computation time) played

def result(awale_board, msg=None):
    """Display score."""

    if msg: print msg
    
    south_score, north_score = awale_board.score  # final score

    # Comptabilize seeds left on board
    south_score += sum( [awale_board.board[idx] for idx in awale.PLAYER_CUPS[awale.SOUTH_PLAYER] ] )
    north_score += sum( [awale_board.board[idx] for idx in awale.PLAYER_CUPS[awale.NORTH_PLAYER] ] )

    title = ""
    if south_score > north_score:
        title = "South player wins with %d seeds vs %d." % (south_score, north_score)
    elif north_score > south_score:
        title = "North player wins with %d seeds vs %d." % (north_score, south_score)
    else:
        title = "Draw (%d seeds each)." % south_score
    
    display(awale_board, title)

def quit(awale_board):
    """Exit awale game."""

    print "Bye."
    sys.exit()  # and exit



#
# External entry point.
#
if __name__ == "__main__":
    main(sys.argv)
