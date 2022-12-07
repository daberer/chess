import numpy as np


class Attacked_fields:
    def __init__(self, bo, ob):
        self.attackers = [bo[b][1] for b in bo if bo[b][1] != None]
        self.bo = bo
        self.ob = ob
        self.piece = None

    def create_dict(self):
        """
        in pygame first coordinate is x! (see pygame.event.get().pos)
        :return:
        """
        self.di = {}
        for x in range(1, 9):
            for y in range(1, 9):
                self.di[(x,y)] = 0

    def clear_dict(self):
        self.di = dict.fromkeys(self.di, 0)

    def get_dict_of_fields(self, exclude=None):
        self.create_dict()
        self.black_attackfields = []
        self.white_attackfields = []
        for piece in self.attackers:
            if (piece.name(), piece.field) == exclude:
                continue
            self.piece = piece
            if self.piece.color == 'black':
                ret = self.find_fields_for_piece()
                if ret is not None:
                    self.black_attackfields.append(ret)
            if self.piece.color == 'white':
                ret = self.find_fields_for_piece()
                if ret is not None:
                    self.white_attackfields.append(ret)
        self.setify()
        return self.return_dict()

    def find_fields_for_piece(self):
        if self.piece.name() == 'Pawn':
            return self.pawn_find_attacked_fields()
        if self.piece.name() == 'Rook':
            return self.rook_find_attacked_fields()
        if self.piece.name() == 'Bishop':
            return self.bishop_find_attacked_fields()
        if self.piece.name() == 'Knight':
            return self.knight_find_attacked_fields()
        if self.piece.name() == 'Queen':
            return self.bishop_find_attacked_fields() + self.rook_find_attacked_fields()
        if self.piece.name() == 'King':
            return self.king_find_attacked_fields()

    def setify(self):
        self.white_attackfields = set(
            [item for sublist in self.white_attackfields for item in sublist]
        )
        self.black_attackfields = set(
            [item for sublist in self.black_attackfields for item in sublist]
        )

    def nanify_dict(self):
        """
        adapts dict to have nan values. Now each field can be checked if -1 or 1 (True if attacked by white or both)
        or larger than 0 (True if attacked by black or both)
        :param di:
        :return:
        """
        for key, value in self.di.items():
            if value == 0:
                self.di[key] = np.nan

    def return_dict(self):
        for ele in self.white_attackfields:
            self.di[ele] -= 1
        for ele in self.black_attackfields:
            self.di[ele] += 2
        self.nanify_dict()
        return self.di

    def pawn_find_attacked_fields(self):
        x, y = self.piece.field[0], self.piece.field[1]
        y -= 1
        if self.piece.color == 'white':
            y += 2
        return [(k, y) for k in [j for j in [i + x for i in range(-1, 2, 2)] if j > 0 and j < 9] if y > 0 and y < 9]

    def rook_find_attacked_fields(self):
        """
        start at field of piece and iterate in each of the four directions until any piece is in the way.
        :return:
        """
        x, y = self.piece.field[0], self.piece.field[-1]
        left, right, up, down = [], [], [], []
        for k in [(j,y) for j in [i + x for i in range(1, 8)] if j > 1 and j < 9]:
            # king exception because an attack-range is not stopped by a king - otherwise he could retreat along the same line
            if self.bo[k][1] == None or (self.bo[k][1].name() == 'King' and self.piece.color != self.bo[k][1].color):
                right.append(k)
            else:
                right.append(k)
                break
        for l in [(j,y) for j in [i for i in range(x, 1, -1)] if j > 0 and j < 8]:
            if self.bo[l][1] == None or (
                self.bo[l][1].name() == 'King'
                and self.piece.color != self.bo[l][1].color
            ):
                left.append(l)
            else:
                left.append(l)
                break
        for m in [(x,j) for j in [y - i for i in range(1, 9)] if j > 0 and j < 8]:
            if self.bo[m][1] == None or (self.bo[m][1].name() == 'King' and self.piece.color != self.bo[m][1].color):
                down.append(m)
            else:
                down.append(m)
                break
        for n in [(x,j) for j in [i + 1 for i in range(y, 8)] if j > 1 and j < 9]:
            if self.bo[n][1] == None or (self.bo[n][1].name() == 'King' and self.piece.color != self.bo[n][1].color):
                up.append(n)
            else:
                up.append(n)
                break
        return left + right + up + down

    def bishop_find_attacked_fields(self):
        """
        start at field of piece and iterate in each of the four directions until any piece is in the way.
        :return:
        """
        x, y = self.piece.field[0], self.piece.field[1]
        upleft, upright, downleft, downright = [], [], [], []
        for k in [(x + i + 1, j) for i,j in enumerate(range(y + 1, 9)) if x + i +1 < 9]:
            if self.bo[k][1] == None or (
                self.bo[k][1].name() == 'King'
                and self.piece.color != self.bo[k][1].color
            ):
                upright.append(k)
            else:
                upright.append(k)
                break
        for l in [(x - i - 1, j) for i,j in enumerate(range(y + 1, 9)) if x -i -1 > 0]:
            if self.bo[l][1] == None or (
                self.bo[l][1].name() == 'King'
                and self.piece.color != self.bo[l][1].color
            ):
                upleft.append(l)
            else:
                upleft.append(l)
                break
        for m in [(x + i + 1, j - 1) for i, j in enumerate(range(y, 1, -1)) if (i + x + 1) < 9]:
            if self.bo[m][1] == None or (
                self.bo[m][1].name() == 'King'
                and self.piece.color != self.bo[m][1].color
            ):
                downright.append(m)
            else:
                downright.append(m)
                break
        for n in [(x - i - 1, j - 1) for i, j in enumerate(range(y, 1, -1)) if x - i - 1 > 0]:
            if self.bo[n][1] == None or (
                self.bo[n][1].name() == 'King'
                and self.piece.color != self.bo[n][1].color
            ):
                downleft.append(n)
            else:
                downleft.append(n)
                break
        return upleft + upright + downleft + downright

    def knight_find_attacked_fields(self):
        x, y = self.piece.field[0], self.piece.field[1]
        ver = []
        for m in [j for j in [i + y for i in range(-2, 3, 4)] if j > 0 and j < 9]:
            if (x - 1) > 0:
                ver.append(((x - 1), m))
            if (x + 1) < 9:
                ver.append(((x + 1), m))
        hor = []
        for m in [j for j in [i + y for i in range(-1, 2, 2)] if j > 0 and j < 9]:
            if (x - 2) > 0:
                hor.append(((x - 2), m))
            if (x + 2) < 9:
                hor.append(((x + 2), m))
        return ver + hor

    def king_find_attacked_fields(self):
        x, y = self.piece.field[0], self.piece.field[1]
        hor = [(j, y) for j in [i + x for i in range(-1, 2, 2)]if j > 0 and j < 9]
        ver = [(x, j) for j in [i + y for i in range(-1, 2, 2)]
            if j < 9 and j > 0
        ]
        diag = []
        for v in ver:
            for h in hor:
                diag.append((h[0], v[1]))
        return hor + ver + diag
