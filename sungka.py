

# Specific variables for pydoc
from __init__ import VERSION
__author__ = "Visnu Ejay Baclao"
__date__ = "batch 2015"
__version__ = VERSION
__credits__ = """Sungka tayo."""

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
# Main CLI.
#
if HAVE_CMD:
    
    class AwaleCLI(cmd.Cmd):
        """Command Line Interface for Awale game."""

        def __init__(self, options=None):
            cmd.Cmd.__init__(self)
            self.intro= """
  pyAwale is a free software available under the terms of the GNU GPL.
  Refer to the file COPYING (which should be included in this distribution)
  for the specific terms of this licence.
  You can freely download pyAwale and enjoy to play with it.
  """
            self.prompt = "pyAwale> "

            self.awale = Awale(algo=options.algo, depth=int(options.level)*3)

        #
        # Private functions.
        #

        def _display(self):
            """Display current board state / score."""
            
            display(self.awale)

        def _human_sow(self, player, cup):
            """Human turn."""

            human_sow(self.awale, player, cup)
        
        def _computer_sow(self, player):
            """Computer turn."""

            computer_sow(self.awale, player)

        def _quit(self):
            """Display score and exit."""
        
            result(self.awale)
            quit(self.awale)

        #
        # Params/settings.
        #

        def do_info(self, line=None):
            """Display engine settings/parameters."""

            if HAVE_PSYCO: 
                print "'psyco' optimizer activated"

            print "'%s'" % self.awale.algo_type,
            print "algorithm used",
            print "(level", self.awale.algo_depth/3, ")"

        def do_algo(self, algo):
            """Display/toogle to another algorithm."""

            if algo:
                if algo in awale.ALGO_TYPES:
                    self.awale.algo_type = algo
                else:
                    print "unknown '%s' algo?" % algo, awale.ALGO_TYPES
                print "algo setted to", self.awale.algo_type

        def do_level(self, level):
            """Display/set default level of the algorithm."""

            if level:
                self.awale.algo_depth = int(level)*3
            print "level setted to", self.awale.algo_depth/3

        #
        # Actions.
        #

        def do_display(self, line=None):
            """Show board state and score."""

            self._display()

        def do_sow(self, cup):
            """Sow and capture from given cup; Then, compute adversary move."""

            try:
                # First, human turn
                if cup:
                    self._human_sow(awale.SOUTH_PLAYER, cup)  # south
                else:  # computer help
                    self._computer_sow(awale.SOUTH_PLAYER)
                    
                # Then, computer turn
                self._computer_sow(awale.NORTH_PLAYER)
        
            except awale.InvalidSown, msg:  # invalid input
                #warnings.warn(str(msg), stacklevel=1)
                print >> sys.stderr, msg
            except awale.NoMoreMove, msg:  # no move available
                if __debug__: print >> sys.stderr, msg
                self._quit()
            except awale.EndOfGame, msg:  # eog
                if __debug__: print >> sys.stderr, msg
                self._quit()
        
        def do_EOF(self, line=None):
            """Quit."""
        
            self._quit()


