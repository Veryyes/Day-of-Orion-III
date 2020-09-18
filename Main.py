import os
import sys
import time
import logging
from enum import Enum

from asciimatics.screen import Screen
import IPython

import MainMenu

GAME_TITLE="Day of Orion III"
LOGFILE="orion3.log"

class State(Enum):
    QUIT = 1
    MAIN_MENU = 2
    HOST = 3
    CONNECT = 4
    GAME = 5


'''
Root Game State/Context
Passed down as a parameter to almost most things to interact with the game itself
Also holds predefined global thingies
'''
class Game:
    FPS = 30.0
    SPF = 1/FPS
    world_size = (5, 5)
    region_size = (2, 2)

    def __init__(self, screen):
        self.tick = 0
        self.running = True
        self.key_state = None
        self.state = State.MAIN_MENU

        self.context = MainMenu.MainMenu(lambda s: 0, 
                                        lambda s: 0, 
                                        lambda s: s.width, 
                                        lambda s: s.height, 
                                        screen)

    def set_context(self, context):
        self.context = context

    def set_state(self, state):
        self.state = state

    def set_state_quit(self):
        self.state = State.QUIT
    
    def set_state_connect(self):
        self.state = State.CONNECT

    def set_state_host(self):
        self.state = State.HOST

    def set_state_game(self):
        self.state = State.GAME

    def is_pressed(self, k, case_sensitive=False):
        if self.key_state == None:
            return False
        if type(k) != int:
            if case_sensitive:
                return self.key_state == ord(k)
            # Nasty way to capitalize letters if not already
            return (self.key_state & ~32) == (ord(k) & ~32)
        else:
            return self.key_state == k


    '''
    Did the user press enter? (13 => \r and 10 => \n)
    '''
    def pressed_enter(self):
        return self.key_state == 13 or self.key_state == 10

    def any_pressed(self):
        return self.key_state

def init(screen):
    game = Game(screen)

    # Set up Logging
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
    
    
    # Implementation of screen.has_resized differs on OS, behavior appears to be different too ....
    def resized_fix(self):
        re_sized = False
        info = self._stdout.GetConsoleScreenBufferInfo()['Window']
        width = info.Right - info.Left + 1
        height = info.Bottom - info.Top + 1
        if width != self._last_width or height != self._last_height:
            re_sized = True
            logging.debug("Resized: {} -> {}, {} -> {}".format(self._last_width, width, self._last_height, height))
        self._last_width = width
        self._last_height = height
        return re_sized

    if sys.platform == "win32":
        screen.has_resized = resized_fix

    return game

def loop(game, screen):
    if game.state == State.QUIT:
        game.running = False

    
    if screen.has_resized(screen):
        screen.clear()

    game.context.update(game, screen)

    screen.refresh()

def app(screen):
    game = init(screen)
    while(game .running):
        # Grab Keyboard state
        game.key_state = screen.get_key()
        start_time = time.clock()

        # Update Every entity
        loop(game, screen)
        game.tick += 1        
        
        # How long did it take to calculate everything we needed to this game loop?
        delta_t = time.clock() - start_time
        if(delta_t < game.SPF):
            # Sleep for the rest of the tick/loop
            time.sleep(abs(delta_t))
        else: # We are taking longer that SPF seconds to calculate a game loop/tick
            logging.debug("Game is lagging by: {} seconds".format(delta_t))
        

if __name__ == "__main__":
    print("> Starting {}".format(GAME_TITLE))
    Screen.wrapper(app)