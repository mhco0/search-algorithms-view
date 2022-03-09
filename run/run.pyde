import random
from Grid import Grid
from Pathfinding import Pathfinding
from GUI import Sidebar, Button
from FoodLabel import FoodLabel

class Phase:
  WAITING = 0
  ALGORITHM_CHOOSE_KEYBOARD = 1
  ALGORITHM_CHOOSE_MOUSE = 2
  ALGORITHM_CHOOSED = 3
  SEARCH = 4
  GO = 5


FRAME_RATE = 30

WIDTH = 800
HEIGHT = 640


def setup():
    global phase, grid, vehicle, food, frame_cnt, interface, sidebar, sidebar_pos, label
    size(WIDTH, HEIGHT)
    grid = Grid(16)
    grid.buildMap(10.0, random.randint(0, 100))
    frameRate(FRAME_RATE)
    frame_cnt = 0
    phase = Phase.WAITING
    vehicle = grid.walkablePosition()
    food = grid.walkablePosition()
    label = FoodLabel(0, 0, "Comidas: ")
    
    btns = [Button(text, 16, color(255, 255, 255), color(64, 64, 64, 225)) for text in ["DFS", "BFS", "DIJKSTRA", "GREEDY",  "A*", "GA"]]
    sidebar = Sidebar(btns, color(56, 28, 255, 150))
    sidebar_pos = ((width - sidebar.width)//2, height - 3*sidebar.height//2)

def draw():
    global phase, grid, vehicle, food, selected_algorithm, pathfindingFunc, pathfindingCtx, optimal_distance, optimal_path, distance, path, frame_cnt, sidebar, sidebar_pos
    
    if phase == Phase.WAITING:
        # print("WAITING")
        path = []
    elif phase == Phase.ALGORITHM_CHOOSED:
        # print("CHOOSED")
        selected_algorithm = sidebar.clicked(sidebar_pos, (mouseX, mouseY)).text
        pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle, food, ctx)
        if selected_algorithm == "DFS":
            pathfindingFunc = lambda ctx: Pathfinding.dfs(grid, vehicle, ctx)
        elif selected_algorithm == "BFS": 
            pathfindingFunc = lambda ctx: Pathfinding.bfs(grid, vehicle, ctx)
        elif selected_algorithm == "DIJKSTRA":
            pathfindingFunc = lambda ctx: Pathfinding.dijkstra(grid, vehicle, ctx)
        elif selected_algorithm == "GREEDY":
            pathfindingFunc = lambda ctx: Pathfinding.greedy(grid, vehicle, food, ctx)
        elif selected_algorithm == "GA":
            assert("Beza vagabundo")
            #pathfindingFunc = lambda ctx: Pathfinding.()
        elif selected_algorithm == "A*":
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
        # print("SEARCHING")
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
            phase = Phase.WAITING
    grid.display()
    grid.displaySeen()
    grid.displayCell(vehicle, color(220,20,60))
    if (phase == Phase.GO or phase == Phase.SEARCH):
        textSize(25);
        text("{} {}/{}".format(selected_algorithm, distance,optimal_distance), 0, 40)
        for p in path:
            grid.displayCell(p, color(138,43,226,90))
    grid.displayCell(food, color(138,43,226))
    label.display()
    if phase != Phase.SEARCH:
        sidebar.display(sidebar_pos)
    
def keyPressed():
    global phase
    
    str_key = str(key)
    
    if str_key.lower() in interface.keys_binded():
        phase = Phase.ALGORITHM_CHOOSE_KEYBOARD
def mouseClicked():
  global phase, sidebar, sidebar_pos
  if phase == Phase.WAITING and sidebar.clicked(sidebar_pos, (mouseX, mouseY)):
    phase = Phase.ALGORITHM_CHOOSED
