from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King, Player
from check import Attacked_fields
import re


def loc(str):
    """
    translates string containing name of field into coordinates
    :param str: string of length two, containing char and number ("A1")
    :return:
    x and y coordinates each ranging from 0 - 700 in steps of 100.
    H1 is 0,0, A8 is 700,700
    """
    assert len(str) == 2
    cha = list(str)[0]
    num = list(str)[1]
    return ((ord(cha) - 65)) * 100, 800 - int(num) * 100


bo = {}
ob = {}
check = {}
intercept_bo = {}
for x in range(1, 9):
    for y in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        bo[f"{y}{x}"] = [(loc(y + str(x))), None]
        check[f"{y}{x}"] = 0
        ob[(loc(y + str(x)))] = f"{y}{x}"
        intercept_bo[f"{y}{x}"] = None

all_sprites_list = None


def recreate_checkdict():
    at = Attacked_fields(bo, ob)
    # find all attacked fields for attacker
    global check
    check = at.get_dict_of_fields()


def go_home(piece):
    """
    Return piece to position it had prior to move
    :param piece:
    :return:
    """
    piece.rect.x = bo[piece.field][0][0]
    piece.rect.y = bo[piece.field][0][1]
    return False


def legal(mv, piece, piecex, piecey, old_occupant):
    """
    checks if move is according to the allowed move patterns for each piece (isthisallowed)
    checks if no pieces are on the way to the new field (noroadbloacks)
    checks if a given check is being countered (escape_check)
    :param mv: move class
    :param piece: Chess piece that is moving (Class from chess-pieces)
    :param piecex: x coordinate of new field
    :param piecey: y coordinate of new field
    :param old_occupant: piece or None, occupying the new field
    :return:
    """
    # check if move is legal
    if mv.isthisallowed():
        if mv.noroadblocks():
            not_causes_check_bool, causes_check_old_occupant = not_causes_check(
                piece, mv
            )
            if not_causes_check_bool:
                old_occupant = causes_check_old_occupant
                mv.old_occupant = old_occupant
                escape_bool, escape_old_occupant = escape_check(piece, mv)

                if escape_bool:
                    piece.rect.x = piecex
                    piece.rect.y = piecey
                    if escape_old_occupant:
                        old_occupant = escape_old_occupant

                    if old_occupant != None:  # check if someone is there
                        if piece.color != old_occupant.color:
                            old_occupant.kill()
                            return update(piece, piecex, piecey, False)
                        else:
                            return go_home(piece)
                    else:
                        return update(piece, piecex, piecey, False)

        return go_home(piece)


def find_king(color: str) -> King:
    """
    finds the kind in all
    :param ret: bool, true if the king piece shall be returned to calling function (makes code reusable)
    :return:
    """
    king = ''
    vals = list(bo.values())
    for k, j in vals:
        if j:
            if j.name() == 'King':
                if j.color == color:
                    king = j
    return king


# Set up pieces
def set_up_piece(color, coordinate_tuple, kind, field):
    piece = kind(color, field)
    piece.rect.x = coordinate_tuple[0]
    piece.rect.y = coordinate_tuple[1]
    return piece


def update(piece, piecex, piecey, intercept=False):
    """
    Update dictionary with positions
    :param piece:
    :param piecex:
    :param piecey:
    :param intercept: if the updated dict is a hypothetical dict not real board
    :return:
    """
    if piece.name() == 'Pawn' and (
        (piece.color == 'white' and piecey == 0)
        or (piece.color == 'black' and piecey == 700)
    ):
        field = piece.field
        piece.kill()
        piece = set_up_piece(piece.color, (piecex, piecey), Queen, field)
        all_sprites_list.add(piece)

    if intercept:
        intercept_bo = {key: value for key, value in bo.items()}
        intercept_bo[ob[piecex, piecey]][1] = piece
        intercept_bo[piece.field][1] = None
        piece.field = ob[piecex, piecey]
    else:
        bo[ob[piecex, piecey]][1] = piece
        bo[piece.field][1] = None
        piece.field = ob[piecex, piecey]
        return True


def hypothetical_move_check(piece, move):
    """
    Check if at the end of move there is still danger to the king.
    The return of the former occupant piece is necessary because the hypothetical function potentially kills off a piece
    in the new field.
    :param piece:
    :param move:
    :return:
    bool : True if after move there is no danger to king.
    old_occupant : chess_piece.object or None
    """

    king = find_king(piece.color)

    # maybe king moved. should suffice because king cannot move to a field that is threatened.
    if piece == king:
        return True, move.old_occupant

    col, x, y, ty, fd = None, None, None, None, None
    origin = piece.field
    if move.old_occupant:
        col, x, y, ty, fd = (
            move.old_occupant.color,
            bo[move.old_occupant.field][0][0],
            bo[move.old_occupant.field][0][1],
            move.old_occupant.return_class(),
            move.old_occupant.field,
        )
        move.old_occupant.kill()

    update(piece, move.new_field[0], move.new_field[1], False)
    at = Attacked_fields(bo, ob)
    global check
    check = at.get_dict_of_fields()

    if (king.color == 'black' and check[king.field] not in [-1, 1]) or (
        king.color == 'white' and check[king.field] not in [1, 2]
    ):
        update(piece, bo[origin][0][0], bo[origin][0][1], False)
        if move.old_occupant:
            old_occupant = set_up_piece(col, (x, y), ty, fd)
            all_sprites_list.add(old_occupant)
            return True, old_occupant
        return True, None

    update(piece, bo[origin][0][0], bo[origin][0][1], False)
    if move.old_occupant:
        old_occupant = set_up_piece(col, (x, y), ty, fd)
        all_sprites_list.add(old_occupant)
    return False, None


def not_causes_check(piece, move):
    """
    If the move would cause the king to be in check
    :param piece:
    :param move:
    :return:
    """
    allowed, occupant = hypothetical_move_check(piece, move)
    return allowed, occupant


def escape_check(piece, move):
    """
    in this move the King needs to leave check
    :param piece:
    :param move:
    :return:
    bool : True if king leaves check with the move
    old_occupant : chess_piece.object or None
    """

    if not check_given:
        return True, None

    return hypothetical_move_check(piece, move)

    print('deal with piece that stepped in between')
    print('deal with piece that takes other piece')
    return False
    # at = Attacked_fields(utils.bo, utils.ob, utils.check)
    # if self.old_occupant:
    #     utils.check = at.get_dict_of_fields(exclude=(self.old_occupant.name(), self.old_occupant.field))
    # else:
    #     utils.check = at.get_dict_of_fields()
    # if not ch.king_in_check(self.king):
    #     return True
    # return False


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
