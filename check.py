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

    def setify(self):
        self.white_attackfields = set([item for sublist in self.white_attackfields for item in sublist])
        self.black_attackfields = set([item for sublist in self.black_attackfields for item in sublist])

    def return_dict(self):
        for ele in self.white_attackfields:
            self.di[ele] -= 1
        for ele in self.black_attackfields:
            self.di[ele] += 2
        return self.di

    def pawn_find_attacked_fields(self):
        ch, nu = ord(self.piece.field[0]), int(self.piece.field[-1])
        nu -=1
        if self.piece.color == 'white':
            nu += 2
        # join char with number for adjacent letters as long as numbers and letters within A-H and 0-8
        return [chr(k) + str(nu) for k in [j for j in [i + ch for i in range(-1,2,2)] if j > 64 and j < 73] if nu < 9 and nu > -1]



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




