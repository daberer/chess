import math

class Move():
    def __init__(self, old_field, new_field):
        self.old_field = old_field
        self.new_field = new_field
        self.move = None



    def isthisallowed(self, piece):
        self.piece = piece
        if self.piece.__class__.__name__ == 'Pawn':
            return self.pawn()
        if self.piece.__class__.__name__ == 'Knight':
            return self.knight()


    def pawn(self):
        if self.piece.color == 'black':
            self.move = (0, 100)
        else:
            self.move = (0, -100)
        if tuple(map(lambda i, j: i + j, self.old_field, self.move)) == self.new_field:
            return True
        else:
            return False

    def knight(self):
        # knight always hops the same distance..
        diff = tuple(map(lambda i,j: i - j, self.old_field, self.new_field))
        if round(math.hypot(diff[0], diff[1]),2) == 223.61:
            return True
        else:
            return False



