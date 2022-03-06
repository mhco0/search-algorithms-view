import random
from Grid import Grid
from Pathfinding import Pathfinding

ALGORITHM_CHOOSE = 0
SEARCH = 1
SHOW_PATH = 2
GO = 3
WAITING = 4

FRAME_RATE = 30

def setup():
    global phase, grid, vehicle, food, frame_cnt
    size(800, 640)
    grid = Grid(16)
    grid.buildMap(10.0, random.randint(0, 100))
    frameRate(FRAME_RATE)
    frame_cnt = 0
    phase = WAITING
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()

def draw():
    global phase, grid, vehicle, food, pathfindingFunc, pathfindingCtx, distance, path, frame_cnt
    if phase == WAITING:
        print("WAITING")
        path = []
    elif phase == ALGORITHM_CHOOSE:
        print("CHOOSING")
        pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle, food, ctx)
        pathfindingCtx = None
        phase = SEARCH
    elif phase == SEARCH:
        print("SEARCHING")
        if grid.wasVisited(food):
            pathfindingCtx = None
            (distance, path) = grid.getPath(vehicle, food)
            frame_cnt = frameCount
            phase = GO
        else:
            (pathfindingCtx, lastVis) = pathfindingFunc(pathfindingCtx)
            (distance, path) = grid.getPath(vehicle, lastVis)
    elif phase == GO:
        print("GO!")
        print(distance)
        if (frameCount - frame_cnt == 60):
            phase = WAITING
    
    grid.display()
    grid.displaySeen()
    grid.displayCell(vehicle, color(220,20,60))
    if (phase == GO or phase == SEARCH):
        for p in path:
            grid.displayCell(p, color(138,43,226,90))
    grid.displayCell(food, color(138,43,226))
def keyPressed():
    global phase
    if key.lower() == 'p':
        phase = ALGORITHM_CHOOSE
