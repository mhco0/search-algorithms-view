import random
sand = color(230, 230, 179)
water = color(140, 191, 217)  
swamp = color(167, 152, 118)  
wall = color(90, 90, 90)  
inf = int(1e9+7)

SAND = 1
SWAMP = 5
WATER = 10
WALL = inf

class Grid:
  def __init__(self, cellSize):
    self.cellSize = cellSize
    self.shape = (width//cellSize, height//cellSize)
    self.world = [[0 for x in range(self.shape[1])] for y in range(self.shape[0])] 
    self.seen = [[False for x in range(self.shape[1])] for y in range(self.shape[0])]
    self.visited = [[False for x in range(self.shape[1])] for y in range(self.shape[0])]
    self.dist = [[0 for x in range(self.shape[1])] for y in range(self.shape[0])]
    self.parent = [[None for x in range(self.shape[1])] for y in range(self.shape[0])]
  
  def buildMap (self, noiseScale, seed):
    noiseSeed(seed)
    noiseDetail(8)
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        xoff = float(i) / self.shape[0]
        yoff = float(j) / self.shape[1]
        result = noise(xoff * noiseScale, yoff * noiseScale)
        if (result <= 0.3):
          self.world[i][j] = WATER
        elif (result <= 0.4):
          self.world[i][j] = WALL
        elif (result <= 0.55):
          self.world[i][j] = SAND
        elif (result <= 0.65):
          self.world[i][j] = SWAMP
        else :
          self.world[i][j] = WATER
  
  def reset(self):
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        self.seen[i][j] = False
        self.visited[i][j] = False
        self.dist[i][j] = inf
  def see(self, p):
    self.seen[p[0]][p[1]] = True
  def visit(self, p):
    self.visited[p[0]][p[1]] = True
  def wasSeen(self, p):
    return self.seen[p[0]][p[1]]
  def wasVisited(self, p):
    return self.visited[p[0]][p[1]]

  def setDistW(self, p):
    self.dist[p[0]][p[1]] = self.world[p[0]][p[1]]
  def setDist(self, p, w):
    self.dist[p[0]][p[1]] = w

  def setParent(self, p, par):
    self.parent[p[0]][p[1]] = par
    
  def getPath(self, src, dst):
    path = []
    dist = grid.world[src[0]][src[1]]
    while dst != src:
      path.append(dst)
      dist += grid.world[dst[0]][dst[1]]
      dst = grid.parent[dst[0]][dst[1]]
    path.append(src)
    return (dist, path)

  delta = [(1, 0), (0, 1), (0, -1), (-1, 0)]
  
  def is_within_map_bounds(self, p):
    return p[0] >= 0 and p[1] >= 0 and p[0] < self.shape[0] and p[1] < self.shape[1]
  
  def is_walkable(self, p):
    return self.world[p[0]][p[1]] != WALL
  def walkablePosition(self):
    pos = (0, 0)
    while True:
      pos = (random.randint(0, self.shape[0]-1), random.randint(0, self.shape[1]-1))
      if (self.is_walkable(pos) and self.world[pos[1]][pos[1]] != WATER):
        return pos
  
  def adjacent(self, p):
    neighbors = []
    for (dx, dy) in self.delta:
      np = (p[0] + dx, p[1] + dy)
      if (self.is_within_map_bounds(np) and self.is_walkable(np)):
        neighbors.append(np)
    return neighbors

  def getPath(self, src, dst):
    path = []
    dist = self.world[src[0]][src[1]]
    while dst != src:
      path.append(dst)
      dist += self.world[dst[0]][dst[1]]
      dst = self.parent[dst[0]][dst[1]]
    path.append(src)
    return (dist, path)
  
  def cellCenter(self, pos):
    return PVector((pos[0] + 0.5)*self.cellSize,  (pos[1] + 0.5)*self.cellSize)

  def displayCell(self, p, cellColor):
    noStroke()
    fill(cellColor)
    rect(p[0] * self.cellSize, p[1] * self.cellSize, self.cellSize, self.cellSize)
  def highlightCell(self, p, borderColor):
    stroke(borderColor)
    strokeWeight(2);
    noFill()
    rect(p[0] * self.cellSize, p[1] * self.cellSize, self.cellSize, self.cellSize)
  
  def displaySeen(self):
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        p = (i, j)
        if (self.wasVisited(p)):
          self.displayCell(p, color(220,20,60, 50))
        elif self.wasSeen (p):
          self.displayCell(p, color(220,20,60,99))
          self.highlightCell(p, color(220,20,60))
  
  def display(self):
    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        p = (i, j)
        if (self.world[i][j] == SAND):
          self.displayCell(p, sand)
        elif (self.world[i][j] == SWAMP):
          self.displayCell(p, swamp)
        elif (self.world[i][j] == WATER):
          self.displayCell(p, water)
        else:
          self.displayCell(p, wall)
