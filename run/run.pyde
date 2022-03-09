import random
from Grid import Grid
from Pathfinding import Pathfinding

ALGORITHM_CHOOSE = 0
SEARCH = 1
SHOW_PATH = 2
GO = 3
WAITING = 4
WALK = 5
RESPAWN_FOOD = 6

FRAME_RATE = 30

def setup():
    global phase, grid, vehicle, food, frame_cnt, food_count
    size(800, 640)
    grid = Grid(16)
    grid.buildMap(10.0, random.randint(0, 100))
    frameRate(FRAME_RATE)
    frame_cnt = 0
    phase = WAITING
    food_count = 0
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()

def draw():
    global phase, grid, vehicle, food, pathfindingFunc, pathfindingCtx, distance, path, frame_cnt, food_count, step, path_len
    if phase == WAITING:
        #print("WAITING")
        grid.display()
        grid.displayCell(vehicle, color(255,0,255))
        grid.displayCell(food, color(255,0,0)) 
    elif phase == ALGORITHM_CHOOSE:
        #print("CHOOSING")
        pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle, food, ctx)
        pathfindingCtx = None
        phase = SEARCH
        grid.display()
        grid.displayCell(vehicle, color(255,0,255))
        grid.displayCell(food, color(255,0,0))
    elif phase == SEARCH:
        #print("SEARCHING")
        if grid.wasSeen(food):
            pathfindingCtx = None
            (distance, path) = grid.getPath(vehicle, food)
            path_len = len(path)
            step = path_len
            phase = GO
        else:
            pathfindingCtx = pathfindingFunc(pathfindingCtx)
        grid.display()
        grid.displayCell(vehicle, color(255,0,255))
        grid.displayCell(food, color(255,0,0))
        frame_cnt = frameCount
    elif phase == GO:
        #print("GO!")
        grid.display()
        grid.displayCell(vehicle, color(255,0,255))
        for p in path:
            grid.displayCell(p, color(255,0,255, 60))
        if (frameCount - frame_cnt == 10):
            phase = WALK
        grid.displayCell(food, color(255,0,0))
    
    elif phase == WALK:
        #print("WALKING")
        if ((frameCount - frame_cnt) % 1 == 0):
            grid.reset()
            grid.display()
            if (step > 0):
                vehicle = path[step-1]
                step -= 1
                for idx, p in enumerate(path):
                    if(idx < step):
                        grid.displayCell(p, color(255,0,255, 40))
                if(vehicle == food):
                    food_count += 1
                    frame_cnt = frameCount
                    phase = RESPAWN_FOOD
            grid.displayCell(food, color(255,0,0))
            grid.displayCell(vehicle, color(255,0,255))

    elif phase == RESPAWN_FOOD:
        print("Food count: ", food_count)
        if (frameCount - frame_cnt == 30):
            food = grid.walkablePosition()
            phase = ALGORITHM_CHOOSE
            grid.display()
            
def keyPressed():
    global phase
    if key.lower() == 'p':
        phase = ALGORITHM_CHOOSE
