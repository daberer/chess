from move import Move
from check import Attacked_fields
import utils
import copy


class Check_game_over():
    def __init__(self, col):
        self.color = col




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
            if self.king.color == 'black' and utils.bo[field][1] == None:
                if utils.check[field] not in [-1, 1]:
                    return True

            if self.king.color == 'white' and utils.bo[field][1] == None:
                if utils.check[field] not in [1, 2]:
                    return True
        return False

    def king_in_check(self, king=None):
        """
        see if king is in check according to the utils.check dictionary.
        :param king: Object of chess_pieces.King class, makes code reuseable.
        :return:
        """
        if king:
            self.king = king
        if self.king.color == 'black' and utils.check[self.king.field] not in [-1, 1]:
            return False
        if self.king.color == 'white' and utils.check[self.king.field] not in [1, 2]:
            return False
        return True

    def interception(self):
        """
        check if anyone can jump between the attacker and the king.
        :return:
        """
        col = self.king.color
        def go_back_to_bo():
            """
            renew hypothetical dict
            :return:
            """
            utils.intercept_bo = {key: value for key, value in utils.bo.items()}

        # TODO prevent that they are the same thing!!!!!!
        interceptors = [utils.bo[b][1] for b in utils.bo if utils.bo[b][1] != None and utils.bo[b][1].color == col]
        enemies = [utils.bo[b][1] for b in utils.bo if utils.bo[b][1] != None and utils.bo[b][1].color != col]
        empty_fields = [b for b in utils.bo.keys() if utils.bo[b][1] == None]
        for interceptor in interceptors:
            origin = interceptor.field
            #check if someone on my team an kill someone of theirs to save the king
            for enemy in enemies:
                go_back_to_bo()
                mv = Move(utils.bo[interceptor.field][0], utils.bo[enemy.field][0], interceptor, enemy, utils.bo, utils.ob,
                          utils.check)
                # look if we can take down piece
                if mv.isthisallowed() and mv.noroadblocks():
                    utils.update(interceptor, utils.bo[interceptor.field][0][0], utils.bo[interceptor.field][0][1],intercept=True)
                    at = Attacked_fields(utils.intercept_bo, utils.ob, utils.check)
                    # find all attacked fields but exclude the "taken" enemy
                    utils.check = at.get_dict_of_fields((enemy.name(), enemy.field))
                    #piece = set_up_piece(piece.color, (piecex, piecey), Queen, field)
                    utils.update(interceptor, utils.bo[origin][0][0], utils.bo[origin][0][1])
                    go_back_to_bo()
                    if not self.king_in_check():
                        return True

        for interceptor in interceptors:
            origin = interceptor.field
            # Hail mary
            for field in empty_fields:
                go_back_to_bo()
                mv = Move(utils.bo[interceptor.field][0], utils.bo[field][0], interceptor, None, utils.bo, utils.ob,
                          utils.check)
                if mv.isthisallowed() and mv.noroadblocks():
                    utils.update(interceptor, utils.bo[field][0][0], utils.bo[field][0][1],
                       intercept=True)
                    at = Attacked_fields(utils.intercept_bo, utils.ob, utils.check)
                    utils.check = at.get_dict_of_fields()
                    # put interceptor back where he was so that his field does not change for loop
                    utils.update(interceptor, utils.bo[origin][0][0], utils.bo[origin][0][1])
                    if not self.king_in_check():
                        return True
        return False


    def checkmate(self):
        """
        finds the enemy king from dict, then checks if the king is checked. In case of check calls the run_away function
        to see if the king can flee.
        returns True if check mate
        :return:
        """
        self.king = utils.find_king(self.color)
        check = False
        if self.king.color == 'black' and utils.check[self.king.field] in [-1,2]:
            check = True

        if self.king.color == 'white' and utils.check[self.king.field] in [1,2]:
            check = True

        if check:
            if not self.run_away():
                if not self.interception():
                    return True, True
            return False, True
        else:
            return False, False




