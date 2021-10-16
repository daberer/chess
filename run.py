import pygame, random
import re
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King, Player
from move import Move
pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0,0,0)
LIGHT = (242,218,182)
DARK = (181,135,99)

#TODO: fix fen set up (Queen and King are set conversly)
start_fen = 'rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR'
#start_fen = "rn2k1r1/ppp1pp1p/3p2p1/5bn1/P7/2N2B2/1PPPPP2/2BNK1RR"

SCREENWIDTH=800
SCREENHEIGHT=800

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")
font = pygame.font.SysFont(None, 100)

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

#Set up pieces
def set_up_piece(color, coordinate_tuple, kind, field):
    piece = kind(color, field)
    piece.rect.x = coordinate_tuple[0]
    piece.rect.y = coordinate_tuple[1]
    return piece

#translate field into x,y
def fen_code(sign):
    """
    translates Forsyth-Edward-Notation into the corresponding chess piece
    :param sign: str of fen code
    :return: color and type of piece
    """
    assert(type(sign) == str)
    if sign.isupper():
        col = 'white'
    else:
        col = 'black'
    sign = sign.lower()
    if sign == 'p':
        ret = Pawn
    elif sign == 'n':
        ret = Knight
    elif sign == 'b':
        ret = Bishop
    elif sign == 'r':
        ret = Rook
    elif sign == 'q':
        ret = Queen
    elif sign == 'k':
        ret = King
    elif sign == 'o':
        ret = None
    else:
        raise Exception(f'{sign} is not a valid sign:')

    return col, ret



def loc(str):
    """
    translates string containing name of field into coordinates
    :param str: string of length two, containing char and number ("A1")
    :return:
    x and y coordinates each ranging from 0 - 700 in steps of 100.
    H1 is 0,0, A8 is 700,700
    """
    assert(len(str)==2)
    cha = list(str)[0]
    num = list(str)[1]
    return ((ord(cha)-65))*100, 800-int(num)*100

#create board dict
bo = {}
ob = {}
for x in range(1,9):
    for y in ['A','B','C','D','E','F','G','H']:
        bo[f"{y}{x}"] = [(loc(y + str(x))), None]
        ob[(loc(y + str(x)))] = f"{y}{x}"



def fen_insert(st, length, ind):
    """
    inserts up to eight "o" characters into an input string instead of an integer 1-8 at a given index.
    :param st: string, that is being added to
    :param length: int, number of times "o" is being added to st
    :param ind: int, index where int is located in st.
    :return:
    """
    return st[:ind] + length*'o' + st[ind+1:]

def has_numbers(inputString):
    """
    Checks input string for numbers.
    :param inputString:
    :return: True if inputString has number.
    """
    return bool(re.search(r'\d', inputString))

def extend_fen(fen):
    """
    replace the number for number of empty fields in the fen notation with 'o' times the number
    rn3k becomes rnoook
    :param fen:
    :return:
    """
    ext_fen = (fen + '.')[:-1]
    while has_numbers(ext_fen):
        ind = None
        match = re.search(r"\d", ext_fen)
        if match:
            ind = match.start()
            ext_fen = fen_insert(ext_fen, int(ext_fen[ind]), ind)
    return ext_fen

start_fen = start_fen.replace('/','')
start_fen = extend_fen(start_fen)
start_fen = start_fen[::-1]

for i, field in enumerate(bo):
    co, ty = fen_code(start_fen[i])
    if ty is not None:
        piece = set_up_piece(co, bo[field][0], ty, field)
        bo[field][1] = piece
        all_sprites_list.add(piece)



#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()
score = 0
pl = Player()
all_sprites_list.add(pl)


#Drawing on Screen
screen.fill(GREEN)


#board = pygame.sprite.Group()
fields = [(i * 100, j * 100) for j in range(8) for i in range(8)]

game_over = False

def go_home(piece):
    """
    Return piece to position it had prior to move
    :param piece:
    :return:
    """
    piece.rect.x = bo[piece.field][0][0]
    piece.rect.y = bo[piece.field][0][1]
    return False

