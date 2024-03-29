from collections import deque
from heapq import heappush, heappop
import random

class Pathfinding:
  @staticmethod
  def dfs (grid, src, dfs_s):
    if dfs_s is None:
      dfs_s = []
      grid.reset()
      dfs_s.append(src)
      grid.see(src)
      return (dfs_s, src)

    last_vis = None

    while len(dfs_s) > 0:
      v = dfs_s.pop()
      last_vis = v
      grid.visit(v)
      pop = True
      adjList = grid.adjacent(v)
      random.shuffle(adjList)
      for u in adjList:
        if not grid.wasSeen(u):
          if pop:
            dfs_s.append(v)
            pop = False
          grid.setParent(u, v)
          grid.see(u)
          dfs_s.append(u)
          break
      if not pop:
        break
    return (dfs_s, last_vis)

  @staticmethod
  def bfs (grid, src, bfs_q):
    if bfs_q is None:
      bfs_q = deque()
      grid.reset()
      bfs_q.append(src)
      grid.see(src)
      return (bfs_q, src)

    sz = len(bfs_q)
    while sz > 0:
      v = bfs_q.popleft()
      grid.visit(v)
      sz -= 1
      for u in grid.adjacent(v):
        if not grid.wasSeen(u):
          grid.see(u)
          grid.setParent(u, v)
          bfs_q.append(u)
    return (bfs_q, src)
  
  @staticmethod
  def nextStep (grid, src, pF, heap_q):
    if heap_q is None:
      heap_q = []
      grid.reset()
      grid.see(src)
      grid.setDistW(src)
      heappush(heap_q, ((pF(src), src)))
      return (heap_q, src)
    lastVis = src
    while len(heap_q) > 0:
      (d, v) = heappop(heap_q)
      if (grid.wasVisited(v)):
          continue
      lastVis = v
      grid.visit(v)
      for u in grid.adjacent(v):
        cur_d = grid.dist[v[0]][v[1]] + grid.world[u[0]][u[1]]
        if cur_d < grid.dist[u[0]][u[1]]:
          grid.see(u)
          grid.setDist(u, cur_d)
          grid.setParent(u, v)
          heappush(heap_q, ((pF(u), u)))
      break
    return (heap_q, lastVis)

  @staticmethod
  def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
  @staticmethod
  def dijkstra (grid, src, heap_q):
    return Pathfinding.nextStep (grid, src, lambda pos : grid.dist[pos[0]][pos[1]], heap_q)
  @staticmethod
  def greedy (grid, src, dest, heap_q):
    return Pathfinding.nextStep (grid, src, lambda pos : Pathfinding.heuristic(dest, pos), heap_q)
  @staticmethod
  def a_star (grid, src, dest, heap_q):
    return Pathfinding.nextStep (grid, src, lambda pos : grid.dist[pos[0]][pos[1]] + Pathfinding.heuristic(dest, pos), heap_q)
