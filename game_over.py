class Check_game_over():
    def __init__(self, checkdict, col, bo, ob):
        self.checkdict = checkdict
        self.color = col
        self.bo = bo
        self.ob = ob



    def find_king(self):
        self.king = ''
        vals = list(self.bo.values())
        for k,j in vals:
            if j:
                if j.name() == 'King':
                    if j.color != self.color:
                        self.king = j

    def run_away(self):
        """
        checks if the king can flee.
        :return:
        """
        ch, nu = ord(self.king.field[0]), int(self.king.field[-1])
        hor = [chr(j)+str(nu) for j in [i + ch for i in range(-1,2,2)] if j > 64 and j < 73]
        ver = [chr(ch) + str(j) for j in [i + nu for i in range(-1,2,2)] if j < 9 and j > 0]
        diag = []
        for num in ver:
            for let in hor:
             diag.append(let[0] + (num[1]))
        fields = hor + ver + diag

        for field in fields:
            if self.king.color == 'black' and self.bo[field][1] == None:
                if self.checkdict[field] not in [-1, 1]:
                    return True

            if self.king.color == 'white' and self.bo[field][1] == None:
                if self.checkdict[field] not in [1, 2]:
                    return True
        return False


    def checkmate(self):
        """
        finds the enemy king from dict, then checks if the king is checked. In case of check calls the run_away function
        to see if the king can flee.
        returns True if check mate
        :return:
        """
        self.find_king()
        check = False
        if self.king.color == 'black' and self.checkdict[self.king.field] in [-1,2]:
            check = True

        if self.king.color == 'white' and self.checkdict[self.king.field] in [1,2]:
            check = True

        if check:
            if not self.run_away():
                return True
        return False

