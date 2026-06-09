import copy

def minimax(state, depth, move_lin, maximizing=True):
    # also add something about game over
    if depth == 0:
        return (state.value, [])
    
    state.getLegalMoves()

    if maximizing:
        max_num = -100
        # searches through all legal white moves
        # moves[0] is white moves, moves[1] is black moves

        # move is indexed (piece position, piece, move)
        for move in state.legal_moves:
            move_lin1 = list(move_lin)
            move_lin1.append(move)
            move_row = move[0][0]+int(move[2].split(' ')[1])
            move_column = move[0][1]+int(move[2].split(' ')[0])
            move_square = (move_row, move_column)
            board_clone = copy.deepcopy(state)
            board_clone.makeMove(move[1], move[0], move_square, move[2])
            node_value = minimax(board_clone, depth-1, move_lin1, False)[0]

            max_num = max(max_num, node_value)

        return (max_num, move_lin1)
    
    else:
        min_num = 100
        # searches through all legal black moves
        # moves[1] is black moves
        for move in state.legal_moves:
            move_lin1 = list(move_lin)
            move_lin1.append(move)
            board_clone = copy.deepcopy(state)
            move_row = move[0][0]+int(move[2].split(' ')[1])
            move_column = move[0][1]+int(move[2].split(' ')[0])
            move_square = (move_row, move_column)
            board_clone.makeMove(move[1], move[0], move_square, move[2])
            node_value = minimax(board_clone, depth-1, move_lin1, True)[0]

            min_num = min(min_num, node_value)

        return (min_num, move_lin1)

def minimaxWithAB(state, depth, alpha, beta, move_lin, maximizing=True):
    # also add something about game over
    if depth == 0:
        return (state.value, [])
    
    state.getLegalMoves()
    if maximizing:
        max_num = -100
        # searches through all legal white moves
        # moves[0] is white moves, moves[1] is black moves

        # move is indexed (piece position, piece, move)
        for move in state.legal_moves:
            move_lin1 = list(move_lin)
            move_lin1.append(move)

            move_row = move[0][0]+int(move[2].split(' ')[1])
            move_column = move[0][1]+int(move[2].split(' ')[0])
            move_square = (move_row, move_column)
            board_clone = copy.deepcopy(state)
            board_clone.makeMove(move[1], move[0], move_square, move[2])
            node_value = minimaxWithAB(board_clone, depth-1, alpha, beta, move_lin1, False)[0]

            if node_value > max_num:
                best_lin = move_lin1

            max_num = max(max_num, node_value)

            # the alpha-beta pruning part eliminates unnecceary move computation
            alpha = max(alpha, node_value)

            if beta <= alpha:
                break
            
        return (max_num, best_lin)
    
    else:
        min_num = 100
        # searches through all legal black moves
        # moves[1] is black moves
        for move in state.legal_moves:
            move_lin1 = list(move_lin)
            move_lin1.append(move)

            board_clone = copy.deepcopy(state)
            move_row = move[0][0]+int(move[2].split(' ')[1])
            move_column = move[0][1]+int(move[2].split(' ')[0])
            move_square = (move_row, move_column)
            board_clone.makeMove(move[1], move[0], move_square, move[2])
            node_value = minimaxWithAB(board_clone, depth-1, alpha, beta, move_lin1, True)[0]

            if node_value < min_num:
                best_lin = move_lin1

            min_num = min(min_num, node_value)

            # the alpha-beta pruning part eliminates unnecceary move computation
            beta = min(beta, node_value)

            if beta <= alpha:
                break

        return (min_num, best_lin)
