
class FoodLabel:
    
    def __init__(self, x, y, prefix):
        self.count = 0
        self.x = x 
        self.y = y
        self.prefix = prefix
        
        self.text_size = 16
        self.text_color = color(255, 255, 255)
    
    def display(self):
        fill(self.text_color)
        textSize(self.text_size)
        text(self.prefix + str(self.count), self.x, self.y + self.text_size)
        
    def add_food(self):
        self.count += 1
