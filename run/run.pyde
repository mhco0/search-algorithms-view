import random
from Grid import Grid
from Pathfinding import Pathfinding
from Interface import Interface
from FoodLabel import FoodLabel

ALGORITHM_CHOOSE = 0
SEARCH = 1
SHOW_PATH = 2
GO = 3
WAITING = 4

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
    phase = WAITING
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()
    label = FoodLabel(0, 0, "Comidas: ")
    interface = Interface(width // 2 - INTERFACE_WIDTH // 2 , height - INTERFACE_HEIGHT, INTERFACE_WIDTH, INTERFACE_HEIGHT, ["DFS", "BFS", "DIJKSTRA", "GREEDY",  "A*", "GA"], ["1", "2", "3", "4", "5", "6"])

def draw():
    global phase, grid, vehicle, food, pathfindingFunc, pathfindingCtx, optimal_distance, optimal_path, distance, path, frame_cnt
    
    if phase == WAITING:
        print("WAITING")
        path = []
    elif phase == ALGORITHM_CHOOSE:
        print("CHOOSING")
        str_key = str(key)
        
        selected_option = interface.binded_option(str_key)
        
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
        phase = SEARCH
        while not grid.wasVisited(food):
            (pathfindingCtx, _) = Pathfinding.dijkstra(grid, vehicle, pathfindingCtx)
        (optimal_distance, optimal_path) = grid.getPath(vehicle, food)
        distance = 0
        pathfindingCtx = None
        grid.reset()
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
        if (frameCount - frame_cnt == 60):
            phase = WAITING
    
    grid.display()
    grid.displaySeen()
    grid.displayCell(vehicle, color(220,20,60))
    if (phase == GO or phase == SEARCH):
        textSize(25);
        text("Distance {}/{}".format(distance,optimal_distance), 25, 25)
        for p in path:
            grid.displayCell(p, color(138,43,226,90))
    grid.displayCell(food, color(138,43,226))
    label.display()
    interface.display()
    
def keyPressed():
    global phase
    
    str_key = str(key)
    
    if str_key.lower() in interface.keys_binded():
        phase = ALGORITHM_CHOOSE
