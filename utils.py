from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King, Player
from check import Attacked_fields
import re

all_sprites_list = None

# translate field into x,y
def fen_code(sign):
    """
    translates Forsyth-Edward-Notation into the corresponding chess piece
    :param sign: str of fen code
    :return: color and type of piece
    """
    assert type(sign) == str
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


def fen_insert(st, length, ind):
    """
    inserts up to eight "o" characters into an input string instead of an integer 1-8 at a given index.
    :param st: string, that is being added to
    :param length: int, number of times "o" is being added to st
    :param ind: int, index where int is located in st.
    :return:
    """
    return st[:ind] + length * 'o' + st[ind + 1 :]


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


# TODO: fix fen set up (Queen and King are set conversly) or are they correct and the fen code was wrong?
start_fen = 'rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR'
# start_fen = "rn2k1r1/ppp1pp1p/3p2p1/5bn1/P7/2N2B2/1PPPPP2/2BNK1RR"
check_given = False
start_fen = start_fen.replace('/', '')
start_fen = extend_fen(start_fen)
start_fen = start_fen[::-1]
