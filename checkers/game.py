import pygame
import time
from checkers.board import Board
from checkers.constants import BLUE, WHITE, RED, SQUARE_SIZE, WIDTH, HEIGHT, PLAYER1_COLOR, PLAYER2_COLOR
from minimax.algorithm import minimax, clear_memo_table
from minimax.alpha_beta import alpha_beta, clear_transposition_table

USE_ALPHA_BETA = True 

class Game:
    def __init__(self, win, ai_game=True):
        self._init()
        self.win = win
        self.ai_game = ai_game
    
    def update(self):
        self.board.draw(self.win)
        winner = self.board.winner()
        if winner is not None:
            self.draw_winner(winner)
            pygame.display.update()
            pygame.time.delay(2000)
            return False
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        return True

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = PLAYER1_COLOR
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PLAYER1_COLOR:
            self.turn = PLAYER2_COLOR
        else:
            self.turn = PLAYER1_COLOR

    def ai_move(self):
        if USE_ALPHA_BETA:
            clear_transposition_table()
        else:
            clear_memo_table()
        
        max_time = 0.5  
        start_time = time.time()
        best_move = None
        best_val = float('-inf')
        
        depth = 1
        max_depth = 4  
        
        while depth <= max_depth and (time.time() - start_time) < max_time:
            if USE_ALPHA_BETA:
                val, move = alpha_beta(self.board, depth, float('-inf'), float('inf'), True, self)
            else:
                val, move = minimax(self.board, depth, True, self)
            
            if move:
                best_move = move
                best_val = val
            
            if best_val > 9000:
                break
                
            depth += 1
        
        if best_move:
            self.board = best_move
            self.change_turn()
        else:
            if USE_ALPHA_BETA:
                _, new_board = alpha_beta(self.board, 2, float('-inf'), float('inf'), True, self)
            else:
                _, new_board = minimax(self.board, 2, True, self)
            
            self.board = new_board
            self.change_turn()

    def draw_winner(self, winner):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.win.blit(s, (0, 0))
        
        font = pygame.font.SysFont('arial', 50)
        text = font.render(f"{'RED' if winner == PLAYER2_COLOR else 'BLACK'} WINS!", True, WHITE)
        self.win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        
        font = pygame.font.SysFont('arial', 30)
        restart = font.render("Click anywhere to continue", True, WHITE)
        self.win.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))
