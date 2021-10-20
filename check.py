import numpy as np

class Attacked_fields():
    def __init__(self, attackers, bo, ob, di):
        self.attackers = attackers
        self.di = di
        self.bo = bo
        self.ob = ob
        self.piece = None


    def list_of_fields(self):
        self.black_attackfields = []
        self.white_attackfields = []
        for piece in self.attackers:
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
        if self.piece.name() == 'Queen':
            return self.bishop_find_attacked_fields() + self.rook_find_attacked_fields()



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
            if self.bo[k][1] == None:
                right.append(k)
            else:
                break
        for l in [chr(j)+str(nu) for j in [ch-i for i in range(1, ch-64)] if j > 64 and j < 73]:
            if self.bo[l][1] == None:
                left.append(l)
            else:
                break
        for m in [chr(ch)+str(j) for j in [i for i in range(nu-1, 0, -1)]]:
            if self.bo[m][1] == None:
                down.append(m)
            else:
                break
        for n in [chr(ch)+str(j) for j in [i for i in range(nu+1, 9)]]:
            if self.bo[n][1] == None:
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
        for k in [chr(j + ch) + str(i+nu+1) for i, j in enumerate(range(1,73-ch))]:
            if self.bo[k][1] == None:
                upright.append(k)
            else:
                break
        for l in [chr(ch-j)+str(nu+i+1) for i, j in enumerate(range(1, ch-64))]:
            if self.bo[l][1] == None:
                upleft.append(l)
            else:
                break
        for m in [chr(j + ch) + str(nu-1-i) for i, j in enumerate(range(1,73-ch)) if nu-1-i > 0]:
            if self.bo[m][1] == None:
                downright.append(m)
            else:
                break
        for n in [chr(ch-j)+str(nu-i-1) for i, j in enumerate(range(1, ch-64)) if nu-1-i > 0]:
            if self.bo[n][1] == None:
                upright.append(n)
            else:
                break
        return upleft+upright+downleft+downright





        print('hey ho')



    # def get_fields_on_the_way(self, start, end):
    #     """
    #     Finds fields between a start field and an end field (for movement of bishops, rooks and queens)
    #     :param start: str, field where piece started (e.g. 'F4')
    #     :param end: str, field where piece wants to move to
    #     :return: list, fields between start and end field
    #     """
    #     ch1 = start[0]
    #     ch2 = end[0]
    #     nu1 = start[1]
    #     nu2 = end[1]
    #     if ord(ch1) > ord(ch2):
    #         let = [chr(i) for i in list(range(ord(ch1), ord(ch2), -1))[1:]]
    #     else:
    #         let = [chr(i) for i in list(range(ord(ch1), ord(ch2)))[1:]]
    #     if int(nu1) > int(nu2):
    #         num = [str(x) for x in list(range(int(nu1), int(nu2), -1))[1:]]
    #     else:
    #         num = [str(x) for x in list(range(int(nu1), int(nu2)))[1:]]
    #
    #     # if movement is rook-move
    #     if len(let) == 0 and len(num) > 0:
    #         ret = [ch1 + num[i] for i in range(len(num))]
    #     elif len(let) > 0 and len(num) == 0:
    #         ret = [let[i] + nu1 for i in range(len(let))]
    #     else:
    #         ret = [let[i] + num[i] for i in range(len(num))]
    #
    #     return ret
    #
    #
    #
    #
    #
    #         print('add stuff')




