import pygame, random
import re
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King
pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0,0,0)
LIGHT = (242,218,182)
DARK = (181,135,99)

start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
start_fen = "rn2k1r1/ppp1pp1p/3p2p1/5bn1/P7/2N2B2/1PPPPP2/2BNK1RR"

SCREENWIDTH=800
SCREENHEIGHT=800

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

#Set up pieces
def set_up_piece(color, coordinate_tuple, type):
    piece = type(color)
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
    return int(num)*100-100, (7-(ord(cha)-65))*100

#create board dict
bo = {}
for y in ['A','B','C','D','E','F','G','H']:
    for x in range(1,9):
        bo[f"{y}{x}"] = [(loc(y + str(x))), None]

def fen_insert(st, length, ind):
        return st[:ind] + length*'o' + st[ind+1:]

def has_numbers(inputString):
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

for i, field in enumerate(bo):
    co, ty = fen_code(start_fen[i])
    if ty is not None:
        piece = set_up_piece(co, bo[field][0], ty)
        all_sprites_list.add(piece)











#pawnloop

# black_pawns = {}
# white_pawns = {}
#
#
# A_pawn_black = set_up_piece('black', 0, 100, Pawn)
# B_pawn_black = set_up_piece('black', 100, 100, Pawn)
# C_pawn_black = set_up_piece('black', 200, 100, Pawn)
# D_pawn_black = set_up_piece('black', 300, 100, Pawn)
# E_pawn_black = set_up_piece('black', 400, 100, Pawn)
# F_pawn_black = set_up_piece('black', 500, 100, Pawn)
# G_pawn_black = set_up_piece('black', 600, 100, Pawn)
# H_pawn_black = set_up_piece('black', 700, 100, Pawn)
#
# black_pawns = [A_pawn_black, B_pawn_black, C_pawn_black, D_pawn_black, E_pawn_black, F_pawn_black, G_pawn_black, H_pawn_black]
#
# for pawn in black_pawns:
#     all_sprites_list.add(pawn)
#
# A_pawn_white = set_up_piece('white', 0, 600, Pawn)
# B_pawn_white = set_up_piece('white', 100, 600, Pawn)
# C_pawn_white = set_up_piece('white', 200, 600, Pawn)
# D_pawn_white = set_up_piece('white', 300, 600, Pawn)
# E_pawn_white = set_up_piece('white', 400, 600, Pawn)
# F_pawn_white = set_up_piece('white', 500, 600, Pawn)
# G_pawn_white = set_up_piece('white', 600, 600, Pawn)
# H_pawn_white = set_up_piece('white', 700, 600, Pawn)
#
# white_pawns = [A_pawn_white, B_pawn_white, C_pawn_white, D_pawn_white, E_pawn_white, F_pawn_white, G_pawn_white, H_pawn_white]
#
# for pawn in white_pawns:
#     all_sprites_list.add(pawn)
#
#
# x_knight_black = set_up_piece('black', 100, 0, Knight)
# y_knight_black = set_up_piece('black', 500, 0, Knight)
# x_bishop_black = set_up_piece('black', 200, 0, Bishop)
# y_bishop_black = set_up_piece('black', 600, 0, Bishop)
# x_rook_black = set_up_piece('black', 0, 0, Rook)
# y_rook_black = set_up_piece('black', 700, 0, Rook)
#
#
#
# x_knight_white = set_up_piece('white', 100, 700, Knight)
# y_knight_white = set_up_piece('white', 500, 700, Knight)
# x_bishop_white = set_up_piece('white', 200, 700, Bishop)
# y_bishop_white = set_up_piece('white', 600, 700, Bishop)
# x_rook_white = set_up_piece('white', 0, 700, Rook)
# y_rook_white = set_up_piece('white', 700, 700, Rook)
#
# queen_black = set_up_piece('black', 300, 0, Queen)
# queen_white = set_up_piece('white', 300, 700, Queen)
# king_black = set_up_piece('black', 400, 0, King)
# king_white = set_up_piece('white', 400, 700, King)
#
# pieces = [x_knight_black, y_knight_black, x_bishop_black, y_bishop_black, x_rook_black, y_rook_black, queen_black,
#           king_black, x_knight_white, y_knight_white, x_bishop_white, y_bishop_white, x_rook_white, y_rook_white,
#           queen_white, king_white]
#
# for piece in pieces:
#     all_sprites_list.add(piece)




black_knight = Knight('white')
black_knight.rect.x = 350
black_knight.rect.y = 350



# Add the knight to the list of objects


all_sprites_list.add(black_knight)

#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()

while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False

        mx, my = pygame.mouse.get_pos()
        black_knight.move(mx, my)


        #Game Logic
        all_sprites_list.update()

        #Drawing on Screen
        screen.fill(GREEN)

        #Draw The Board
        for y in range(8):
            y_loc = y * 100
            for i in range(8):
                x_loc = i*100
                if i % 2 == 0 and y % 2 == 1 or i % 2 == 1 and y % 2 == 0:
                    pygame.draw.rect(screen, DARK, pygame.Rect(x_loc,y_loc, x_loc+100,y_loc+100))

                else:
                    pygame.draw.rect(screen, LIGHT, pygame.Rect(x_loc,y_loc, x_loc+100,y_loc+100))



        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)

        #Refresh Screen
        pygame.display.flip()

        #Number of frames per secong e.g. 60
        clock.tick(60)

pygame.quit()
