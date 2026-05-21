import copy

def minimax(state, depth, moves, maximizing=True):
    # also add something about game over
    if depth == 0:
        return state.value
    
    if maximizing:
        max_num = -100
        # searches through all legal white moves
        # moves[0] is white moves, moves[1] is black moves
        for move in range(moves[0]):
            modified_moves = moves[0][:move] + moves[0][move+1:]
            board_clone = copy.deepcopy(state)
            board_clone.makeMove()
            node_value = minimax(state, depth-1, modified_moves, False).value
            max_num = max(max_num, node_value)
        return max_num
    
    else:
        max_num = 100
        # searches through all legal black moves
        # moves[1] is black moves
        for move in range(moves[1]):
            modified_moves = moves[1][:move] + moves[1][move+1:]
            board_clone = copy.deepcopy(state)
            board_clone.makeMove()
            node_value = minimax(state, depth-1, modified_moves, True).value
            min_num = min(max_num, node_value)
        return min_num
