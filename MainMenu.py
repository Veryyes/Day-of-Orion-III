from random import randint
from enum import Enum

from asciimatics.screen import Screen
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene

from Pane import Pane
from Main import State

class MainMenu(Pane):
	def __init__(self, x, y, w, h, screen):
		super().__init__(x, y, w, h)
		self.title = FigletText("Day of Orion III", font='big')
		self.stars = [(randint(1, screen.width-1), randint(1, screen.height-1), randint(0,3)) for _ in range(70)]
		self.star_animation = ['.','x','*','+']
		self.color_maps = []

		self.__reroll_color_maps(screen)

	def __reroll_color_maps(self, screen):
		self.color_maps = []
		color = randint(0, screen.colours-1)
		for i in range(self.title.max_height):
			self.color_maps.append([(color, None, None)] *len(self.title.rendered_text[0][i]))
		

	def update(self, game, screen):
        # Draw random stars on screen and reroll colors
		for i in range(len(self.stars)):
			screen.print_at(self.star_animation[int(self.stars[i][2]+game.tick/20.0)%4], self.stars[i][0], self.stars[i][1])
	
		if(game.tick%180 == 0):
			self.__reroll_color_maps(screen)

        # Set the Title Position and Color and draw it
		x = int(screen.width/2.0 - self.title.max_width/2.0)
		y = int(screen.height/2.0 - self.title.max_height/2.0)
		for i in range(self.title.max_height):
			screen.paint(self.title.rendered_text[0][i], x, y+i, colour_map=self.color_maps[i])

		screen.print_at("Press any Key to continue", int(screen.width/2.0 - 12.5), int(screen.height*.8))
		
		if game.any_pressed():
			game.set_state_quit()

		super().update(screen)