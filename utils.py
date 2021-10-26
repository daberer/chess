import chess_pieces

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

bo = {}
ob = {}
check = {}
intercept_bo = {}
for x in range(1,9):
    for y in ['A','B','C','D','E','F','G','H']:
        bo[f"{y}{x}"] = [(loc(y + str(x))), None]
        check[f"{y}{x}"] = 0
        ob[(loc(y + str(x)))] = f"{y}{x}"
        intercept_bo[f"{y}{x}"] = None

all_sprites_list = None

check_given = False



def find_king(color):
    """
    finds the kind in all
    :param ret: bool, true if the king piece shall be returned to calling function (makes code reusable)
    :return:
    """
    king = ''
    vals = list(bo.values())
    for k,j in vals:
        if j:
            if j.name() == 'King':
                if j.color != color:
                    king = j
    return king

#Set up pieces
def set_up_piece(color, coordinate_tuple, kind, field):
    piece = kind(color, field)
    piece.rect.x = coordinate_tuple[0]
    piece.rect.y = coordinate_tuple[1]
    return piece

def update(piece, piecex, piecey, intercept=False, Queen=None):
    """
    Update dictionary with positions
    :param piece:
    :param piecex:
    :param piecey:
    :param intercept: if the updated dict is a hypothetical dict not real board
    :return:
    """
    if piece.name() == 'Pawn' and ((piece.color == 'white' and piecey == 0) or (piece.color == 'black' and piecey == 700)):
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

def escape_check(piece, move):
    if not check_given:
        return True

    king = find_king(piece.color)

    # maybe king moved. should suffice because king cannot move to a field that is threatened.
    if piece == king:
        return True

    update(piece, bo[piece.field][0][0], bo[piece.field][0][1], False, chess_pieces.Queen)
    print('deal with piece that stepped in between')
    print('deal with piece that takes other piece')
    return False
    # at = Attacked_fields(utils.bo, utils.ob, utils.check)
    # if self.old_inhabitant:
    #     utils.check = at.get_dict_of_fields(exclude=(self.old_inhabitant.name(), self.old_inhabitant.field))
    # else:
    #     utils.check = at.get_dict_of_fields()
    # if not ch.king_in_check(self.king):
    #     return True
    # return False
