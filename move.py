import math

class Move():
    def __init__(self, old_field, new_field, piece, old_inhabitant, bo, ob, check_dict=None):
        self.old_field = old_field
        self.new_field = new_field
        self.piece = piece
        self.move = None
        self.diff = tuple(map(lambda i,j: i - j, self.old_field, self.new_field))
        self.dist = round(math.hypot(self.diff[0], self.diff[1]), 2)
        self.old_inhabitant = old_inhabitant
        self.bo = bo
        self.ob = ob
        self.check_dict = check_dict


    def update_check_dict(self, up_dict):
        self.check_dict = up_dict

    def get_bo(self):
        return self.bo

    def noroadblocks(self):
        if self.piece.name() not in ['Pawn', 'Bishop', 'Rook', 'Queen']:
            return True
        # diagonal = True
        # if round(self.dist % 100, 2) == 0:
        #     diagonal = False
        ontheway = self.get_fields_on_the_way(self.ob[self.old_field], self.ob[self.new_field])
        for block in ontheway:
            if self.bo[block][1] != None:
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
        if not self.old_inhabitant:
            # move one or two fields with pawn
            self.move = [(0, 100)]
            if self.old_field[1] == 100 and self.piece.color == 'black' or self.old_field[1] == 600 and self.piece.color == 'white':
                self.move = [self.move[0], (0, 200)]
            if self.piece.color == 'white':
                self.move = [tuple([-1*i for i in j]) for j in self.move]# change sign
            for mo in self.move:
                if self.add_two_tuples(self.old_field, mo) == self.new_field:
                    return True

        # move pawn diagonally
        if self.dist == 141.42:
            if self.piece.color == 'white' and self.diff[1] > 0 and self.old_inhabitant:
                return True
            if self.piece.color == 'black' and self.diff[1] < 0 and self.old_inhabitant:
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
            if self.piece.color == 'black' and not self.check_dict[self.ob[self.new_field]] in [-1, 1]:
                return True
            if self.piece.color == 'white' and not self.check_dict[self.ob[self.new_field]] in [1, 2]:
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



