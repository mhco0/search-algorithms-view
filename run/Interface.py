
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
        prev_word_width = self.x
        
        for i in range(len(self.options)):
            keyboard_key_text = "(" + self.keyboard_keys[i] + ")"
            text(keyboard_key_text, prev_word_width + ((textWidth(self.options[i]) - textWidth(keyboard_key_text)) // 2), self.y + self.text_size)
            text(self.options[i], prev_word_width, self.y + 2 * self.text_size)
            prev_word_width += textWidth(self.options[i]) + self.text_padding
     
    def binded_option(self, ikey):
        for i in range(len(self.keyboard_keys)):
            if self.keyboard_keys[i] == ikey:
                return self.options[i]
        return ""
    
    def clicked_option(self, pos):
        prev_word_width = self.x
        for i in range(len(self.options)):
            x0 = prev_word_width
            x1 = prev_word_width + textWidth(self.options[i])
            if (pos[0] >= x0 and pos[0] <= x1 and pos[1] >= self.y and pos[1] <= self.y + 2 * self.text_size):
                return self.options[i]
            prev_word_width = x1 + self.text_padding
        return ""
    
    def keys_binded(self):
        return self.keyboard_keys
