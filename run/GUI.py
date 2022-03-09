
class Button:
    def __init__(self, str, text_size, text_color, fill_color, padding = 10, radius = 5):
        self.text = str
        self.text_size = text_size
        self.text_color = text_color
        self.fill_color = fill_color
        self.padding = padding
        self.radius = radius
        
        textSize(self.text_size)
        self.width = textWidth(self.text) + 2*padding
        self.height = self.text_size + 2*padding
    
    def display(self, pos):
        fill(self.fill_color)
        rect(pos[0], pos[1], self.width, self.height, self.radius)
        textSize(self.text_size)
        fill(self.text_color)
        text(self.text, pos[0] + self.padding, pos[1] + self.text_size + self.padding)
    
    def clicked(self, pos, mousePos):
        if (mousePos[0] >= pos[0] and  mousePos[0] <= pos[0] + self.width):
            if (mousePos[1] >= pos[1] and  mousePos[1] <= pos[1] + self.height):
                return True
        return False

class Sidebar:
    def __init__(self, btns, fill_color, padding = 10, radius = 5):
        assert(len(btns))
        self.buttons = btns
        self.fill_color = fill_color
        self.padding = padding
        self.radius = radius
        
        self.width = sum([btn.width for btn in btns]) + (len(btns) + 1) * padding
        self.height = btns[0].height + 2*padding
    
    def display(self, pos):
        fill(self.fill_color)
        rect(pos[0], pos[1], self.width, self.height, self.radius)
        xb = pos[0] + self.padding
        yb = pos[1] + self.padding
        for btn in self.buttons:
            btn.display((xb, yb))
            xb += btn.width + self.padding
    
    def clicked(self, pos, mousePos):
        xb = pos[0] + self.padding
        yb = pos[1] + self.padding
        for btn in self.buttons:
            if(btn.clicked((xb, yb), mousePos)):
                return btn
            xb += btn.width + self.padding
        return None
