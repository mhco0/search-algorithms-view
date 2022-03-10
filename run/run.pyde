import random
from Grid import Grid
from Pathfinding import Pathfinding
from GUI import Sidebar, Button
from FoodLabel import FoodLabel
from Vehicle import Vehicle

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
GRID_SIZE = 16

def setup():
    global phase, grid, vehicle, food, frame_cnt, sidebar, sidebar_pos, label
    size(WIDTH, HEIGHT)
    frameRate(FRAME_RATE)
    frame_cnt = 0
    
    grid = Grid(GRID_SIZE)
    grid.buildMap(10.0, random.randint(0, 100))
    
    vehicle = Vehicle(grid, grid.walkablePosition())
    food = grid.walkablePosition()
    label = FoodLabel(0, 0, "Comidas: ")
        
    btns = [Button(text, 16, color(255, 255, 255), color(64, 64, 64, 225)) for text in ["DFS", "BFS", "DIJKSTRA", "GREEDY",  "A*", "GA"]]
    sidebar = Sidebar(btns, color(56, 28, 255, 150))
    sidebar_pos = ((width - sidebar.width)//2, height - 3*sidebar.height//2)
    
    phase = Phase.WAITING

def draw():
    global phase, grid, vehicle, food, selected_algorithm, pathfindingFunc, pathfindingCtx, optimal_distance, optimal_path, distance, path, frame_cnt, sidebar, sidebar_pos
    
    if phase == Phase.WAITING:
        # print("WAITING")
        path = []
    elif phase == Phase.ALGORITHM_CHOOSED:
        # print("CHOOSED")
        btn_clicked = sidebar.clicked(sidebar_pos, (mouseX, mouseY))
        if btn_clicked:
            selected_algorithm = btn_clicked.text
        pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle.cell, food, ctx)
        if selected_algorithm == "DFS":
            pathfindingFunc = lambda ctx: Pathfinding.dfs(grid, vehicle.cell, ctx)
        elif selected_algorithm == "BFS": 
            pathfindingFunc = lambda ctx: Pathfinding.bfs(grid, vehicle.cell, ctx)
        elif selected_algorithm == "DIJKSTRA":
            pathfindingFunc = lambda ctx: Pathfinding.dijkstra(grid, vehicle.cell, ctx)
        elif selected_algorithm == "GREEDY":
            pathfindingFunc = lambda ctx: Pathfinding.greedy(grid, vehicle.cell, food, ctx)
        elif selected_algorithm == "GA":
            assert("Beza vagabundo")
            #pathfindingFunc = lambda ctx: Pathfinding.()
        elif selected_algorithm == "A*":
            pathfindingFunc = lambda ctx : Pathfinding.a_star(grid, vehicle.cell, food, ctx)
    
        pathfindingCtx = None
        phase = Phase.SEARCH
        while not grid.wasVisited(food):
            (pathfindingCtx, _) = Pathfinding.dijkstra(grid, vehicle.cell, pathfindingCtx)
        (optimal_distance, optimal_path) = grid.getPath(vehicle.cell, food)
        distance = 0
        pathfindingCtx = None
        grid.reset()
    elif phase == Phase.SEARCH:
        # print("SEARCHING")
        if grid.wasSeen(food):
            pathfindingCtx = None
            (distance, path) = grid.getPath(vehicle.cell, food)
            frame_cnt = frameCount
            phase = Phase.GO
        else:
            (pathfindingCtx, lastVis) = pathfindingFunc(pathfindingCtx)
            (distance, path) = grid.getPath(vehicle.cell, lastVis)
    elif phase == Phase.GO:
        if (frameCount - frame_cnt == 60):
            frame_cnt = frameCount
            grid.reset()
            phase = Phase.WALK
    elif phase == Phase.WALK:
        if frameCount < frame_cnt:
            vehicle.walk()            
        else:
            if (len(path) > 1):
                dir = grid.cellCenter(path[-2]) - grid.cellCenter(path[-1])
                weight = grid.world[path[-2][0]][path[-2][1]] + grid.world[path[-1][0]][path[-1][1]]
                n_frames = 1/(1.0/weight)
                frame_cnt = frameCount + int(n_frames)
                vehicle.velocity = dir /n_frames
            if len(path) == 1:
                label.add_food()
            if len(path):
                vehicle.setCellPosition(path[-1])
                path.pop()
            elif (frameCount - frame_cnt == 60):
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
        text("{} {}/{}".format(selected_algorithm, distance,optimal_distance), 0, 40)
        for p in path:
            grid.displayCell(p, color(138,43,226,90))
    grid.displayCell(food, color(138,43,226))
    vehicle.display()
    label.display()
    if phase != Phase.WALK:
        sidebar.display(sidebar_pos)

def keyPressed():
    global phase
    str_key = str(key)
    if str_key.lower() == 'p' and phase != Phase.WALK:
        phase = Phase.WAITING

def mouseClicked():
  global phase, sidebar, sidebar_pos
  if phase != Phase.WALK and sidebar.clicked(sidebar_pos, (mouseX, mouseY)):
    phase = Phase.ALGORITHM_CHOOSED
