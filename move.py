import math
import utils


class Move:
    def __init__(
        self, old_field, new_field, piece, old_occupant, game=None):
        self.old_field = old_field
        self.new_field = new_field
        self.piece = piece
        self.move = None
        self.diff = tuple(map(lambda i, j: i - j, self.new_field, self.old_field))
        self.dist = round(math.hypot(self.diff[0], self.diff[1]), 2)
        self.old_occupant = old_occupant
        self.game = game


    def noroadblocks(self):
        if self.piece.name() not in ['Pawn', 'Bishop', 'Rook', 'Queen']:
            return True
        # diagonal = True
        # if round(self.dist % 100, 2) == 0:
        #     diagonal = False
        ontheway = self.get_fields_on_the_way(
            self.game.board_code[self.old_field], self.game.board_code[self.new_field]
        )
        for block in ontheway:
            if self.game.board[block][1] != None:
                return False
        return True

    def isthisallowed(self):
        if self.old_field == self.new_field:
            return False
        if self.piece.name() == 'Pawn':
            return self.pawn()
        if self.piece.name() == 'Knight':
            return self.knight()
        if self.piece.name() == 'Bishop':
            return self.bishop()
        if self.piece.name() == 'Rook':
            return self.rook()
        if self.piece.name() == 'Queen':
            return self.queen()
        if self.piece.name() == 'King':
            return self.king()

    def pawn(self):
        if not self.old_occupant:
            # move one or two fields with pawn
            self.move = [(0, 100)]
            if (
                self.old_field[1] == 100
                and self.piece.color == 'black'
                or self.old_field[1] == 600
                and self.piece.color == 'white'
            ):
                self.move = [self.move[0], (0, 200)]
            if self.piece.color == 'white':
                self.move = [
                    tuple([-1 * i for i in j]) for j in self.move
                ]  # change sign
            for mo in self.move:
                if self.add_two_tuples(self.old_field, mo) == self.new_field:
                    if self.dist == 200:
                        self.piece.enpassant = True
                    return True

        # move pawn diagonally
        if self.dist == 141.42:
            #enpassant
            en_pawn_field, en_pawn = self.find_enpassanting_pawn()
            if en_pawn_field is not None:
                en_pawn_diff = tuple(map(lambda i, j: i - j, en_pawn_field, self.old_field))
                if round(math.hypot(en_pawn_diff[0], en_pawn_diff[1]), 2) == 100:
                    if (self.piece.color == 'white' and self.diff[1] < 0 or self.piece.color == 'black' and self.diff[1] > 0) \
                            and self.old_field[1] == en_pawn_field[1]: # pos1 represents movement in x-axis
                        en_pawn.kill()
                        self.game.board[en_pawn.field][1] = None
                        return True
            if self.piece.color == 'white' and self.diff[1] < 0 and self.old_occupant:
                return True
            if self.piece.color == 'black' and self.diff[1] > 0 and self.old_occupant:
                return True





        return False

    def knight(self):
        # knight always hops the same distance..
        if self.dist == 223.61:
            return True
        return False

    def bishop(self):
        if abs(self.diff[0]) == abs(self.diff[1]):
            return True
        return False

    def rook(self):
        if self.diff[0] == 0 or self.diff[1] == 0:
            # if rook moves then castling is not allowed anymore
            self.piece.castle = False
            return True
        return False

    def queen(self):
        if self.bishop() or self.rook():
            return True
        return False

    def king(self):
        """
        king may move one field and then only to fields where the check_dict says no attacker is pointing at.
        :return:
        """
        if self.dist == 141.42 or self.dist == 100:
            if self.piece.color == 'black' and not self.game.board_check[
                self.game.board_code[self.new_field]
            ] in [-1, 1]:
                self.piece.castle = False  # no more castling
                return True
            if self.piece.color == 'white' and not self.game.board_check[
                self.game.board_code[self.new_field]
            ] in [1, 2]:
                self.piece.castle = False
                return True

        # castling
        elif (
            self.game.board_code[self.old_field][1] == self.game.board_code[self.new_field][1]
        ):  # horizontal movement


            def all_clear(old, new, color):
                """Checks if one of the 3 fields the kings moves on for castling is under threat"""
                mid = (int((old[0] + new[0]) / 2), old[1])
                for field in [old, mid, new]:
                    field_code = self.game.board_code[field]
                    if color == 'black' and self.game.board_check[field_code] in [-1, 1]:
                        return False
                    if color == 'white' and self.game.board_check[field_code] in [1, 2]:
                        return False
                return True

            # kingside castle
            if (
                self.dist == 200
                and (ord(self.game.board_code[self.old_field][0]) < ord(self.game.board_code[self.new_field][0]))
                and all_clear(self.old_field, self.new_field, self.piece.color)
                and not self.old_occupant
            ):
                if self.rook_ready_to_castle():
                    return True

            # queenside castle
            elif (
                self.dist == 200
                and (ord(self.game.board_code[self.old_field][0]) > ord(self.game.board_code[self.new_field][0]))
                and all_clear(self.old_field, self.new_field, self.piece.color)
                and not self.old_occupant
            ):
                if self.rook_ready_to_castle(queenside=True):
                    return True
        return False

    def rook_ready_to_castle(self, queenside=False):
        """
        checks if there is a rook available to castle.
        :param queenside:
        :return:
        """
        if not queenside:
            rook_homefield = self.game.board_code[self.add_two_tuples(self.new_field, (100, 0))]
            rook_newfield = self.add_two_tuples(self.new_field, (-100, 0))
        else:
            rook_homefield = self.game.board_code[self.add_two_tuples(self.new_field, self.diff)]
            rook_newfield = self.add_two_tuples(self.new_field, (100, 0))

        if self.game.board[rook_homefield] != None:
            if self.game.board[rook_homefield][1].name() == 'Rook':
                if self.game.board[rook_homefield][1].castle == True:
                    self.game.board[rook_homefield][1].kill()
                    self.game.board[rook_homefield][1] = None
                    import chess_pieces

                    new_rook = self.game.set_up_piece(
                        color=self.piece.color,
                        coordinate_tuple=rook_newfield,
                        kind=chess_pieces.Rook,
                        field=self.game.board_code[rook_newfield],
                    )
                    self.game.board[self.game.board_code[rook_newfield]][1] = new_rook
                    utils.all_sprites_list.add(new_rook)
                    return True
        return False

    ########### helper functions

    def add_two_tuples(self, one, two):
        return tuple(map(lambda i, j: i + j, one, two))

    def get_fields_on_the_way(self, start, end):
        """
        Finds fields between a start field and an end field (for movement of bishops, rooks and queens)
        :param start: str, field where piece started (e.g. 'F4')
        :param end: str, field where piece wants to move to
        :return: list, fields between start and end field
        """
        ch1 = start[0]
        ch2 = end[0]
        nu1 = start[1]
        nu2 = end[1]
        if ord(ch1) > ord(ch2):
            let = [chr(i) for i in list(range(ord(ch1), ord(ch2), -1))[1:]]
        else:
            let = [chr(i) for i in list(range(ord(ch1), ord(ch2)))[1:]]
        if int(nu1) > int(nu2):
            num = [str(x) for x in list(range(int(nu1), int(nu2), -1))[1:]]
        else:
            num = [str(x) for x in list(range(int(nu1), int(nu2)))[1:]]

        # if movement is rook-move
        if len(let) == 0 and len(num) > 0:
            ret = [ch1 + num[i] for i in range(len(num))]
        elif len(let) > 0 and len(num) == 0:
            ret = [let[i] + nu1 for i in range(len(let))]
        else:
            ret = [let[i] + num[i] for i in range(len(num))]

        return ret

    def find_enpassanting_pawn(self):
        """If it exists it returns the one Pawn that can be taken enpassant"""
        for k in self.game.board:
            if self.game.board[k][1] != None:
                if self.game.board[k][1].name() == 'Pawn':
                    if self.game.board[k][1].enpassant == True:
                        return self.game.board[k][0], self.game.board[k][1]
        return None, None
