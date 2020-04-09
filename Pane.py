from enum import Enum

class Style(Enum):
    BOLD = 1
    NORMAL = 2
    REVERSE = 3
    UNDERLINE = 4

class Colour(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    
'''
Enumerate Relative Positions
'''
class Pos(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    TOP = 1
    BOTTOM = 3

    # Specifies the index in textAlign
    X=0
    Y=1

'''
This is a box/menu that will be actually rendered
'''
class Pane:
    def __init__(self, x,y,w,h, text=""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center_text = False
        self.text = []
        self.textAlign = (Pos.CENTER, Pos.CENTER)
        self.overflowText = False
        self.hmargin = .6
        self.children = []
        self.parent = None
        self.isSelected = False
        self.defaultColor = Colour.WHITE.value
        self.selectedColor = Colour.GREEN.value
        self.alwaysRedraw = False

        '''
        Flag used to mark if the Pane needs to be updated in the next draw
        if self.alwaysRedraw is False then this needs to be set to update the
        Pane in its next call to update
        '''
        self.updateStatic = True

        '''
        Splits text by newlines and when the text is about to spill over the margin
        '''
        line_max_w = int(self.w * (1 - self.hmargin))
        for line in text.splitlines():
            for i in range(0, len(line), line_max_w):
                self.text.append(text[i:i+line_max_w])

    def setTextAlignLeft(self):
        self.textAlign = (Pos.LEFT, self.textAlign[Pos.Y.value])
        self.updateStatic = True

    def setTextAlignRight(self):
        self.textAlign = (Pos.RIGHT, self.textAlign[Pos.Y.value])
        self.updateStatic = True

    def setTextAlignCenter(self):
        self.textAlign = (Pos.CENTER, Pos.CENTER)
        self.updateStatic = True
        
    def setTextAlignTop(self):
        self.textAlign = (self.textAlign[Pos.X.value], Pos.TOP)
        self.updateStatic = True

    def setTextAlignBottom(self):
        self.textAlign = (self.textAlign[Pos.X.value], Pos.BOTTOM)
        self.updateStatic = True

    def setText(self, text):
        self.text = []
        self.appendText(text)
        
    def appendText(self, text):
        self.updateStatic = True
        line_max_w = int(self.w * (1 - self.hmargin))

        if self.overflowText:
            for line in text.splitlines():
                self.text.append(line)
        else:       
            for line in text.splitlines():
                for i in range(0, len(line), line_max_w):
                    self.text.append(text[i:i+line_max_w])

    def draw_boarder(self,screen):
        color = self.defaultColor
        if(self.isSelected):
            color = self.selectedColor
        screen.move(self.x, self.y)
        screen.draw(self.x+self.w, self.y, char="-", colour=color)
        screen.draw(self.x+self.w, self.y+self.h, char="|", colour=color)
        screen.draw(self.x, self.y+self.h, char='-', colour=color)
        screen.draw(self.x, self.y, char="|", colour=color)

        # Stole outline style from Radare2 ;)
        screen.print_at(".", self.x,self.y, colour=color)
        screen.print_at(".",self.x+self.w,self.y, colour=color)
        screen.print_at("\'", self.x+self.w,self.y+self.h, colour=color)
        screen.print_at("`",self.x,self.y+self.h, colour=color)

    def draw_text(self, screen):
        if self.textAlign[Pos.Y.value] == Pos.TOP:
            y = self.y+1
        elif self.textAlign[Pos.Y.value] == Pos.CENTER:
            y = int((self.y+self.h/2.0))
        elif self.textAlign[Pos.Y.value] == Pos.BOTTOM:
            y = (self.y + self.h) - len(self.text)
            
        if self.textAlign[Pos.X.value] == Pos.LEFT:
            for text in self.text:
                x = self.x+1
                screen.print_at(text, x, y)
                y += 1
        elif self.textAlign[Pos.X.value] == Pos.CENTER:
            for text in self.text:
                x = int((self.x+self.w/2.0) - len(text)/2.0)
                screen.print_at(text, x, y)
                y += 1
        elif self.textAlign[Pos.X.value] == Pos.RIGHT:
            for text in self.text:
                x = (self.x+self.w) - len(text)
                screen.print_at(text, x, y)
                y += 1

    def update(self, screen):
        if self.updateStatic or self.alwaysRedraw:
            self.updateStatic = False
            self.draw_boarder(screen)
            self.draw_text(screen)
        for child in self.children:
            child.update(screen)