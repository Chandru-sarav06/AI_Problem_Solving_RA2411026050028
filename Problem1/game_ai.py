import time
import math

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ''

class TicTacToeAI:
    def __init__(self):
        self.nodes_explored = 0
        self.win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]

    def evaluate(self, board):
        for condition in self.win_conditions:
            if board[condition[0]] != EMPTY and board[condition[0]] == board[condition[1]] == board[condition[2]]:
                if board[condition[0]] == PLAYER_O:
                    return 10
                elif board[condition[0]] == PLAYER_X:
                    return -10
        return 0

    def is_moves_left(self, board):
        return EMPTY in board

    def get_empty_cells(self, board):
        return [i for i, cell in enumerate(board) if cell == EMPTY]

    def minimax(self, board, depth, is_max):
        self.nodes_explored += 1
        score = self.evaluate(board)
        
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not self.is_moves_left(board):
            return 0
            
        if is_max:
            best = -math.inf
            for i in self.get_empty_cells(board):
                board[i] = PLAYER_O
                best = max(best, self.minimax(board, depth + 1, not is_max))
                board[i] = EMPTY
            return best
        else:
            best = math.inf
            for i in self.get_empty_cells(board):
                board[i] = PLAYER_X
                best = min(best, self.minimax(board, depth + 1, not is_max))
                board[i] = EMPTY
            return best

    def alphabeta(self, board, depth, alpha, beta, is_max):
        self.nodes_explored += 1
        score = self.evaluate(board)
        
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not self.is_moves_left(board):
            return 0
            
        if is_max:
            best = -math.inf
            for i in self.get_empty_cells(board):
                board[i] = PLAYER_O
                val = self.alphabeta(board, depth + 1, alpha, beta, not is_max)
                best = max(best, val)
                alpha = max(alpha, best)
                board[i] = EMPTY
                if beta <= alpha:
                    break
            return best
        else:
            best = math.inf
            for i in self.get_empty_cells(board):
                board[i] = PLAYER_X
                val = self.alphabeta(board, depth + 1, alpha, beta, not is_max)
                best = min(best, val)
                beta = min(beta, best)
                board[i] = EMPTY
                if beta <= alpha:
                    break
            return best

    def get_best_move(self, board, use_alphabeta=True):
        best_val = -math.inf
        best_move = -1
        self.nodes_explored = 0
        
        start_time = time.perf_counter()
        
        empty_cells = self.get_empty_cells(board)
        
        if len(empty_cells) == 9:
            # First move optimization to center
            best_move = 4
        else:
            for i in empty_cells:
                board[i] = PLAYER_O
                if use_alphabeta:
                    move_val = self.alphabeta(board, 0, -math.inf, math.inf, False)
                else:
                    move_val = self.minimax(board, 0, False)
                board[i] = EMPTY
                
                if move_val > best_val:
                    best_move = i
                    best_val = move_val
                    
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000 # in ms
        
        return best_move, execution_time, self.nodes_explored

    def check_winner(self, board):
        score = self.evaluate(board)
        if score == 10:
            return PLAYER_O
        elif score == -10:
            return PLAYER_X
        elif not self.is_moves_left(board):
            return "Tie"
        return None
