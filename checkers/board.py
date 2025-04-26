import pygame
from .constants import BLACK, ROWS, BLUE, SQUARE_SIZE, COLS, WHITE, BOARD_DARK, BOARD_LIGHT, PLAYER1_COLOR, PLAYER2_COLOR
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BOARD_DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BOARD_LIGHT, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        
        white_score = self.white_left
        blue_score = self.red_left
        
        white_score += self.white_kings * 0.5
        blue_score += self.red_kings * 0.5
        
        center_white = 0
        center_blue = 0
        
        center_rows = range(2, 6)
        center_cols = range(2, 6)
        
        for row in center_rows:
            for col in center_cols:
                piece = self.board[row][col]
                if piece != 0:
                    if piece.color == PLAYER2_COLOR:
                        center_white += 0.3
                    else:
                        center_blue += 0.3
        
        white_score += center_white
        blue_score += center_blue
        
       
        for piece in self.get_all_pieces(PLAYER2_COLOR):
            if not piece.king:
                white_score += (piece.row * 0.1)
                
        for piece in self.get_all_pieces(PLAYER1_COLOR):
            if not piece.king:
                blue_score += ((ROWS - 1 - piece.row) * 0.1)
        
        white_mobility = 0
        blue_mobility = 0
        
        for piece in self.get_all_pieces(PLAYER2_COLOR):
            white_mobility += len(self.get_valid_moves(piece))
            
        for piece in self.get_all_pieces(PLAYER1_COLOR):
            blue_mobility += len(self.get_valid_moves(piece))
            
        white_score += white_mobility * 0.1
        blue_score += blue_mobility * 0.1
        
        return white_score - blue_score

    def get_all_pieces(self, color):
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    pieces.append(self.board[row][col])
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == PLAYER2_COLOR:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PLAYER2_COLOR))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PLAYER1_COLOR))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == PLAYER1_COLOR:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return PLAYER2_COLOR
        elif self.white_left <= 0:
            return PLAYER1_COLOR
        
        current_color = PLAYER1_COLOR if self.red_left > 0 else PLAYER2_COLOR
        for piece in self.get_all_pieces(current_color):
            if self.get_valid_moves(piece):
                return None
        
        return PLAYER2_COLOR if current_color == PLAYER1_COLOR else PLAYER1_COLOR
    
    def get_valid_moves(self, piece):
        if piece is None or piece == 0:
            return {}
        
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == PLAYER1_COLOR or piece.king:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        
        if piece.color == PLAYER2_COLOR or piece.king:
            moves.update(self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right))
        
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def get_board_state(self):
        state = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    state.append((row, col, piece.color, piece.king))
        return tuple(sorted(state))
    
    def copy(self):
        from copy import copy
        new_board = Board()
        new_board.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    from checkers.piece import Piece
                    new_piece = Piece(row, col, piece.color)
                    if piece.king:
                        new_piece.make_king()
                    new_board.board[row][col] = new_piece
        
        new_board.red_left = self.red_left
        new_board.white_left = self.white_left
        new_board.red_kings = self.red_kings
        new_board.white_kings = self.white_kings
        
        return new_board