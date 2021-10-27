import numpy as np

class Attacked_fields():
    def __init__(self, bo, ob):
        self.attackers = [bo[b][1] for b in bo if bo[b][1] != None]
        self.bo = bo
        self.ob = ob
        self.piece = None

    def create_dict(self):
        self.di = {}
        for x in range(1,9):
            for y in ['A','B','C','D','E','F','G','H']:
                self.di[f"{y}{x}"] = 0

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
        self.white_attackfields = set([item for sublist in self.white_attackfields for item in sublist])
        self.black_attackfields = set([item for sublist in self.black_attackfields for item in sublist])

    def nanify_dict(self):
        """
        adapts dict to have nan values. Now each field can be checked if smaller than 2 (True if attacked by white or both)
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
        ch, nu = ord(self.piece.field[0]), int(self.piece.field[-1])
        nu -=1
        if self.piece.color == 'white':
            nu += 2
        # join char with number for adjacent letters as long as numbers and letters within A-H and 0-8
        return [chr(k) + str(nu) for k in [j for j in [i + ch for i in range(-1,2,2)] if j > 64 and j < 73] if nu < 9 and nu > -1]

    def rook_find_attacked_fields(self):
        """
        start at field of piece and iterate in each of the four directions until any piece is in the way.
        :return:
        """
        ch, nu = ord(self.piece.field[0]), int(self.piece.field[-1])
        left, right, up, down = [], [], [], []
        for k in [chr(j)+str(nu) for j in [i + ch for i in range(1,73-ch)] if j > 64 and j < 73]:
            # king exception because an attack-range is not stopped by a king - otherwise he could retreat along the same line
            if self.bo[k][1] == None or (self.bo[k][1].name() == 'King' and self.piece.color != self.bo[k][1].color):
                right.append(k)
            else:
                break
        for l in [chr(j)+str(nu) for j in [ch-i for i in range(1, ch-64)] if j > 64 and j < 73]:
            if self.bo[l][1] == None or (self.bo[l][1].name() == 'King' and self.piece.color != self.bo[l][1].color):
                left.append(l)
            else:
                break
        for m in [chr(ch)+str(j) for j in [i for i in range(nu-1, 0, -1)]]:
            if self.bo[m][1] == None or (self.bo[m][1].name() == 'King' and self.piece.color != self.bo[m][1].color):
                down.append(m)
            else:
                break
        for n in [chr(ch)+str(j) for j in [i for i in range(nu+1, 9)]]:
            if self.bo[n][1] == None or (self.bo[n][1].name() == 'King' and self.piece.color != self.bo[n][1].color):
                up.append(n)
            else:
                break
        return left+right+up+down

    def bishop_find_attacked_fields(self):
        """
        start at field of piece and iterate in each of the four directions until any piece is in the way.
        :return:
        """
        ch, nu = ord(self.piece.field[0]), int(self.piece.field[-1])
        upleft, upright, downleft, downright = [], [], [], []
        for k in [chr(j + ch) + str(i+nu+1) for i, j in enumerate(range(1,73-ch)) if (i+nu+1) < 9]:
            if self.bo[k][1] == None or (self.bo[k][1].name() == 'King' and self.piece.color != self.bo[k][1].color):
                upright.append(k)
            else:
                break
        for l in [chr(ch-j)+str(nu+i+1) for i, j in enumerate(range(1, ch-64)) if (nu+i+1) < 9]:
            if self.bo[l][1] == None or (self.bo[l][1].name() == 'King' and self.piece.color != self.bo[l][1].color):
                upleft.append(l)
            else:
                break
        for m in [chr(j + ch) + str(nu-1-i) for i, j in enumerate(range(1,73-ch)) if nu-1-i > 0]:
            if self.bo[m][1] == None or (self.bo[m][1].name() == 'King' and self.piece.color != self.bo[m][1].color):
                downright.append(m)
            else:
                break
        for n in [chr(ch-j)+str(nu-i-1) for i, j in enumerate(range(1, ch-64)) if nu-1-i > 0]:
            if self.bo[n][1] == None or (self.bo[n][1].name() == 'King' and self.piece.color != self.bo[n][1].color):
                upright.append(n)
            else:
                break
        return upleft+upright+downleft+downright

    def knight_find_attacked_fields(self):
        ch, nu = ord(self.piece.field[0]), int(self.piece.field[-1])
        hor = []
        for let in [chr(j) for j in [i + ch for i in range(-2,3,4)] if j > 64 and j < 73]:
            if (nu - 1) > 0:
                hor.append(let+str(nu-1))
            if (nu + 1) < 9:
                hor.append(let+str(nu+1))
        ver = []
        for let in [chr(j) for j in [i + ch for i in range(-1,2,2)] if j > 64 and j < 73]:
            if (nu - 2) > 0:
                ver.append(let+str(nu-2))
            if (nu + 2) < 9:
                ver.append(let+str(nu+2))
        return hor + ver

    def king_find_attacked_fields(self):
        ch, nu = ord(self.piece.field[0]), int(self.piece.field[-1])
        hor = [chr(j)+str(nu) for j in [i + ch for i in range(-1,2,2)] if j > 64 and j < 73]
        ver = [chr(ch) + str(j) for j in [i + nu for i in range(-1,2,2)] if j < 9 and j > 0]
        diag = []
        for num in ver:
            for let in hor:
             diag.append(let[0] + (num[1]))
        return hor + ver + diag







