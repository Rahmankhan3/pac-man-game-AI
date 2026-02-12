import random


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def evaluate_state(pacman_pos, ghost_pos, food_pos):
 
    
    ghost_dist = manhattan_distance(pacman_pos, ghost_pos)
    
    food_dist = manhattan_distance(pacman_pos, food_pos)
    
    if ghost_dist == 0:
        return -10000
    
    
    if food_dist == 0:
        return 10000
    
 
    score = (ghost_dist * 50) - (food_dist * 10)
    
    return score

def get_valid_moves(maze, pos):
    rows, cols = len(maze), len(maze[0])
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
    
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1:
            moves.append((dx, dy))
    
    return moves

def minimax_alpha_beta(maze, pacman_pos, ghost_pos, food_pos, depth, alpha, beta, is_maximizing):
    """
    Maximizing player: Pac-Man (wants high score)
    Minimizing player: Ghost (wants low score)
    """
   
    if depth == 0 or pacman_pos == ghost_pos or pacman_pos == food_pos:
        return evaluate_state(pacman_pos, ghost_pos, food_pos), None
    
    if is_maximizing:  #
        max_eval = float('-inf')
        best_move = None
        
        valid_moves = get_valid_moves(maze, pacman_pos)
        if not valid_moves:
            return evaluate_state(pacman_pos, ghost_pos, food_pos), None
        
        for dx, dy in valid_moves:
            new_pacman_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
            eval_score, _ = minimax_alpha_beta(maze, new_pacman_pos, ghost_pos, food_pos, 
                                               depth - 1, alpha, beta, False)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (dx, dy)
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  
        
        return max_eval, best_move
    
    else: 
        min_eval = float('inf')
        best_move = None
        
        valid_moves = get_valid_moves(maze, ghost_pos)
        if not valid_moves:
            return evaluate_state(pacman_pos, ghost_pos, food_pos), None
        
        for dx, dy in valid_moves:
            new_ghost_pos = (ghost_pos[0] + dx, ghost_pos[1] + dy)
            eval_score, _ = minimax_alpha_beta(maze, pacman_pos, new_ghost_pos, food_pos, 
                                               depth - 1, alpha, beta, True)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (dx, dy)
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break 
        
        return min_eval, best_move

def greedy_chase(maze, ghost_pos, pacman_pos):
    """Ghost simply moves toward Pac-Man using shortest distance"""
    valid_moves = get_valid_moves(maze, ghost_pos)
    
    if not valid_moves:
        return None
    
    best_move = None
    min_distance = float('inf')
    
    for dx, dy in valid_moves:
        new_pos = (ghost_pos[0] + dx, ghost_pos[1] + dy)
        distance = manhattan_distance(new_pos, pacman_pos)
        
        if distance < min_distance:
            min_distance = distance
            best_move = (dx, dy)
    
    return best_move


def get_ghost_move(maze, pacman_pos, ghost_pos, food_pos, use_minimax=True, depth=3):
    """
    Get the best move for ghost to chase Pac-Man
    use_minimax=True: Uses minimax (smarter but slower)
    use_minimax=False: Uses greedy chase (faster)
    """
    if use_minimax:
       
        _, move = minimax_alpha_beta(maze, pacman_pos, ghost_pos, food_pos, 
                                     depth, float('-inf'), float('inf'), False)
    else:
      
        move = greedy_chase(maze, ghost_pos, pacman_pos)
    
    return move if move else (0, 0)

# Get best move for Pac-Man (to evade ghost and reach food)
def get_pacman_move(maze, pacman_pos, ghost_pos, food_pos, depth=3):
   
    _, move = minimax_alpha_beta(maze, pacman_pos, ghost_pos, food_pos, 
                                 depth, float('-inf'), float('inf'), True)
    return move if move else (0, 0)
