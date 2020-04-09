import os
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


'''
Root Game State/Context
Passed down as a parameter to almost most things to interact with the game itself
Also holds predefined global thingies
'''
class Game:
    FPS = 30.0
    SPF = 1/FPS

    def __init__(self, screen):
        self.tick = 0
        self.running = True
        self.key_state = None
        self.state = State.MAIN_MENU

        self.context = MainMenu.MainMenu(0, 0, screen.width, screen.height, screen)
        
    def set_state(self, state):
        self.state = state

    def set_state_quit(self):
        self.state = State.QUIT

    def is_pressed(self, k, case_sensitive=False):
        if case_sensitive:
            return self.key_state == ord(k)
        # Nasty way to capitalize letters if not already
        return (self.key_state & ~32) == (ord(k) & ~32) 

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
    
    return game

def loop(game, screen):
    if game.state == State.QUIT:
        game.running = False
        
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