def update(piece, piecex, piecey):
    """
    Update dictionary with positions
    :param piece:
    :param piecex:
    :param piecey:
    :return:
    """
    if (piece.color == 'white' and piecey == 0) or (piece.color == 'black' and piecey == 700):
        field = piece.field
        piece.kill()
        piece = set_up_piece(piece.color, (piecex, piecey), Queen, field)

        all_sprites_list.add(piece)

    bo[ob[piecex, piecey]][1] = piece
    bo[piece.field][1] = None
    piece.field = ob[piecex, piecey]
    return True

def legal(mv, piece, piecex, piecey, old_inhabitant):
    # check if move is legal
        if mv.isthisallowed():
            if mv.noroadblocks():
                piece.rect.x = piecex
                piece.rect.y = piecey

                if old_inhabitant != None:# check if someone is there
                    if piece.color != old_inhabitant.color:
                        old_inhabitant.kill()
                        return update(piece, piecex, piecey)
                    else:
                        return go_home(piece)
                else:
                    return update(piece, piecex, piecey)
            else:
                return go_home(piece)
        else:
            return go_home(piece)

def execute_move(move_count, computer_move=True):
    col = 'black'
    if move_count % 2 == 0:
        col = 'white'
    if computer_move:
        possible_pieces = []
        for b in bo:
            if bo[b][1] != None:
                if bo[b][1].color == col:
                    possible_pieces.append(bo[b][1])
        piece = random.choice(possible_pieces)
        possible_fields = []
        for b in bo:
            possible_fields.append(b)
        while len(possible_fields):
            goal = random.choice(possible_fields)
            possible_fields.remove(goal)
            old_inhabitant = bo[goal][1]
            mv = Move(bo[piece.field][0], bo[goal][0], piece, old_inhabitant, bo, ob)
            if legal(mv, piece, bo[goal][0][0], bo[goal][0][1], old_inhabitant):
                return True


    if len(pl.carry_pieces_list) > 0:
        piece = pl.carry_pieces_list[0]
        pl.carry_pieces_list = []

        if move_count % 2 == 0 and piece.color == 'black':
            go_home(piece)
        elif move_count % 2 != 0 and piece.color == 'white':
            go_home(piece)
        piecex = round(piece.rect.x, -2)
        piecey = round(piece.rect.y, -2)
        old_inhabitant = bo[ob[piecex, piecey]][1]
        mv = Move(bo[piece.field][0], (piecex, piecey), piece, old_inhabitant, bo, ob)
        return legal(mv, piece, piecex, piecey, old_inhabitant)





def check_game_over():
    two = 0
    for s in  all_sprites_list.sprites():
        if type(s) == King:
            two += 1
    if two == 2:
        return False
    return True


def end_game():
    color = None
    for s in  all_sprites_list.sprites():
        if type(s) == King:
            color = s.color
    text_surface = font.render(f'{color} wins!', True, (64, 224, 208))
    screen.blit(text_surface, dest=(200,350))
    pygame.display.flip()
    import time
    time.sleep(5)
    pygame.quit()

def draw_board():
    for i, field in enumerate(fields):
        if (i + int(i / 8)) % 2 == 0:
            pygame.draw.rect(screen, DARK, pygame.Rect(field[0],field[1], 100,100))
        else:
            pygame.draw.rect(screen, LIGHT, pygame.Rect(field[0],field[1], 100,100))

game_over = False
move_count = 0

while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                 carryOn=False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                blocks_hit_list = pygame.sprite.spritecollide(pl, all_sprites_list, False)
                for i, block in enumerate(blocks_hit_list):
                    if block.name() == 'Player':
                        blocks_hit_list.pop(i)
                # prevent more than one pieces from being picked up
                if len(blocks_hit_list) > 1:
                    pl.carry_pieces_list = [blocks_hit_list[0]]
                else:
                    pl.carry_pieces_list = blocks_hit_list



            elif True: #event.type == pygame.MOUSEBUTTONUP:
                import time
                time.sleep(0.1)
                correct_move = execute_move(move_count, computer_move=True)
                if correct_move:
                    move_count += 1
                    game_over = check_game_over()



            draw_board()



            all_sprites_list.update()



            #Now let's draw all the sprites in one go.
            all_sprites_list.draw(screen)

            #Refresh Screen
            pygame.display.flip()
            if game_over:
                end_game()

            #Number of frames per secong e.g. 60
            clock.tick(200)

pygame.quit()
