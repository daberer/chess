import pygame, random
import re
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King, Player
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
#start_fen = "rn2k1r1/ppp1pp1p/3p2p1/5bn1/P7/2N2B2/1PPPPP2/2BNK1RR"

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

for i, field in enumerate(bo):
    co, ty = fen_code(start_fen[i])
    if ty is not None:
        piece = set_up_piece(co, bo[field][0], ty)
        all_sprites_list.add(piece)

















#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()
score = 0
pl = Player()
all_sprites_list.add(pl)


#Drawing on Screen
screen.fill(GREEN)



sometimes = -1

while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                 carryOn=False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                blocks_hit_list = pygame.sprite.spritecollide(pl, all_sprites_list, False)
                pl.carry_pieces_list = blocks_hit_list

            elif event.type == pygame.MOUSEBUTTONUP:
                pl.carry_pieces_list = []




            sometimes += 1
            if sometimes % 5 == 0:
                #Draw The Board
                for y in range(8):
                    y_loc = y * 100
                    for i in range(8):
                        x_loc = i*100
                        if i % 2 == 0 and y % 2 == 1 or i % 2 == 1 and y % 2 == 0:
                            pygame.draw.rect(screen, DARK, pygame.Rect(x_loc,y_loc, x_loc+100,y_loc+100))

                        else:
                            pygame.draw.rect(screen, LIGHT, pygame.Rect(x_loc,y_loc, x_loc+100,y_loc+100))






                #Game Logic
                all_sprites_list.update()

            #Now let's draw all the sprites in one go.
            all_sprites_list.draw(screen)

            #Refresh Screen
            pygame.display.flip()

            #Number of frames per secong e.g. 60
            clock.tick(100)

pygame.quit()
