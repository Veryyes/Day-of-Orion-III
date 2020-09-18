from Pane import Pane
from Main import State
from GameMenu import GameUI

class ConnectMenu(Pane):
	def __init__(self, x, y, w, h, screen):
		super().__init__(x,y,w,h, screen)
		self.connect = Pane(int(x+w*.2), int(y+h*.1), int(w*.6), int(h*.3), text="Connect")
		self.host = Pane(int(x+w*.2), int(y+h*.6), int(w*.6), int(h*.3), text="Host")
		self.connect.isSelected=True
		self.children.append(self.connect)
		self.children.append(self.host)

	def update(self, game, screen):
		super().update(screen)

		if self.connect.isSelected:
			if game.is_pressed(screen.KEY_DOWN):
				self.connect.updateStatic = True
				self.connect.isSelected = False
				self.host.updateStatic = True
				self.host.isSelected=True
			elif game.pressed_enter():
				screen.clear()
				game.set_state_game()
				game.set_context(GameUI(
					lambda screen: 0,
					lambda screen: 0,
					lambda screen: int(screen.width*7/8),
					lambda screen: int(screen.height*6/8),
					screen
				))
				#run connection

		elif self.host.isSelected:
			if game.is_pressed(screen.KEY_UP):
				self.connect.updateStatic = True
				self.connect.isSelected=True
				self.host.updateStatic = True
				self.host.isSelected=False
			elif game.pressed_enter():
				screen.clear()
				game.set_state_quit()
				#run host