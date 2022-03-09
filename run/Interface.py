
class Interface:
    
    def __init__(self, x, y, iwidth, iheight, options, keyboard_keys):
        assert(len(options) == len(keyboard_keys))
        self.x = x
        self.y = y
        self.width = iwidth
        self.height = iheight
        
        self.options = options
        self.keyboard_keys = keyboard_keys
        
        self.radius = 5
        self.color = color(64, 64, 64)
        self.text_size = 16
        self.text_padding = 8
        self.text_color = color(255, 255, 255)
        
    def display(self):
        fill(self.color)
        noStroke()
        rect(self.x, self.y, self.width, self.height, self.radius)
        textSize(self.text_size)
        
        fill(self.text_color)
        prev_word_width = 0
        
        for i in range(len(self.options)):
            text("(" + self.keyboard_keys[i] + ")", self.x + prev_word_width + textWidth(self.options[i]) / 2 - textWidth("(" + self.keyboard_keys[i] + ")") / 2, self.y + self.text_size)
            text(self.options[i], self.x + prev_word_width, self.y + 2 * self.text_size)
            prev_word_width += textWidth(self.options[i]) + self.text_padding
     
    def binded_option(self, ikey):
        for i in range(len(self.keyboard_keys)):
            if self.keyboard_keys[i] == ikey:
                return self.options[i]
        return ""
    
    def keys_binded(self):
        return self.keyboard_keys
