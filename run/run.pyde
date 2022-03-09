import random
from Grid import Grid
from Pathfinding import Pathfinding
from Interface import Interface
from FoodLabel import FoodLabel

class Phase:
  WAITING = 0
  ALGORITHM_CHOOSE_KEYBOARD = 1
  ALGORITHM_CHOOSE_MOUSE = 2
  ALGORITHM_CHOOSED = 3
  SEARCH = 4
  GO = 5
  WALK = 6
  RESPAWN_FOOD = 7
  


FRAME_RATE = 30

WIDTH = 800
HEIGHT = 640

INTERFACE_WIDTH = 280
INTERFACE_HEIGHT = 40


def setup():
    global phase, grid, vehicle, food, frame_cnt, interface, label
    size(WIDTH, HEIGHT)
    grid = Grid(16)
    grid.buildMap(10.0, random.randint(0, 100))
    frameRate(FRAME_RATE)
    frame_cnt = 0
    phase = Phase.WAITING
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()
    label = FoodLabel(0, 0, "Comidas: ")
    interface = Interface((width - INTERFACE_WIDTH) // 2 , height - 3*INTERFACE_HEIGHT//2, INTERFACE_WIDTH, INTERFACE_HEIGHT, ["DFS", "BFS", "DIJKSTRA", "GREEDY",  "A*", "GA"], ["1", "2", "3", "4", "5", "6"])

def draw():
    global phase, grid, vehicle, food, pathfindingFunc, pathfindingCtx, optimal_distance, optimal_path, distance, path, frame_cnt, selected_option
    
    if phase == Phase.WAITING:
        print("WAITING")
        path = []
    elif phase == Phase.ALGORITHM_CHOOSE_MOUSE:
        selected_option = interface.clicked_option((mouseX, mouseY))
        if selected_option:
            phase = Phase.ALGORITHM_CHOOSED
        else:
            phase = Phase.WAITING
    elif phase == Phase.ALGORITHM_CHOOSE_KEYBOARD:
        str_key = str(key)
        selected_option = interface.binded_option(str_key)
        if selected_option:
            phase = Phase.ALGORITHM_CHOOSED
        else:
            phase = Phase.WAITING
    elif phase == Phase.ALGORITHM_CHOOSED:
        print("CHOOSED")
        
        pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle, food, ctx)
        if selected_option == "DFS":
            pathfindingFunc = lambda ctx: Pathfinding.dfs(grid, vehicle, ctx)
        elif selected_option == "BFS": 
            pathfindingFunc = lambda ctx: Pathfinding.bfs(grid, vehicle, ctx)
        elif selected_option == "DIJKSTRA":
            pathfindingFunc = lambda ctx: Pathfinding.dijkstra(grid, vehicle, ctx)
        elif selected_option == "GREEDY":
            pathfindingFunc = lambda ctx: Pathfinding.greedy(grid, vehicle, food, ctx)
        elif selected_option == "GA":
            assert("Beza vagabundo")
            #pathfindingFunc = lambda ctx: Pathfinding.()
        elif selected_option == "A*":
            pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle, food, ctx)
    
        pathfindingCtx = None
        phase = Phase.SEARCH
        while not grid.wasVisited(food):
            (pathfindingCtx, _) = Pathfinding.dijkstra(grid, vehicle, pathfindingCtx)
        (optimal_distance, optimal_path) = grid.getPath(vehicle, food)
        distance = 0
        pathfindingCtx = None
        grid.reset()
    elif phase == Phase.SEARCH:
        print("SEARCHING")
        if grid.wasVisited(food):
            pathfindingCtx = None
            (distance, path) = grid.getPath(vehicle, food)
            frame_cnt = frameCount
            phase = Phase.GO
        else:
            (pathfindingCtx, lastVis) = pathfindingFunc(pathfindingCtx)
            (distance, path) = grid.getPath(vehicle, lastVis)
    elif phase == Phase.GO:
        print("GO!")
        if (frameCount - frame_cnt == 60):
            grid.reset()
            phase = Phase.WALK
    elif phase == Phase.WALK:
        if frameCount % 3 == 0:
            if len(path) == 1:
                label.add_food()
                frame_cnt = frameCount
            if len(path):
                vehicle = path[-1]
                path.pop()
            if (frameCount - frame_cnt == 60):
                frame_cnt = frameCount
                grid.reset()
                phase = Phase.RESPAWN_FOOD
    elif phase == Phase.RESPAWN_FOOD:
        if (frameCount - frame_cnt == 60):
            food = grid.walkablePosition()
            phase = Phase.ALGORITHM_CHOOSED
                
    grid.display()
    grid.displaySeen()
    if (phase == Phase.GO or phase == Phase.SEARCH):
        textSize(25);
        text("{} {}/{}".format(selected_option, distance,optimal_distance), 0, 40)
        for p in path:
            grid.displayCell(p, color(138,43,226,90))
    grid.displayCell(food, color(138,43,226))
    grid.displayCell(vehicle, color(220,20,60))
    label.display()
    if phase != Phase.SEARCH:
        interface.display()
    
def keyPressed():
    global phase
    
    str_key = str(key)
    
    if str_key.lower() in interface.keys_binded():
        phase = Phase.ALGORITHM_CHOOSE_KEYBOARD
def mouseClicked():
  global phase
  if phase == Phase.WAITING:
    phase = Phase.ALGORITHM_CHOOSE_MOUSE
