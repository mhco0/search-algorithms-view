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
    grid.buildMap(7.0, 2)
    frameRate(FRAME_RATE)
    phase = WAITING
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()

def draw():
    global phase, grid, vehicle, food, pathfindingFunc, pathfindingCtx, distance, path
    if phase == WAITING:
        print("WAITING")
    elif phase == ALGORITHM_CHOOSE:
        print("CHOOSING")
        pathfindingFunc = lambda ctx : Pathfinding.dijkstra(grid, vehicle, ctx)
        pathfindingCtx = None
        phase = SEARCH
    elif phase == SEARCH:
        print("SEARCHING")
        if grid.wasSeen(food):
            pathfindingCtx = None
            (distance, path) = grid.getPath(vehicle, food)
            phase = GO
        else:
            pathfindingCtx = pathfindingFunc(pathfindingCtx)
    elif phase == GO:
        print("GO!")
        print(distance)
        phase = WAITING
    
    grid.display()
    grid.displayCell(vehicle, color(255,0,255))
    grid.displayCell(food, color(255,0,0))
def keyPressed():
    global phase
    if key.lower() == 'p':
        phase = ALGORITHM_CHOOSE
