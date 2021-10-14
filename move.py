import math

class Move():
    def __init__(self, old_field, new_field, piece, old_inhabitant):
        self.old_field = old_field
        self.new_field = new_field
        self.piece = piece
        self.move = None
        self.diff = tuple(map(lambda i,j: i - j, self.old_field, self.new_field))
        self.old_inhabitant = old_inhabitant


    # def isanyonehome(self, old_inhabitant):
    #     if old_inhabitant != None:# check if someone is there
    #         if self.piece.color != old_inhabitant.color:
    #             old_inhabitant.kill()
    #             # Check if killed piece was the King
    #             if old_inhabitant.name() == 'King':
    #                 return True

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
                if tuple(map(lambda i, j: i + j, self.old_field, mo)) == self.new_field:
                    return True

        # move pawn diagonally
        dist = round(math.hypot(self.diff[0], self.diff[1]), 2)
        if dist == 141.42:
            if self.piece.color == 'white' and self.diff[1] > 0 and self.old_inhabitant:
                return True
            if self.piece.color == 'black' and self.diff[1] < 0 and self.old_inhabitant:
                return True
        return False

    def knight(self):
        # knight always hops the same distance..
        if round(math.hypot(self.diff[0], self.diff[1]),2) == 223.61:
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
        dist = round(math.hypot(self.diff[0], self.diff[1]), 2)
        if  dist == 141.42 or dist == 100:
            return True
        return False






