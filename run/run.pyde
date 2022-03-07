import random
from Grid import Grid
from Pathfinding import Pathfinding

ALGORITHM_CHOOSE = 0
SEARCH = 1
SHOW_PATH = 2
GO = 3
WAITING = 4
WALK = 5

FRAME_RATE = 30

def setup():
    global phase, grid, vehicle, food, frame_cnt, foodcount
    size(800, 640)
    grid = Grid(16)
    grid.buildMap(10.0, random.randint(0, 100))
    frameRate(FRAME_RATE)
    frame_cnt = 0
    phase = WAITING
    foodcount = 0
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()

def draw():
    global phase, grid, vehicle, food, pathfindingFunc, pathfindingCtx, distance, path, frame_cnt, foodcount
    if phase == WAITING:
        print("WAITING")
    elif phase == ALGORITHM_CHOOSE:
        print("CHOOSING")
        pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle, food, ctx)
        pathfindingCtx = None
        phase = SEARCH
    elif phase == SEARCH:
        print("SEARCHING")
        if grid.wasSeen(food):
            pathfindingCtx = None
            (distance, path) = grid.getPath(vehicle, food)
            #frame_cnt = frameCount
            phase = GO
        else:
            pathfindingCtx = pathfindingFunc(pathfindingCtx)
    elif phase == GO:
        print("GO!")
        print(distance)
        frame_cnt = frameCount
    
    elif phase == WALK:
        frame_cnt = frameCount
        for p in path:
            vehicle = p
            grid.reset()
            grid.display()
            grid.displayCell(vehicle, color(255,0,255))
            grid.displayCell(food, color(255,0,0))
        if(vehicle == food):
            foodcount += 1
            frame_cnt = frameCount
            if (frameCount - frame_cnt >= 60):
                food = grid.walkablePosition()
                phase = ALGORITHM_CHOOSE
    
    grid.display()
    grid.displayCell(vehicle, color(255,0,255))
    if (phase == GO):
        for p in path:
            grid.displayCell(p, color(255,0,255, 60))
        if (frameCount - frame_cnt >= 120):
            phase = WALK
    grid.displayCell(food, color(255,0,0))
def keyPressed():
    global phase
    if key.lower() == 'p':
        phase = ALGORITHM_CHOOSE
