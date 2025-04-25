import pygame
from copy import deepcopy
from checkers.constants import BLUE, WHITE, PLAYER1_COLOR, PLAYER2_COLOR

memo_table = {}

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game):
    position_key = position.get_board_state()

    if position_key in memo_table and memo_table[position_key][0] >= depth:
        return memo_table[position_key][1], memo_table[position_key][2]
    
    if depth == 0 or position.winner() != None:
        eval_score = position.evaluate()
        memo_table[position_key] = (depth, eval_score, position)
        return eval_score, position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        
        all_moves = get_all_moves(position, PLAYER2_COLOR, game)
        ordered_moves = sorted(all_moves, key=lambda x: x.evaluate(), reverse=True)
        
        for move in ordered_moves:
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        if best_move:
            memo_table[position_key] = (depth, maxEval, best_move)
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        
        all_moves = get_all_moves(position, PLAYER1_COLOR, game)
        ordered_moves = sorted(all_moves, key=lambda x: x.evaluate(), reverse=False)
        
        for move in ordered_moves:
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        if best_move:
            memo_table[position_key] = (depth, minEval, best_move)
        
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    
    return board

def get_all_moves(board, color, game):
    moves = []
    
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if hasattr(board, 'copy'):
                temp_board = board.copy()
            else:
                temp_board = deepcopy(board)
                
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

def clear_memo_table():
    global memo_table
    memo_table = {} 