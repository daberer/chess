from check import Attacked_fields
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King
import re


class Sprites:
    """Holds list with sprites"""

    all_sprites_list = None


class Game:
    """
    Creates a game object to have a game structure
    """

    def __init__(self, turn=True, board=None, fen=None, ob=None):
        self.turn = True
        self.move_count = 0
        self.board = board
        self.board_code = ob
        self.board_check = None
        self.board_intercept = None
        self.fen = Fen()
        self.check_given = False
        self.white_gameover = False
        self.black_gameover = False
        self.white_castle = False
        self.black_castle = False
        self.active_piece = None
        self.current_fen = None
        self.moves = {}

    def next_move(self):
        self.move_count += 1
        self.turn = not self.turn
        # for now use unformatted fen
        #raw_fen = self.fen.get_fen_from_board(self.board)
        #self.current_fen = self.fen.shrink_fen(raw_fen)
        self.current_fen = self.fen.get_fen_from_board(self.board)
        self.moves[self.move_count] = self.current_fen


    def recreate_checkdict(self):
        at = Attacked_fields(self.board, self.board_code)
        self.board_check = at.get_dict_of_fields()

    def activate_piece(self, piece):
        self.active_piece = piece

    def go_home(self, piece=None):
        """
        Return piece to position it had prior to move
        :param piece:
        :return:
        """
        if piece:
            self.active_piece = piece
        self.active_piece.rect.x = self.board[self.active_piece.field][0][0]
        self.active_piece.rect.y = self.board[self.active_piece.field][0][1]
        return False

    def loc(self, str):
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

    def create_boards(self):
        bo = {}
        ob = {}
        check = {}
        intercept_bo = {}
        for x in range(8, 0, -1):
            for y in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                bo[f"{y}{x}"] = [(self.loc(y + str(x))), None]
                check[f"{y}{x}"] = 0
                ob[(self.loc(y + str(x)))] = f"{y}{x}"
                intercept_bo[f"{y}{x}"] = None
        self.board = bo
        self.board_code = ob
        self.board_check = check
        self.board_intercept = intercept_bo

    def fill_board(self, custom_pos=None):
        pos = self.fen.start_fen
        if custom_pos:
            pos = custom_pos
        for i, field in enumerate(self.board):
            co, ty = self.fen.fen_code(pos[i])
            if ty is not None:
                piece = self.set_up_piece(co, self.board[field][0], ty, field)
                self.board[field][1] = piece
                Sprites.all_sprites_list.add(piece)

    def legal(self, mv, piece, piecex, piecey, old_occupant):
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
                (
                    not_causes_check_bool,
                    causes_check_old_occupant,
                ) = self.not_causes_check(piece, mv)
                if not_causes_check_bool:
                    old_occupant = causes_check_old_occupant
                    mv.old_occupant = old_occupant
                    escape_bool, escape_old_occupant = self.escape_check(piece, mv)

                    if escape_bool:
                        piece.rect.x = piecex
                        piece.rect.y = piecey
                        if escape_old_occupant:
                            old_occupant = escape_old_occupant

                        if old_occupant != None:  # check if someone is there
                            if piece.color != old_occupant.color:
                                old_occupant.kill()
                                return self.update(piece, piecex, piecey, False)
                            else:
                                return self.go_home()
                        else:
                            return self.update(piece, piecex, piecey, False)

            return self.go_home()

    def find_king(self, color: str):
        """
        finds the kind in all
        :param ret: bool, true if the king piece shall be returned to calling function (makes code reusable)
        :return:
        """
        king = ''
        vals = list(self.board.values())
        for k, j in vals:
            if j:
                if j.name() == 'King':
                    if j.color == color:
                        king = j
        return king

    def not_causes_check(self, piece, move):
        """
        If the move would cause the king to be in check
        :param piece:
        :param move:
        :return:
        """
        allowed, occupant = self.hypothetical_move_check(piece, move)
        return allowed, occupant

    def escape_check(self, piece, move):
        """
        in this move the King needs to leave check
        :param piece:
        :param move:
        :return:
        bool : True if king leaves check with the move
        old_occupant : chess_piece.object or None
        """
        if not self.check_given:
            return True, None

        return self.hypothetical_move_check(piece, move)

    def hypothetical_move_check(self, piece, move):
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

        king = self.find_king(piece.color)

        # maybe king moved. should suffice because king cannot move to a field that is threatened.
        if piece == king:
            return True, move.old_occupant

        col, x, y, ty, fd = None, None, None, None, None
        origin = piece.field
        if move.old_occupant:
            col, x, y, ty, fd = (
                move.old_occupant.color,
                self.board[move.old_occupant.field][0][0],
                self.board[move.old_occupant.field][0][1],
                move.old_occupant.return_class(),
                move.old_occupant.field,
            )
            move.old_occupant.kill()

        queen = self.update(
            self.active_piece, self.active_piece.rect.x, self.active_piece.rect.y, True
        )

        self.recreate_checkdict()
        if (king.color == 'black' and self.board_check[king.field] not in [-1, 1]) or (
            king.color == 'white' and self.board_check[king.field] not in [1, 2]
        ):
            if queen:
                queen.kill()
                self.board[queen.field][1] = None

            self.update(
                piece, self.board[origin][0][0], self.board[origin][0][1], False
            )
            if move.old_occupant:
                old_occupant = self.set_up_piece(col, (x, y), ty, fd)
                Sprites.all_sprites_list.add(old_occupant)
                return True, old_occupant
            return True, None

        self.update(piece, self.board[origin][0][0], self.board[origin][0][1], False)
        if move.old_occupant:
            old_occupant = self.set_up_piece(col, (x, y), ty, fd)
            Sprites.all_sprites_list.add(old_occupant)
        return False, None

    def set_up_piece(self, color, coordinate_tuple, kind, field):
        piece = kind(color, field)
        piece.rect.x = coordinate_tuple[0]
        piece.rect.y = coordinate_tuple[1]
        return piece

    def update(self, piece, piecex, piecey, intercept=False):
        """
        Update dictionary with positions
        :param piece:
        :param piecex:
        :param piecey:
        :param intercept: if the updated dict is a hypothetical dict not real board
        :return:
        """
        queen_created = False  # if a queen is created and hypothetical intercept move is considered, queen needs to be
        # removed later
        if piece.name() == 'Pawn' and (
            (piece.color == 'white' and piecey == 0)
            or (piece.color == 'black' and piecey == 700)
        ):
            field = piece.field
            piece.kill()
            self.board[field][1] = None  # Not just kill but erase from self.board
            piece = self.set_up_piece(piece.color, (piecex, piecey), Queen, field)
            queen_created = True
            Sprites.all_sprites_list.add(piece)

        if intercept:
            self.board_intercept = {key: value for key, value in self.board.items()}
            self.board_intercept[self.board_code[piecex, piecey]][1] = piece
            # TODO: Bug - influences self.board
            self.board_intercept[piece.field][1] = None
            piece.field = self.board_code[piecex, piecey]
            if queen_created:
                return piece

        else:
            self.board[self.board_code[piecex, piecey]][1] = piece
            self.board[piece.field][1] = None
            piece.field = self.board_code[piecex, piecey]
            return True

        return False

    def enpassant_expired(self, col):
        """Chance for enpassanting Pawn is over"""
        for k in self.board:
            if self.board[k][1] != None:
                if self.board[k][1].name() == 'Pawn' and self.board[k][1].color == col:
                    self.board[k][1].enpassant = False


