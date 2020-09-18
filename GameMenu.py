from enum import Enum
from Main import State, Game
from Pane import Pane, Colour

class View(Enum):
    WORLD = 1
    REGION = 2

class Team(Enum):
    RED = 1
    BLUE = 2

'''
View Space and the Battlefield through this Pane
'''
class GameUI(Pane):
    def __init__(self, x,y,w,h, screen, text=""):
        super().__init__(x,y,w,h, screen)
        self.hmargin = 0.0
        self.team = Team.RED
        self.defaultColor = Colour.RED.value
        self.world = []
        self.view = View.WORLD

        region_w = self.w // Game.world_size[0]
        region_h = self.h // Game.world_size[1]
        for i in range(Game.world_size[0]):
            row = []
            for j in range(Game.world_size[1]):
                row.append(Region(
                    x = self.x + (j * region_w) , 
                    y = self.y + (i * region_h), 
                    w = region_w, 
                    h = region_h, 
                    id = i*Game.world_size[0]+j))

            self.world.append(row)

    def update(self, game, screen):
        super().update(screen)

        # In world view you see all the regions
        if self.view == View.WORLD:
            for i in range(Game.world_size[0]):
                for j in range(Game.world_size[1]):
                    self.world[i][j].update(game, screen)
        elif self.view == View.REGION:
            pass

class Region(Pane):
    def __init__(self, x,y,w,h, id, text=""):
        super().__init__(x,y,w,h)
        self.id = id
        self.hmargin = 0.0
        self.defaultColor = Colour.RED.value

    def update(self, game, screen):
        if self.updateStatic or self.alwaysRedraw:
            self.updateStatic = False
            self.draw_boarder(screen)
            if(self.isSelected):
                screen.print_at(str(self.id), self.x+1, self.y+1, colour=Colour.BLACK.value, bg=Colour.YELLOW.value)
            else:
                screen.print_at(str(self.id), self.x+1, self.y+1, colour=Colour.YELLOW.value)