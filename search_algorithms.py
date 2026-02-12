from collections import deque
import heapq

# Uninformed Search: BFS
def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = {start}
    nodes_expanded = 0
    
    while queue:
        (x, y), path = queue.popleft()
        nodes_expanded += 1
        
        if (x, y) == goal:
            return path, nodes_expanded
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    
    return None, nodes_expanded

# Uninformed Search: DFS
def dfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]
    visited = {start}
    nodes_expanded = 0
    
    while stack:
        (x, y), path = stack.pop()
        nodes_expanded += 1
        
        if (x, y) == goal:
            return path, nodes_expanded
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))
    
    return None, nodes_expanded

# Informed Search: A* with Manhattan distance
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = [(0, start, [start], 0)]
    visited = {start}
    nodes_expanded = 0
    
    while open_set:
        f, (x, y), path, g = heapq.heappop(open_set)
        nodes_expanded += 1
        
        if (x, y) == goal:
            return path, nodes_expanded
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                new_g = g + 1
                new_h = manhattan_distance((nx, ny), goal)
                new_f = new_g + new_h
                heapq.heappush(open_set, (new_f, (nx, ny), path + [(nx, ny)], new_g))
    
    return None, nodes_expanded