class Fen:
    """Class for Forsyth-Edwards-Notation"""

    def __init__(self):
        start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        start_fen = start_fen.split(' ')[0]
        start_fen = start_fen.replace('/', '')
        self.start_fen = self.extend_fen(start_fen)

    # translate field into x,y
    def fen_code(self, sign, color=None):
        """
        translates Forsyth-Edward-Notation into the corresponding chess piece and vice versa
        :param sign: str of fen code, or piece class
        :return: color and type of piece
        """
        fendict = {'p': Pawn, 'n': Knight, 'b': Bishop, 'r':  Rook, 'q': Queen,  'k': King, 'o': None}
        key_list = list(fendict.keys())
        val_list = list(fendict.values())
        col = None
        if type(sign) == str:
            if sign.isupper():
                col = 'white'
            else:
                col = 'black'
            sign = sign.lower()
            ret = fendict[sign]
        else:
            position = val_list.index(sign)
            ret = key_list[position]
            if color:
                col = color
                if col == 'white':
                    ret = ret.upper()
        return col, ret

    def fen_insert(self, st, length, ind):
        """
        inserts up to eight "o" characters into an input string instead of an integer 1-8 at a given index.
        :param st: string, that is being added to
        :param length: int, number of times "o" is being added to st
        :param ind: int, index where int is located in st.
        :return:
        """
        return st[:ind] + length * 'o' + st[ind + 1 :]

    def has_numbers(self, inputString):
        """
        Checks input string for numbers.
        :param inputString:
        :return: True if inputString has number.
        """
        return bool(re.search(r'\d', inputString))

    def extend_fen(self, fen):
        """
        replace the number for number of empty fields in the fen notation with 'o' times the number
        rn3k becomes rnoook
        :param fen:
        :return:
        """
        ext_fen = (fen + '.')[:-1]
        while self.has_numbers(ext_fen):
            ind = None
            match = re.search(r"\d", ext_fen)
            if match:
                ind = match.start()
                ext_fen = self.fen_insert(ext_fen, int(ext_fen[ind]), ind)
        return ext_fen

    def shrink_fen(self, fen):
        """replace consecutive 'o' signs with the length of this pattern. rnoook becomes rn3k."""
        fen = '/'.join(fen[i:i+8] for i in range(0, len(fen), 8))
        occurs = re.findall(r'(([o])\2+)', fen)
        for oc in occurs:
            match = re.search(f"{oc[0]}", fen)
            num = str(len(match.re.pattern))
            fen = fen[:match.start()] + num + fen[match.end():]
        # TODO: find neater solution for single 'o's
        while 'o' in fen:
            match = re.search('o', fen)
            fen = fen[:match.start()] + '1' + fen[match.end():]
        return fen

    def get_fen_from_board(self, board):
        fen_string = ''
        for item in board.items():
            if item[1][1]:
                _, add = self.fen_code(item[1][1].__class__, item[1][1].color)
                fen_string += add
            else:
                fen_string += 'o'

        return fen_string

