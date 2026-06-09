import pygame
import minimax

# intialize pygame

pygame.init()
SIZE = (600, 600)
screen = pygame.display.set_mode(SIZE)

# import board image and scale it appropriately

BOARD = pygame.image.load("images/board.png").convert()

SCALED_BOARD = pygame.transform.scale(BOARD, SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PIECE_VALUES = {'wp':1,
                'wN':3,
                'wB':3,
                'wR':5,
                'wQ':9,
                'bp':-1,
                'bN':-3,
                'bB':-3,
                'bR':-5,
                'bQ':-9,
                'wK':0,
                'bK':0,
                '__':0}

# define functions

def getImages():
    # images is really "scaled images"
    images = [[],[]]
    original_images = [["white-pawn.png", "white-knight.png", "white-bishop.png", "white-rook.png", "white-queen.png", "white-king.png"],
              ["black-pawn.png", "black-knight.png", "black-bishop.png", "black-rook.png", "black-queen.png", "black-king.png"]]
    for i in range(2):
        for j in range(6):
            image = pygame.image.load("images/" + original_images[i][j]).convert_alpha()
            images[i].append(pygame.transform.scale(image, (30,30)))
    return images
    

def getCoordinates():
        l = []
        for i in range(8):
            l.append([])
            y = 22 + (i * 75)
            for j in range(8):
                x = 22 + (j * 75)
                l[i].append((x, y))
        return l

def makeBoard():
    squares = []
    coordinates = getCoordinates()
    for i in range(8):
        l = []
        for j in range(8):
            if i%2 == 0 and j%2 == 0:
                l.append(Square(WHITE, 75, (i, j)))
            elif i%2 == 1 and j%2 == 1:
                l.append(Square(WHITE, 75, (i, j)))
            else:
                l.append(Square(BLACK, 75, (i, j)))
        squares.append(l)
        
    return squares

def isValid(piece, move, position, state):
    move_list = move.split(" ")

    # list of valid moves for each piece
    movespieces = {"wp":['0 -1'],
                   "bp":['0 1'],
                   "bP":['0 -1'],
                   "wN": ['1 2', '1 -2', '-1 2', '-1 -2', '2 1', '2 -1', '-2 1', '-2 -1'],
                   "bN": ['1 2', '1 -2', '-1 2', '-1 -2', '2 1', '2 -1', '-2 1', '-2 -1'],
                   }

    # for rooks/queens
    if piece[1] == 'R' or piece[1] == 'Q':
        if move_list[0] != '0':
            if move_list[1] != '0':
                if piece[1] == 'R':
                    return False
            else:
                return True
        else:
            return True
        
    # for bishops/queens
    if piece[1] == 'B' or piece[1] == 'Q':
        if abs(int(move_list[0])) != abs(int(move_list[1])):
            return False
        else:
            return True
    
    if piece[1] == 'K':
        if -1 <= int(move_list[0]) <= 1 and -1 <= int(move_list[1]) <= 1:
            return True
        else:
            return False

    try:
        # allows pawns to move 2 squares in their first move
        if piece == "wp" and position[0] == 6:
            movespieces[piece].append('0 -2')
        elif piece == "bp" and position[0] == 1:
            movespieces[piece].append('0 2')

        
        if piece == "wp":
            # allows white pawns to take diagonally
            if state.board[position[0]-1][position[1]+1] != '__':
                movespieces[piece].append('1 -1')
            if state.board[position[0]-1][position[1]-1] != '__':
                movespieces[piece].append('-1 -1')

            # allows white pawns to do en passant
            if state.passant_square is not None:
                if position[0] == state.passant_square[0] and (position[1] + 1) == state.passant_square[1]:
                    movespieces[piece].append('1 -1')
                if position[0] == state.passant_square[0] and (position[1] - 1) == state.passant_square[1]:
                    movespieces[piece].append('-1 -1')

        if piece == "bp":
            # allows black pawns to take diagonally
            if state.board[position[0]+1][position[1]+1] != '__':
                movespieces[piece].append('1 1')
            if state.board[position[0]+1][position[1]-1] != '__':
                movespieces[piece].append('-1 1')
            
            # allows black pawns to do en passant
            if state.passant_square is not None:
                if position[0] == state.passant_square[0] and (position[1] + 1) == state.passant_square[1]:
                    movespieces[piece].append('1 1')
                if position[0] == state.passant_square[0] and (position[1] - 1) == state.passant_square[1]:
                    movespieces[piece].append('-1 1')

    except:
        return False
    
    if move is not None:
        if move in movespieces[piece]:
            return True
        else:
            return False

# takes the piece in question and the destination of the piece as input
def friendlyFire(piece, destination, board):
    if board[destination[0]][destination[1]] != "__":
        if piece[0] == board[destination[0]][destination[1]][0]:
            return True
    return False

# checks a move's legality by seeing if it can skip over pieces, and if not, then if it does so
def is_Skip(piece, move, position, board):

    skip_list = []

    move_list = move.split(" ")

    x = int(move_list[0])
    y = int(move_list[1])

    if x != 0:
        x_norm = x//abs(x)
    else:
        x_norm = 0
    
    if y != 0:
        y_norm = y//abs(y)
    else:
        y_norm = 0

    # if piece[1] == 'B':
    #         x_norm = int(move_list[0])//abs(int(move_list[0]))
    #         y_norm = int(move_list[1])//abs(int(move_list[1]))
    # else:
    #     if int(move_list[0]) > 0:
    #         x_norm = int(move_list[0])//abs(int(move_list[0]))
    #         y_norm = 0
    #     else:
    #         y_norm = int(move_list[1])//abs(int(move_list[1]))
    #         x_norm = 0
    if piece[1] == 'Q' and 0 in (x, y):
        rook_like = True
    else:
        rook_like = False
    
    if piece[1] == 'Q' and abs(x) == abs(y):
        bishop_like = True
    else:
        bishop_like = False

    if piece[1] == 'B' or bishop_like:

        for elt in range(abs(int(move_list[0]))):
            square = board[position[0] + (elt * y_norm)][position[1] + (elt * x_norm)]
            skip_list.append(square)
            if 0 < elt < abs(int(move_list[0])) and square != '__':
                return True
            
    if piece[1] == 'R' or rook_like:

        for elt in range(abs(int(move_list[0]) + int(move_list[1]))):
            square = board[position[0] + (elt * y_norm)][position[1] + (elt * x_norm)]
            skip_list.append(square)
            if 0 < elt and square != '__':
                return True

    return False

# define classes

class State():
    def __init__(self):
        # initial state
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.coordinates = getCoordinates()
        self.turn = "w"
        self.pastMoves = []
        self.canCastle = True
        self.move_num = 0
        self.value = 0
        self.passant_square = None
        self.legal_moves = []

    def drawBoard(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]

                # checks white pieces
                if piece == "wp":
                    screen.blit(images[0][0], self.coordinates[i][j])
                elif piece == "wN":
                    screen.blit(images[0][1], self.coordinates[i][j])
                elif piece == "wB":
                    screen.blit(images[0][2], self.coordinates[i][j])
                elif piece == "wR":
                    screen.blit(images[0][3], self.coordinates[i][j])
                elif piece == "wQ":
                    screen.blit(images[0][4], self.coordinates[i][j])
                elif piece == "wK":
                    screen.blit(images[0][5], self.coordinates[i][j])
                
                # checks black pieces
                elif piece == "bp":
                    screen.blit(images[1][0], self.coordinates[i][j])
                elif piece == "bN":
                    screen.blit(images[1][1], self.coordinates[i][j])
                elif piece == "bB":
                    screen.blit(images[1][2], self.coordinates[i][j])
                elif piece == "bR":
                    screen.blit(images[1][3], self.coordinates[i][j])
                elif piece == "bQ":
                    screen.blit(images[1][4], self.coordinates[i][j])
                elif piece == "bK":
                    screen.blit(images[1][5], self.coordinates[i][j])
                
                else:
                    continue
    
    def updateValue(self):
        self.value = 0
        for row in self.board:
            for piece in row:
                self.value += PIECE_VALUES[piece]
    
    def isCastle(self, piece, piece_square, move_square, move):
        move_list = move.split(' ')
        # checks on white's turn with according row
        if self.turn == 'w':
            if piece[1] == 'K' and piece_square[0] == 7:
                if move_list[0] == '2' and self.board[7][7] == "wR" and friendlyFire(piece, move_square, self.board) == False and is_Skip(piece, move, piece_square, self.board) == False:
                    return True
                if move_list[0] == '-2' and self.board[7][0] == "wR" and friendlyFire(piece, move_square, self.board) == False and is_Skip(piece, move, piece_square, self.board) == False:
                    return True
                else:
                    return False
        
        # checks on black's turn with according row
        if self.turn == 'b':
            if piece[1] == 'K' and piece_square[0] == 0:
                if move_list[0] == '2' and self.board[0][7] == "bR" and friendlyFire(piece, move_square, self.board) == False and is_Skip(piece, move, piece_square, self.board) == False:
                    return True
                if move_list[0] == '-2' and self.board[0][0] == "bR" and friendlyFire(piece, move_square, self.board) == False and is_Skip(piece, move, piece_square, self.board) == False:
                    return True
                else:
                    return False
        return False

    def makeCastle(self, piece, piece_square, move_square, move):
        if self.isCastle(piece, piece_square, move_square, move) == True:
            self.board[piece_square[0]][piece_square[1]] = '__'

            if move[0] == '-':
                # white queenside castle
                if self.turn == 'w':
                    self.board[7][2] = 'wK'
                    self.board[7][3] = 'wR'
                    self.board[7][0] = '__'
                # black queenside castle
                else:
                    self.board[0][2] = 'bK'
                    self.board[0][3] = 'bR'
                    self.board[0][0] = '__'
            else:
                # white kingside castle
                if self.turn == 'w':
                    self.board[7][6] = 'wK'
                    self.board[7][5] = 'wR'
                    self.board[7][7] = '__'
                # black kingside castle
                else:
                    self.board[0][6] = 'bK'
                    self.board[0][5] = 'bR'
                    self.board[0][7] = '__'

            # change turns
            if self.turn == 'w':
                self.turn = 'b'
            else:
                self.turn = 'w'


    def makeMove(self, piece, piece_square, move_square, move):

        if isValid(piece, move, piece_square, self) == True and friendlyFire(piece, move_square, self.board) == False and is_Skip(piece, move, piece_square, self.board) == False:

                    if self.board[move_square[0]][move_square[1]] != "__":
                        taken_pieces[self.turn].append(self.board[move_square[0]][move_square[1]])
                        self.value += PIECE_VALUES[self.board[move_square[0]][move_square[1]]]

                    self.board[move_square[0]][move_square[1]] = piece
                    self.board[piece_square[0]][piece_square[1]] = "__"

                    if self.turn == 'w':
                        self.turn = 'b'
                    else:
                        self.turn = 'w'

                    if piece[1] == 'p':
                        if int(move.split(' ')[0]) != 0:
                            if self.passant_square is not None:
                                # the y-coordinate will change regardless, if the new x-coordinate equals that of the passant square, it was taken
                                if (piece_square[1] + int(move.split(' ')[0])) == self.passant_square[1]:
                                    self.board[self.passant_square[0]][self.passant_square[1]] = '__'
                                    # if it was just white's turn
                                    if self.turn == 'b':
                                        self.value += 1
                                    else:
                                        self.value -= 1

                        if abs(int(move.split(' ')[1])) == 2:
                            self.passant_square = move_square
                        else:
                            self.passant_square = None
                    else:
                        self.passant_square = None

        elif self.isCastle(piece, piece_square, move_square, move) == True:
            self.makeCastle(piece, piece_square, move_square, move)
            print("It's a castle!")
                    
    def getLegalMoves(self):
        self.legal_moves = []
        for row in range(8):
            for i in range(8):
                for row1 in range(8):
                    for j in range(8):
                        i_position = (row, i)
                        j_position = (row1, j)
                        if i_position == j_position:
                            continue
                        move = f'{j_position[1] - i_position[1]} {j_position[0] - i_position[0]}'
                        piece = self.board[i_position[0]][i_position[1]]
                        if piece[0] != self.turn:
                            continue
                        if isValid(piece, move, i_position,  self) == True and friendlyFire(piece, j_position,  self.board) == False and is_Skip(piece, move, i_position,  self.board) == False:
                            # the form within the list of legal moves is (position of piece, piece, legal move from position)
                            self.legal_moves.append((i_position, piece, move))

coordinates = getCoordinates()

class Square(pygame.sprite.Sprite):
    def __init__(self, color, size, position):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.position = position

        self.rect = self.image.get_rect()
        self.rect.topleft = (coordinates[position[0]][position[1]][0]-22, coordinates[position[0]][position[1]][1]-22)

# initialize variables

images = getImages()
state = State()
squares = makeBoard()

selected_piece = None
p_square = None
selected_point = None
s_square = None
best_move = None
best_value = None
maximizing = True

taken_pieces = {'w':[],
                'b':[]}

# run is the game loop boolean
run = True

while run:
    
    screen.fill((0, 0, 0))
    
    mouse_pos = pygame.mouse.get_pos() 

    valid_moves = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if selected_piece == None:
                selected_piece = mouse_pos
            else:
                selected_point = mouse_pos
                if p_square is not None:
                    piece_img = state.board[p_square[0]][p_square[1]]
        #elif event.type == pygame.MOUSEBUTTONUP:
            # IF THIS BECOMES AN ERROR LATER WITH CLICKING OUTSIDE OF THE BOARD REGION: make the entire board a single sprite, 
            # and make it a condition that this only holds if collide_rect with the board sprite
            #selected_point = None

    for row in squares:
       
       for square in row:
        # draws each piece
        screen.blit(square.image, square.rect.topleft)

        # checks if valid moves needs to be updated, then does a very strenuous loop

        if selected_piece is not None:
            if square.rect.collidepoint(selected_piece):
                p_square = square.position
                piece = str(state.board[p_square[0]][p_square[1]])
                if piece[0] != state.turn:
                    selected_piece = None
                    piece = None
                    p_square = None
                if piece == "__":
                    selected_piece = None
                    piece = None
                    p_square = None

        # operations involving the square that is selected to move to
        if selected_point is not None and p_square is not None:
            if square.rect.collidepoint(selected_point):
                s_square = square.position

                move = f'{s_square[1] - p_square[1]} {s_square[0] - p_square[0]}'

                if isValid(piece, move, p_square, state) == True and friendlyFire(piece, s_square, state.board) == False and is_Skip(piece, move, p_square, state.board) == False:
                    runmini = True
                else:
                    runmini = False

                # validity checked -> when the move is actually made
                state.makeMove(piece, p_square, s_square, move)

                if state.turn == 'b':
                    maximizing = False
                else:
                    maximizing = True

                if runmini:
                    minimaxed = minimax.minimaxWithAB(state, 3, -100, 100, [], maximizing)
                    best_move = minimaxed[1][0]
                    best_value = minimaxed[0]
                runmini = False
                
                print(best_move, best_value)

                piece = None
                
                selected_piece = None
                selected_point = None
                p_square = None
                s_square = None
                piece = None

    state.drawBoard()

    pygame.display.update()