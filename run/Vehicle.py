class Vehicle:
    def __init__(self, grid, cell, velocity = PVector(0, -1)):
        self.cell = cell
        self.position = grid.cellCenter(cell)
        self.grid = grid
        self.r = 5
        self.velocity = velocity
        self.color = color(220,20,60)
    
    def walk(self):
        self.position += self.velocity
    
    def setCellPosition(self, cell):
        self.cell = cell
        self.position = self.grid.cellCenter(cell)
    
    def display(self):
        theta = self.velocity.heading() + PI / 2
        fill(self.color)
        noStroke()
        with pushMatrix():
            translate(self.position.x, self.position.y)
            rotate(theta)
            beginShape()
            vertex(0, -self.r * 2)
            vertex(-self.r, self.r * 2)
            vertex(self.r, self.r * 2)
            endShape(CLOSE)
