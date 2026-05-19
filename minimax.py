import copy

def minimax(state, depth, moves, maximizing=True):
    # also add something about game over
    if depth == 0:
        return state
    
    if maximizing:
        max_num = -100
        # searches through all legal white moves
        # moves[0] is white moves, moves[1] is black moves
        for move in range(moves[0]):
            modified_moves = moves[0][:move] + moves[0][move+1:]
            board_clone = copy.deepcopy(state)
            board_clone.makeMove()
            node_eval = minimax(state, depth-1, modified_moves)
