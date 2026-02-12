import pygame
import sys
from search_algorithms import bfs, dfs, astar
from adversarial_ai import get_ghost_move, get_pacman_move


pygame.init()

CELL_SIZE = 40
MAZE_ROWS = 15
MAZE_COLS = 20
WIDTH = MAZE_COLS * CELL_SIZE
HEIGHT = MAZE_ROWS * CELL_SIZE + 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Maze
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class PacmanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man AI - Search Algorithms")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.pacman_pos = (1, 1)
        self.ghost_pos = (13, 18)
        self.food_pos = (13, 1)
        self.path = []
        self.path_index = 0
        self.algorithm = "A*"
        self.mode = "manual"
        self.nodes_expanded = 0
        self.use_adversarial = False
        
    def draw_maze(self):
        for row in range(MAZE_ROWS):
            for col in range(MAZE_COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if MAZE[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        for pos in self.path:
            x = pos[1] * CELL_SIZE + CELL_SIZE // 2
            y = pos[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.screen, ORANGE, (x, y), 3)
        
        fx = self.food_pos[1] * CELL_SIZE + CELL_SIZE // 2
        fy = self.food_pos[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, GREEN, (fx, fy), 8)
        
        gx = self.ghost_pos[1] * CELL_SIZE + CELL_SIZE // 2
        gy = self.ghost_pos[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, RED, (gx, gy), 15)
        
        px = self.pacman_pos[1] * CELL_SIZE + CELL_SIZE // 2
        py = self.pacman_pos[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, YELLOW, (px, py), 15)
        
    def draw_info(self):
        y_offset = MAZE_ROWS * CELL_SIZE + 10
        
        info_texts = [
            f"Algorithm: {self.algorithm} | Nodes Expanded: {self.nodes_expanded}",
            f"Mode: {self.mode.upper()} | Adversarial AI: {'ON' if self.use_adversarial else 'OFF'}",
            "Controls: 1=BFS 2=DFS 3=A* | SPACE=FindPath | A=Toggle Adversarial | M=Manual"
        ]
        
        for i, text in enumerate(info_texts):
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (10, y_offset + i * 25))
    
    def find_path(self):
        if self.algorithm == "BFS":
            path, nodes = bfs(MAZE, self.pacman_pos, self.food_pos)
        elif self.algorithm == "DFS":
            path, nodes = dfs(MAZE, self.pacman_pos, self.food_pos)
        else:
            path, nodes = astar(MAZE, self.pacman_pos, self.food_pos)
        
        self.path = path if path else []
        self.path_index = 0
        self.nodes_expanded = nodes
        self.mode = "auto" if path else "manual"
    
    def move_pacman_auto(self):
        if self.path and self.path_index < len(self.path):
            self.pacman_pos = self.path[self.path_index]
            self.path_index += 1
            
            if self.pacman_pos == self.food_pos:
                self.mode = "manual"
                self.path = []
    
    def move_pacman_manual(self, dx, dy):
        new_x = self.pacman_pos[0] + dx
        new_y = self.pacman_pos[1] + dy
        
        if (0 <= new_x < MAZE_ROWS and 0 <= new_y < MAZE_COLS and 
            MAZE[new_x][new_y] != 1):
            self.pacman_pos = (new_x, new_y)
    
    def move_ghost(self):
        if self.use_adversarial:
            move = get_ghost_move(MAZE, self.pacman_pos, self.ghost_pos, self.food_pos, 
                                 use_minimax=True, depth=2)
            if move:
                new_x = self.ghost_pos[0] + move[0]
                new_y = self.ghost_pos[1] + move[1]
                if 0 <= new_x < MAZE_ROWS and 0 <= new_y < MAZE_COLS and MAZE[new_x][new_y] != 1:
                    self.ghost_pos = (new_x, new_y)
        else:
            import random
            moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(moves)
            for dx, dy in moves:
                new_x = self.ghost_pos[0] + dx
                new_y = self.ghost_pos[1] + dy
                if 0 <= new_x < MAZE_ROWS and 0 <= new_y < MAZE_COLS and MAZE[new_x][new_y] != 1:
                    self.ghost_pos = (new_x, new_y)
                    break
    
    def run(self):
        running = True
        frame_count = 0
        
        while running:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.algorithm = "BFS"
                    elif event.key == pygame.K_2:
                        self.algorithm = "DFS"
                    elif event.key == pygame.K_3:
                        self.algorithm = "A*"
                    elif event.key == pygame.K_SPACE:
                        self.find_path()
                    elif event.key == pygame.K_a:
                        self.use_adversarial = not self.use_adversarial
                    elif event.key == pygame.K_m:
                        self.mode = "manual"
                        self.path = []
                    elif self.mode == "manual":
                        if event.key == pygame.K_UP:
                            self.move_pacman_manual(-1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move_pacman_manual(1, 0)
                        elif event.key == pygame.K_LEFT:
                            self.move_pacman_manual(0, -1)
                        elif event.key == pygame.K_RIGHT:
                            self.move_pacman_manual(0, 1)
            
            if self.mode == "auto" and frame_count % 10 == 0:
                self.move_pacman_auto()
            
            if frame_count % 8 == 0:
                self.move_ghost()
            
            self.draw_maze()
            self.draw_info()
            
            pygame.display.flip()
            self.clock.tick(30)
            frame_count += 1
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PacmanGame()
    game.run()
