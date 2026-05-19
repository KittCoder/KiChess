import pygame
import board

# intialize pygame

pygame.init()
SIZE = (600, 600)
screen = pygame.display.set_mode(SIZE)

# import board image and scale it appropriately

BOARD = pygame.image.load("images/board.png").convert()

SCALED_BOARD = pygame.transform.scale(BOARD, SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PIECE_VALUES = {'wp':-1,
                'wN':-3,
                'wB':-3,
                'wR':-5,
                'wQ':-9,
                'bp':1,
                'bN':3,
                'bB':3,
                'bR':5,
                'bQ':9,
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

def is_valid(piece, move, position):

    print(position)

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
        print('QUEEN')
        if abs(int(move_list[0])) != abs(int(move_list[1])):
            return False
        else:
            return True
    
    if piece[1] == 'K':
        if -1 <= int(move_list[0]) <= 1 and -1 <= int(move_list[1]) <= 1:
            return True
        else:
            return False

    # allows pawns to move 2 squares in their first move
    if piece == "wp" and position[0] == 6:
        movespieces[piece].append('0 -2')
    elif piece == "bp" and position[0] == 1:
        movespieces[piece].append('0 2')

    # allows pawns to take diagonally
    if piece == "wp":
        if state.board[position[0]-1][position[1]+1] != '__':
            print(state.board[position[0]-2][position[1]+1])
            movespieces[piece].append('1 -1')
        if state.board[position[0]-1][position[1]-1] != '__':
            print(state.board[position[0]-2][position[1]-1])
            movespieces[piece].append('-1 -1')
    
    if piece == "bp":
        if state.board[position[0]+1][position[1]+1] != '__':
            print(state.board[position[0]-2][position[1]+1])
            movespieces[piece].append('1 1')
        if state.board[position[0]+1][position[1]-1] != '__':
            print(state.board[position[0]-2][position[1]-1])
            movespieces[piece].append('-1 1')
    
    print(movespieces['wp'], move)

    if move is not None:
        if move in movespieces[piece]:
            return True
        else:
            return False

def friendlyFire(piece, position):
    if state.board[position[0]][position[1]] != "__":
        if piece[0] == state.board[position[0]][position[1]][0]:
            return True
    return False

# checks a move's legality by seeing if it can skip over pieces, and if not, then if it does so
def is_Skip(piece, move, position):

    skip_list = []

    move_list = move.split(" ")

    if piece[1] == 'B':
            x_norm = int(move_list[0])//abs(int(move_list[0]))
            y_norm = int(move_list[1])//abs(int(move_list[1]))
    else:
        if int(move_list[0]) > 0:
            x_norm = int(move_list[0])//abs(int(move_list[0]))
            y_norm = 0
        else:
            y_norm = int(move_list[1])//abs(int(move_list[1]))
            x_norm = 0

    if piece[1] == 'B' or piece[1] == 'Q':

        for elt in range(abs(int(move_list[0]))):
            square = state.board[position[0] + (elt * y_norm)][position[1] + (elt * x_norm)]
            skip_list.append(square)
            if 0 < elt < abs(int(move_list[0])) and square != '__':
                return True
            
    if piece[1] == 'R' or piece[1] == 'Q':

        for elt in range(abs(int(move_list[0]) + int(move_list[1]))):
            square = state.board[position[0] + (elt * y_norm)][position[1] + (elt * x_norm)]
            skip_list.append(square)
            print(square)
            if 0 < elt and square != '__':
                return True
    
    print(skip_list)

    return False

def getLegalMoves(board):
    pass

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

    def makeMove(self, piece, piece_square, move_square, move):
        global searching
        if is_valid(piece, move, piece_square) == True and friendlyFire(piece, move_square) == False and is_Skip(piece, move, piece_square) == False:

                    if self.board[move_square[0]][move_square[1]] != "__":
                        taken_pieces[state.turn].append(self.board[move_square[0]][move_square[1]])
                        self.value += PIECE_VALUES[self.board[move_square[0]][move_square[1]]]

                    self.board[move_square[0]][move_square[1]] = piece
                    self.board[piece_square[0]][piece_square[1]] = "__"

                    if self.turn == 'w':
                        self.turn = 'b'
                    else:
                        self.turn = 'w'
                    
                    searching = True

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

taken_pieces = {'w':[],
                'b':[]}

# run is the game loop boolean, and searching dictates whether to search for valid moves or not (to save memory)
run = True
searching = True

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
        if searching:
            for row1 in squares:
                for fsquare in row1:
                    if square.position == fsquare.position:
                        continue
                    og_square = square.position
                    f_square = fsquare.position
                    move = f'{f_square[1] - og_square[1]} {f_square[0] - og_square[0]}'
                    piece = state.board[og_square[0]][og_square[1]]
                    if piece[0] != state.turn:
                        continue
                    if is_valid(piece, move, og_square) == True and friendlyFire(piece, og_square) == False and is_Skip(piece, move, og_square) == False:
                        valid_moves.append((og_square, piece, move))
            searching = False

        if selected_piece is not None:
            if square.rect.collidepoint(selected_piece):
                p_square = square.position
                print(p_square)
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
        if selected_point is not None:
            if square.rect.collidepoint(selected_point):
                s_square = square.position
                
                move = f'{s_square[1] - p_square[1]} {s_square[0] - p_square[0]}'

                # validity checked -> when the move is actually made
                state.makeMove(piece, p_square, s_square, move)

                piece = None
                
                selected_piece = None
                selected_point = None
                p_square = None
                s_square = None
                piece = None

    print(state.value)

    state.drawBoard()

    pygame.display.update()