#
# PyGame GUI.
#
if HAVE_PYGAME:
    
    # Last seeds/score image available
    MAX_SEEDS_IMAGE = 15
    MAX_SCORE_IMAGE = 25

    #
    # Cup sprite.
    #
    class CupSprite(pygame.sprite.Sprite):
        """Cup sprite."""

        # South cups positions
        pos_00 = (90, 320)
        pos_01 = (178, 286)
        pos_02 = (268, 251)
        pos_03 = (360, 214)
        pos_04 = (448, 177)
        pos_05 = (538, 140)
        # North cups positions
        pos_06 = (490, 70)
        pos_07 = (405, 105)
        pos_08 = (325, 135)
        pos_09 = (242, 170)
        pos_10 = (160, 204)
        pos_11 = (84, 238)

        # Seeds src images
        cup_00 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_0.png"))
        cup_01 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_1d.png"))
        cup_02 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_2c.png"))
        cup_03 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_3b.png"))
        cup_04 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_4D.png"))
        cup_05 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_5d.png"))
        cup_06 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_6c.png"))
        cup_07 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_7b.png"))
        cup_08 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_8e.png"))
        cup_09 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_9d.png"))
        cup_10 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_10d.png"))
        cup_11 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_11d.png"))
        cup_12 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_12d.png"))
        cup_13 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_12d_13.png"))
        cup_14 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_14d.png"))
        cup_15 = pygame.image.load(os.path.join(DATA_PATH, "awale_seed_15d.png"))

        def __init__(self, cup, nb_seeds=4):
            """Initialize cup seeds and set positioning."""

            pygame.sprite.Sprite.__init__(self)

            # Get cup index
            self.cup_idx = None
            if cup in awale.HUMAN_CUPS:
                self.cup_idx = list(awale.HUMAN_CUPS).index(cup)
            elif cup in awale.COMPUTER_CUPS:
                self.cup_idx = list(awale.COMPUTER_CUPS).index(cup) + awale.BOARD_SIZE / 2

            # Initial image
            self.nb_seeds = nb_seeds

            if self.nb_seeds <= MAX_SEEDS_IMAGE:
                self.image = eval("CupSprite.cup_%02d" % self.nb_seeds)
            else:
                self.image = eval("CupSprite.cup_%02d" % MAX_SEEDS_IMAGE)

            # Set the position
            self.rect = self.image.get_rect()
            self.rect.center = eval("CupSprite.pos_%02d" % self.cup_idx)  # center

            # Default font size/style
            self.font = pygame.font.Font(FONT_TTF, FONT_SIZE)  # ANDROID
            self.font.set_italic(True)

        def update(self, board, count_seeds=False):
            """Update image according to nb_seeds."""
            
            self.nb_seeds = board[self.cup_idx]

            # Update image (use a copy to avoid original Surface modification)
            if self.nb_seeds <= MAX_SEEDS_IMAGE:
                self.image = eval("CupSprite.cup_%02d.copy()" % self.nb_seeds)
            else:
                self.image = eval("CupSprite.cup_%02d.copy()" % MAX_SEEDS_IMAGE)

            # Add display of nb seeds for help
            if count_seeds:
                text = self.font.render("%d" % self.nb_seeds, 1, BROWN_COLOR, BEIGE_COLOR)
                textpos = text.get_rect(topleft=(10, 10))
                self.image.blit(text, textpos)
            elif self.nb_seeds >= 8:  # display nb seeds
                text = self.font.render("%d" % self.nb_seeds, 1, BROWN_COLOR, BEIGE_COLOR)
                textpos = text.get_rect(topleft=(30, 30))
                self.image.blit(text, textpos)

    #
    # House sprite.
    #
    class HouseSprite(pygame.sprite.Sprite):
        """House sprite."""

        def __init__(self, player, nb_seeds=0):
            """Initialize house seeds for given player."""
            
            pygame.sprite.Sprite.__init__(self)

            # Initial image
            self.nb_seeds = nb_seeds
            self.player = player

            # South/north src images
            house = "house"  # camp?
            if self.player == awale.SOUTH_PLAYER:
                house = "south"
            elif self.player == awale.NORTH_PLAYER:
                house = "north"

            self.houses = [ pygame.image.load(os.path.join(DATA_PATH, "awale_%s_0.png" % house)) ]
            for idx in range(1, MAX_SCORE_IMAGE+1):
                self.houses.append(pygame.image.load(os.path.join(DATA_PATH, "awale_%s_%d.png" % (house, idx))))

            if self.nb_seeds <= MAX_SCORE_IMAGE:
                self.image = self.houses[self.nb_seeds]
            else:
                self.image = self.houses[MAX_SCORE_IMAGE]

            # Set the position
            self.rect = self.image.get_rect()
            if self.player == awale.SOUTH_PLAYER:
                self.rect.bottomright = (608, 462)
            elif self.player == awale.NORTH_PLAYER:
                self.rect.topleft = (55, 5)

        def update(self, nb_seeds):
            """Update image according to nb_seeds."""
            
            self.nb_seeds = nb_seeds

            # Update image
            if self.nb_seeds <= MAX_SCORE_IMAGE:
                self.image = self.houses[self.nb_seeds]
            else:
                self.image = self.houses[MAX_SCORE_IMAGE]

    #
    # Main PyGame.
    #
    def awale_game(options=None):
        """Main PyGame interface for Awale game."""

        pygame.init()  # initialize pygame modules

        # Awale window
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("pyAwale-%s - The count-and-capture official board game of Africa." % __version__)

        # Map the back button to the escape key.
        if HAVE_ANDROID:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        
        # Awale images
        awale_closed_image = os.path.join(DATA_PATH, "awale_board_closed.png")
        awale_closed_background = pygame.image.load(awale_closed_image).convert_alpha()

        awale_board_image = os.path.join(DATA_PATH, "awale_board_empty.png")
        awale_board_background = pygame.image.load(awale_board_image).convert_alpha()

        font = pygame.font.Font(FONT_TTF, FONT_SIZE)  # default font size # ANDROID

        # Cups image
        cups = (
            # South cups
            CupSprite('A'),
            CupSprite('B'),
            CupSprite('C'),
            CupSprite('D'),
            CupSprite('E'),
            CupSprite('F'),
            # North cups
            CupSprite('a'),
            CupSprite('b'),
            CupSprite('c'),
            CupSprite('d'),
            CupSprite('e'),
            CupSprite('f')
        )
        cups_group = pygame.sprite.RenderPlain(*cups)

        # Houses image
        houses = (
            # South
            HouseSprite(awale.SOUTH_PLAYER),
            # North
            HouseSprite(awale.NORTH_PLAYER)
        )
        houses_group = pygame.sprite.RenderPlain(*houses)

        # Awale object
        awale_board = Awale(algo=options.algo, depth=int(options.level)*3)

        # Display intro/copirights helper
        def _display_intro():
            """Helper subfunction to display intro/copirights."""
        
            text = font.render("pyAwale is a free software available under the terms of the GNU GPL.", 1, BROWN_COLOR)
            textpos = text.get_rect(topleft=(0, 0))
            screen.blit(text, textpos)

            text = font.render("Refer to the file COPYING (which should be included in this distribution)", 1, BROWN_COLOR)
            textpos = text.get_rect(topleft=(0, 20))
            screen.blit(text, textpos)
            
            text = font.render("for the specific terms of this licence.", 1, BROWN_COLOR)
            textpos = text.get_rect(topleft=(0, 40))
            screen.blit(text, textpos)

            text = font.render("You can freely download pyAwale and enjoy to play with it.", 1, BROWN_COLOR)
            textpos = text.get_rect(topleft=(0, 60))
            screen.blit(text, textpos)

        # Display doc helper
        def _display_help(state):
            """Helper subfunction to display help."""
            
            if state == INTRO:
                text = font.render("- Choose your algo/level with the 'a' and 'l' keys.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 360))
                screen.blit(text, textpos)
            elif state == HUMAN_TURN or state == COMPUTER_TURN:
                text = font.render("- Change your algo/level with the 'a' and 'l' keys.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 360))
                screen.blit(text, textpos)

            if state == INTRO:
                text = font.render("- Begin the game by clicking on the awale board.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 380))
                screen.blit(text, textpos)
            elif state == HUMAN_TURN or state == COMPUTER_TURN:
                text = font.render("- Sow seeds by clicking on the awale cup.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 380))
                screen.blit(text, textpos)
            elif state == END_GAME:
                #text = font.render("- Replay by pressing 'RETURN' key.", 1, BROWN_COLOR)
                text = font.render("- Replay by clicking on the awale board.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 380))
                screen.blit(text, textpos)

            if state == INTRO or state == HUMAN_TURN or state == COMPUTER_TURN:
                text = font.render("- Use 'ESC' key to exit current panel.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 400))
                screen.blit(text, textpos)
            elif state == END_GAME:
                text = font.render("- Use 'ESC' key to quit the game.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(260, 400))
                screen.blit(text, textpos)

        # Display settings/params helper
        def _display_settings(state):
            """Helper subfunction to display settings/params."""

            if state == INTRO:
                text = font.render("optim='psyco'", 1, BROWN_COLOR)
                textpos = text.get_rect(bottomright=(640, 440))
                screen.blit(text, textpos)

            text = font.render("algo='%s'" % awale_board.algo_type, 1, BROWN_COLOR)
            textpos = text.get_rect(bottomright=(640, 460))
            screen.blit(text, textpos)

            text = font.render("level=%d" % (awale_board.algo_depth/3), 1, BROWN_COLOR)
            textpos = text.get_rect(bottomright=(640, 480))
            screen.blit(text, textpos)

        # Display score/turns helper
        def _display_scores(state):
            """Helper subfunction to display scores/turns."""

            if state == END_GAME:
                south_score, north_score = awale_board.score  # final score
                # Comptabilize seeds left on board
                south_score += sum( [awale_board.board[idx] for idx in awale.PLAYER_CUPS[awale.SOUTH_PLAYER] ] )
                north_score += sum( [awale_board.board[idx] for idx in awale.PLAYER_CUPS[awale.NORTH_PLAYER] ] )

                if south_score > north_score:
                    text = font.render("South player wins (%d seeds vs %d)." % (south_score, north_score), 1, BROWN_COLOR)
                elif north_score > south_score:
                    text = font.render("North player wins (%d seeds vs %d)." % (north_score, south_score), 1, BROWN_COLOR)
                else:
                    text = font.render("Draw (%d seeds each)." % south_score, 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(0, 0))
                screen.blit(text, textpos)

                #text = font.render("Replay by hitting 'RETURN' or 'ESC' to quit.", 1, BROWN_COLOR)
                text = font.render("Replay by clicking or 'ESC' to quit.", 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(0, 20))
                screen.blit(text, textpos)

            if state == HUMAN_TURN or state == COMPUTER_TURN or state == END_GAME:
                text = font.render("North score: %d" % awale_board.score[awale.NORTH_PLAYER], 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(0, 40))
                screen.blit(text, textpos)
            
                text = font.render("South score: %d" % awale_board.score[awale.SOUTH_PLAYER], 1, BROWN_COLOR)
                textpos = text.get_rect(topleft=(0, 60))
                screen.blit(text, textpos)
            
            # Display turns
            text = font.render("Turn: %d" % awale_board.turn, 1, BROWN_COLOR)
            textpos = text.get_rect(topleft=(0, 80))
            screen.blit(text, textpos)

        # Display credits helper
        def _display_credits():
            """Helper subfunction to display credits."""

            text = font.render(__credits__, 1, BROWN_COLOR)
            textpos = text.get_rect(bottomright=(640, 480))
            screen.blit(text, textpos)

        idx_human = idx_computer = None  # init
        start_time = elapsed_time = computation_time = None
        
        # Game loop
	state = INTRO
        disp_help = False
        computer_begins = None  # True or False? None= not yet decided
        clock = pygame.time.Clock()
        while True:
            clock.tick(FRAMES_PER_SECOND)  # limit fps

            if HAVE_ANDROID:  # Android may ask that your game pause itself
                if android.check_pause():
                    android.wait_for_resume()
        
            if state == INTRO:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)  # default pointer
                
                # Display copyrights ...
		for event in pygame.event.get():
                    if event.type == QUIT or \
                           ( event.type == KEYDOWN and event.key == K_ESCAPE ):
                        result(awale_board, "Esc!")
                        state = END_GAME  # end
		    elif event.type == MOUSEBUTTONDOWN or \
			   ( event.type == KEYDOWN and event.key == K_RETURN ):
                        display(awale_board,
                                title="Initial board (algo='%s', level=%d)" % (awale_board.algo_type,
                                                                               awale_board.algo_depth/3))
                        start_time = time.time()  # start chrono
			state = HUMAN_TURN  # next= human begin
                    else:
                        if event.type == KEYDOWN:
			    if event.key == K_h or event.key == K_QUESTION:  # display help?
				if not disp_help: 
				    disp_help = True
				else: 
				    disp_help = False
                            elif event.key == K_a:  # update ai
				curr_algo_idx = list(awale.ALGO_TYPES).index(awale_board.algo_type)
				if curr_algo_idx == len(awale.ALGO_TYPES) - 1:
				    awale_board.algo_type = awale.ALGO_TYPES[0]
				else:
				    awale_board.algo_type = awale.ALGO_TYPES[curr_algo_idx + 1]
                                print "Algo setted to", awale_board.algo_type
                            elif event.key == K_l:  # update level
                                if awale_board.algo_depth == MAX_ALGO_DEPTH:
                                    awale_board.algo_depth = 3
                                else:
                                    awale_board.algo_depth = awale_board.algo_depth + 3
                                print "Level setted to", awale_board.algo_depth/3

                # Re-init Awale internal status
                idx_human = idx_computer = None  # reinit 
                awale_board.board = [awale.INITIAL_SEEDS]*awale.BOARD_SIZE
                awale_board.score = [0, 0]  # reset board, but keep algo/level
                awale_board.turn = 0
                computer_begins = None  # reset which begins
                                    
                # Rendering board
                screen.blit(awale_closed_background, (0, 0))

                # Intro
                _display_intro()

                # Settings/params
                _display_settings(state)

                # Doc ('h', '?')
		if disp_help: _display_help(state)

	    elif state == HUMAN_TURN or state == COMPUTER_TURN:
                # Game turns

                if state == HUMAN_TURN:
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)  # default pointer

                    # User inputs
                    for event in pygame.event.get():
                        if event.type == QUIT or \
                               ( event.type == KEYDOWN and event.key == K_ESCAPE ):
                            result(awale_board, "Esc!")
                            state = END_GAME  # end
                        else:
                            if event.type == KEYDOWN:
                                if event.key == K_h or event.key == K_QUESTION:  # display help?
                                    if not disp_help: 
                                        disp_help = True
                                    else: 
                                        disp_help = False
                                elif event.key == K_a:  # update ai
                                    curr_algo_idx = list(awale.ALGO_TYPES).index(awale_board.algo_type)
                                    if curr_algo_idx == len(awale.ALGO_TYPES) - 1:
                                        awale_board.algo_type = awale.ALGO_TYPES[0]
                                    else:
                                        awale_board.algo_type = awale.ALGO_TYPES[curr_algo_idx + 1]
                                    print "Algo setted to", awale_board.algo_type
                                elif event.key == K_l:  # update level
                                    if awale_board.algo_depth == MAX_ALGO_DEPTH:
                                        awale_board.algo_depth = 3
                                    else:
                                        awale_board.algo_depth = awale_board.algo_depth + 3
                                    print "Level setted to", awale_board.algo_depth/3
                                elif event.key == K_c and computer_begins == None:
                                    computer_begins = True  # computer begin
                                    state = COMPUTER_TURN
                                    continue

                            if event.type == MOUSEBUTTONDOWN:
                                elapsed_time = time.time() - start_time  # compute elapsed time
                                cup = None
                                if cups[list(awale.HUMAN_CUPS).index('A')].rect.collidepoint(event.pos): cup = 'A'
                                elif cups[list(awale.HUMAN_CUPS).index('B')].rect.collidepoint(event.pos): cup = 'B'
                                elif cups[list(awale.HUMAN_CUPS).index('C')].rect.collidepoint(event.pos): cup = 'C'
                                elif cups[list(awale.HUMAN_CUPS).index('D')].rect.collidepoint(event.pos): cup = 'D'
                                elif cups[list(awale.HUMAN_CUPS).index('E')].rect.collidepoint(event.pos): cup = 'E'
                                elif cups[list(awale.HUMAN_CUPS).index('F')].rect.collidepoint(event.pos): cup = 'F'
			
                                if cup:
                                    try:
                                        idx_computer = None
                                        idx_human = human_sow(awale_board, awale.SOUTH_PLAYER, cup, elapsed_time)

                                    except awale.InvalidSown, msg:  # invalid input
                                        if __debug__: print >> sys.stderr, msg
                                        pass
                                    except awale.EndOfGame, msg:  # eog
                                        result(awale_board, msg)
                                        state = END_GAME  # end
				    else:
                                        computer_begins = False  # player has begun
					state = COMPUTER_TURN  # next= computer turn
                            
                elif state == COMPUTER_TURN:
                    pygame.mouse.set_cursor(*pygame.cursors.ball)  # wait cursor
                    pygame.time.wait(1000)
                
                    try:
                        idx_computer, computation_time = computer_sow(awale_board, awale.NORTH_PLAYER)

                    except awale.NoMoreMove, msg:  # no move available
                        result(awale_board, msg)
                        state = END_GAME  # end
		    except awale.EndOfGame, msg:  # eog
                        result(awale_board, msg)
                        state = END_GAME  # end
		    else:
                        start_time = time.time()  # start chrono for human player
			state = HUMAN_TURN  # next= human turn

                    pygame.event.clear()  # clean all pending events

                # Update all cups according to Awale board
                cups_group.update(awale_board.board, disp_help)

                # Update houses
                for player in [awale.SOUTH_PLAYER, awale.NORTH_PLAYER]:
                    houses[player].update(awale_board.score[player])

                # Rendering board
                screen.blit(awale_board_background, (0, 0))
                cups_group.draw(screen)
                houses_group.draw(screen)
    
                # First move, which begin: player or computer?
                if computer_begins == None:
                    text = font.render("Click on one of your houses to begin;", 1, BROWN_COLOR)
                    textpos = text.get_rect(topleft=(0, 0))
                    screen.blit(text, textpos)
                    text = font.render("Or, hit 'c' for computer begins.", 1, BROWN_COLOR)
                    textpos = text.get_rect(topleft=(0, 20))
                    screen.blit(text, textpos)
                # Display moves
                if idx_human in awale.SOUTH_CUPS:
                    text = font.render("Your move: '%s' (in %fs)" % (awale.HUMAN_CUPS[idx_human],
                                                                     elapsed_time), 1, BROWN_COLOR)
                    textpos = text.get_rect(topleft=(0, 0))
                    screen.blit(text, textpos)
                if idx_computer in awale.NORTH_CUPS:
                    text = font.render("My move: '%s' (in %fs)" % (awale.COMPUTER_CUPS[idx_computer-6],
                                                                   computation_time), 1, BROWN_COLOR)
                    textpos = text.get_rect(topleft=(0, 20))
                    screen.blit(text, textpos)

                # Display north/south scores + current turn
                _display_scores(state)

                # Params
                _display_settings(state)

                # Doc ('h', '?')
		if disp_help: _display_help(state)

	    elif state == END_GAME:
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)  # end cursor

                # All of Fame ...
		for event in pygame.event.get():
                    if event.type == QUIT or \
                           ( event.type == KEYDOWN and event.key == K_ESCAPE ):
                        quit(awale_board)
                        
		    elif event.type == MOUSEBUTTONDOWN or \
                             ( event.type == KEYDOWN and \
                               ( event.key == K_RETURN or event.key == K_c ) ):
			state = INTRO  # next= replay
                    else:
                        if event.type == KEYDOWN:
                            if event.key == K_h or event.key == K_QUESTION:  # display help?
                                if not disp_help: 
                                    disp_help = True
                                else: 
                                    disp_help = False

                # Update all cups (for last turn) according to Awale board
                cups_group.update(awale_board.board, disp_help)

                # Update houses
                for player in [awale.SOUTH_PLAYER, awale.NORTH_PLAYER]:
                    houses[player].update(awale_board.score[player])

                # Rendering board
                screen.blit(awale_board_background, (0, 0))
                cups_group.draw(screen)
                houses_group.draw(screen)
        
                # Display north/south scores + current turn
                _display_scores(state)

                # Credits
                _display_credits()

                # Doc ('h', '?')
		if disp_help: _display_help(state)

            # Rendering screen
            pygame.display.flip()

#
# Main entry point.
#
def main(sysargs):
    """The count-and-capture official board game of Africa."""

    # Get options
    from optparse import OptionParser, make_option

    option_list = [
	make_option("-a", "--algo",
        	    action="store", dest="algo", 
               	    type="choice", choices=awale.ALGO_TYPES,
                    default='minimax',
                    help="choose ALGO=bfs, minimax, maxi, negamax or alphabeta (default ALGO=%default)"),
        make_option("-l", "--level",
                    action="store", dest="level", 
                    default=1,
                    help="difficulty LEVEL=1, 2 or 3 of game (default LEVEL=%default)"),
        make_option("-o", "--log",
                    action="store_true", dest="log",
                    default=False,
                    help="output results in log file (default LOG=%default)"),
        ]

    if HAVE_PYGAME:
        option_list.append(make_option("-c", "--cli",
                                       action="store_true", dest="cli", 
                                       default=False,
                                       help="use command-line interface"))

    parser = OptionParser(usage="python -O %prog [options] ... [args] ...", 
                          version=__version__,
                          description="A simple Awale game.",
                          option_list=option_list)

    (options, args) = parser.parse_args(sysargs)

    # Compulsory options
    if not hasattr(options, 'cli'):
        setattr(options, 'cli', True)  # CLI by default

    #
    # Process start here.
    #
    if options.log:  # redirect stdout to log file
        log_name = "pyawale-%s.log" % (datetime.datetime.today().isoformat())
        log_file = open(log_name, 'w')

        stdout = sys.stdout  # save stdout
        sys.stdout = Tee(sys.stdout, log_file)  # print to stdout and to a log file

    if options.cli:  # CLI
        awale_cli = AwaleCLI(options)
        try:
            awale_cli.cmdloop()  # enter game loop
        except KeyboardInterrupt:  # C^c
            print >> sys.stderr, "Bye."

    else:  # PyGame
	try:
	    awale_game(options)
        except KeyboardInterrupt:  # C^c
            print >> sys.stderr, "Bye."


    if options.log:  # restore stdout
        log_file.close()
        sys.stdout = stdout

#
# External entry point.
#
if __name__ == "__main__":
    main(sys.argv)
