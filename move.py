import math
from procedure import Sprites


class Move:
    def __init__(self, old_field, new_field, piece, old_occupant, game=None):
        self.old_field = old_field
        self.new_field = new_field
        self.piece = piece
        self.move = None
        self.diff = tuple(map(lambda i, j: i - j, self.new_field, self.old_field))
        self.dist = round(math.hypot(self.diff[0], self.diff[1]), 4)
        self.old_occupant = old_occupant
        self.game = game

    def noroadblocks(self):
        if self.piece.name() not in ['Pawn', 'Bishop', 'Rook', 'Queen']:
            return True
        # diagonal = True
        # if round(self.dist % 100, 2) == 0:
        #     diagonal = False
        ontheway = self.get_fields_on_the_way(self.old_field, self.new_field)
        for block in ontheway:
            if self.game.board[block][1] != None:
                return False
        return True

    def isthisallowed(self, no_casualties=False):
        """
        :param no_casualties: for hypothetical moves
        :return:
        """
        if self.old_field == self.new_field:
            return False
        if self.piece.name() == 'Pawn':
            return self.pawn(no_casualties)
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

    def pawn(self, no_casualties):
        if not self.old_occupant:
            # move one or two fields with pawn
            self.move = [(0, 1)]
            if (
                self.old_field[1] == 7
                and self.piece.color == 'black'
                or self.old_field[1] == 2
                and self.piece.color == 'white'
            ):
                self.move = [self.move[0], (0, 2)]
            if self.piece.color == 'black':
                self.move = [tuple([-1 * i for i in j]) for j in self.move]  # change sign
            for mo in self.move:
                if self.add_two_tuples(self.old_field, mo) == self.new_field:
                    if self.dist == 2:
                        self.piece.enpassant = True
                    return True

        # move pawn diagonally
        if self.dist == 1.4142:
            # enpassant
            en_pawn_field, en_pawn = self.find_enpassanting_pawn()
            if en_pawn_field is not None:
                en_pawn_diff = tuple(
                    map(lambda i, j: i - j, en_pawn_field, self.old_field)
                )
                if round(math.hypot(en_pawn_diff[0], en_pawn_diff[1]), 2) == 1:
                    if (
                        self.piece.color == 'white'
                        and self.diff[1] > 0
                        or self.piece.color == 'black'
                        and self.diff[1] < 0
                    ) and self.old_field[1] == en_pawn_field[1]:  # pos1 represents movement in x-axis
                        if not no_casualties:
                            en_pawn.kill()
                            self.game.board[en_pawn.field][1] = None
                        return True
            if self.piece.color == 'white' and self.diff[1] > 0 and self.old_occupant:
                return True
            if self.piece.color == 'black' and self.diff[1] < 0 and self.old_occupant:
                return True

        return False

    def knight(self):
        # knight always hops the same distance..
        if self.dist == 2.2361:
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
        if self.dist == 1.4142 or self.dist == 1:
            if self.piece.color == 'black' and not self.game.board_check[self.new_field] in [-1, 1]:
                self.piece.castle = False  # no more castling
                return True
            if self.piece.color == 'white' and not self.game.board_check[self.new_field] in [1, 2]:
                self.piece.castle = False
                return True

        # castling
        elif (self.old_field[1] == self.new_field[1]):  # horizontal movement

            def all_clear(old, new, color):
                """Checks if one of the 3 fields the kings moves on for castling is under threat"""
                mid = (int((old[0] + new[0]) / 2), old[1])
                for field in [old, mid, new]:
                    if color == 'black' and self.game.board_check[field] in [-1, 1]:
                        return False
                    if color == 'white' and self.game.board_check[field] in [1, 2]:
                        return False
                return True

            # kingside castle
            if (
                self.dist == 2
                and (self.old_field[0] < self.new_field[0])
                and all_clear(self.old_field, self.new_field, self.piece.color)
                and not self.old_occupant
            ):
                if self.rook_ready_to_castle():
                    return True

            # queenside castle
            elif (
                self.dist == 2
                and (self.old_field[0] > self.new_field[0])
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
            rook_homefield = self.add_two_tuples(self.new_field, (1, 0))
            rook_newfield = self.add_two_tuples(self.new_field, (-1, 0))
        else:
            rook_homefield = self.add_two_tuples(self.new_field, self.diff)
            rook_newfield = self.add_two_tuples(self.new_field, (1, 0))

        if self.game.board[rook_homefield][1] != None:
            if self.game.board[rook_homefield][1].name() == 'Rook':
                if self.game.board[rook_homefield][1].castle == True:
                    self.game.board[rook_homefield][1].kill()
                    self.game.board[rook_homefield][1] = None
                    import chess_pieces

                    new_rook = self.game.set_up_piece(
                        color=self.piece.color,
                        coordinate_tuple=self.game.board[rook_newfield][0],
                        kind=chess_pieces.Rook,
                        field=rook_newfield,
                    )
                    self.game.board[rook_newfield][1] = new_rook
                    Sprites.all_sprites_list.add(new_rook)
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
        y1 = start[1]
        y2 = end[1]
        x1 = start[0]
        x2 = end[0]
        if y1 > y2:
            ver = [i for i in list(range(y1, y2, -1))[1:]]
        else:
            ver = [i for i in list(range(y1, y2))[1:]]
        if x1 > x2:
            hor = [x for x in list(range(x1, x2, -1))[1:]]
        else:
            hor = [x for x in list(range(x1, x2))[1:]]

        # if movement is rook-move
        if len(ver) == 0 and len(hor) > 0:
            ret = [(hor[i], y1) for i in range(len(hor))]
        elif len(ver) > 0 and len(hor) == 0:
            ret = [(x1, ver[i]) for i in range(len(ver))]
        else:
            ret = [(hor[i], ver[i]) for i in range(len(hor))]

        return ret

    def find_enpassanting_pawn(self):
        """If it exists it returns the one Pawn that can be taken enpassant"""
        for k in self.game.board:
            if self.game.board[k][1] != None:
                if self.game.board[k][1].name() == 'Pawn':
                    if self.game.board[k][1].enpassant == True:
                        return k, self.game.board[k][1]
        return None, None
