import pygame
from copy import deepcopy
from checkers.constants import  PLAYER1_COLOR, PLAYER2_COLOR

transposition_table = {}

def alpha_beta(position, depth, alpha, beta, max_player, game):
    position_key = position.get_board_state()
    
    if position_key in transposition_table and transposition_table[position_key][0] >= depth:
        return transposition_table[position_key][1], transposition_table[position_key][2]
    
    if depth == 0 or position.winner() is not None:
        eval_score = position.evaluate()
        transposition_table[position_key] = (depth, eval_score, position)
        return eval_score, position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        
        all_moves = get_all_moves(position, PLAYER2_COLOR, game)
        ordered_moves = order_moves(all_moves, max_player)
        
        for move in ordered_moves:
            evaluation = alpha_beta(move, depth - 1, alpha, beta, False, game)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        
        if best_move:
            transposition_table[position_key] = (depth, maxEval, best_move)
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        
        all_moves = get_all_moves(position, PLAYER1_COLOR, game)
        ordered_moves = order_moves(all_moves, max_player)
        
        for move in ordered_moves:
            evaluation = alpha_beta(move, depth - 1, alpha, beta, True, game)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        
        if best_move:
            transposition_table[position_key] = (depth, minEval, best_move)
        
        return minEval, best_move

def order_moves(moves, max_player):
    return sorted(moves, key=lambda x: x.evaluate(), reverse=max_player)

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

def clear_transposition_table():
    global transposition_table
    transposition_table = {}
