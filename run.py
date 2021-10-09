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
font = pygame.font.Font(pygame.font.get_default_font(), 56)

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
ob = {}
for y in ['A','B','C','D','E','F','G','H']:
    for x in range(1,9):
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

for i, field in enumerate(bo):
    co, ty = fen_code(start_fen[i])
    if ty is not None:
        piece = set_up_piece(co, bo[field][0], ty)
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

import time
while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                 carryOn=False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                blocks_hit_list = pygame.sprite.spritecollide(pl, all_sprites_list, False)
                blocks_hit_list.pop(-1)
                pl.carry_pieces_list = blocks_hit_list



            elif event.type == pygame.MOUSEBUTTONUP:
                if len(pl.carry_pieces_list) > 0:
                    piece = pl.carry_pieces_list[0]
                    piecex = round(piece.rect.x, -2)
                    piecey = round(piece.rect.y, -2)
                    piece.rect.x = piecex
                    piece.rect.y = piecey
                    old_inhabitant = bo[ob[piecex, piecey]][1]
                    if old_inhabitant != None:# check if someone is there
                        if piece.color != old_inhabitant.color:
                            old_inhabitant.kill()
                            # Check if killed piece was the King
                            if old_inhabitant.__class__.__name__ == 'King':

                                game_over=True

                            bo[ob[piecex, piecey]][1] = piece
                    else:
                        bo[ob[piecex, piecey]][1] = piece
                    pl.carry_pieces_list = []

            for i, field in enumerate(fields):
                if (i + int(i / 8)) % 2 == 0:
                    pygame.draw.rect(screen, DARK, pygame.Rect(field[0],field[1], 100,100))
                else:
                    pygame.draw.rect(screen, LIGHT, pygame.Rect(field[0],field[1], 100,100))

            all_sprites_list.update()




                #Game Logic


            #Now let's draw all the sprites in one go.
            all_sprites_list.draw(screen)

            #Refresh Screen
            pygame.display.flip()
            if game_over:
                text_surface = font.render(f'{piece.color} wins!', True, (0, 0, 0))
                screen.blit(text_surface, dest=(270,350))
                pygame.display.flip()
                import time
                time.sleep(5)
                pygame.quit()
            #Number of frames per secong e.g. 60
            clock.tick(80)

pygame.quit()
