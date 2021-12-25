from move import Move
from check import Attacked_fields



class Check_game_over:
    def __init__(self, col, game):
        self.color = col
        self.game = game

    def run_away(self):
        """
        Returns True if the king can flee.
        :return:
        """
        ch, nu = ord(self.king.field[0]), int(self.king.field[-1])
        hor = [
            chr(j) + str(nu)
            for j in [i + ch for i in range(-1, 2, 2)]
            if j > 64 and j < 73
        ]
        ver = [
            chr(ch) + str(j)
            for j in [i + nu for i in range(-1, 2, 2)]
            if j < 9 and j > 0
        ]
        diag = []
        for num in ver:
            for let in hor:
                diag.append(let[0] + (num[1]))
        fields = hor + ver + diag

        for field in fields:
            if self.king.color == 'black' and self.game.board[field][1] == None:
                if self.game.board_check[field] not in [-1, 1]:
                    return True

            if self.king.color == 'white' and self.game.board[field][1] == None:
                if self.game.board_check[field] not in [1, 2]:
                    return True
        return False

    def king_in_check(self, king=None):
        """
        see if king is in check according to the game.board_check dictionary.
        :param king: Object of chess_pieces.King class, makes code reuseable.
        :return:
        """
        if king:
            self.king = king
        if self.king.color == 'black' and self.game.board_check[self.king.field] not in [-1, 1]:
            return False
        if self.king.color == 'white' and self.game.board_check[self.king.field] not in [1, 2]:
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
            self.game.board_intercept = {key: value for key, value in self.game.board.items()}

        # TODO prevent that they are the same thing!!!!!!
        interceptors = [
            self.game.board[b][1]
            for b in self.game.board
            if self.game.board[b][1] != None and self.game.board[b][1].color == col
        ]
        enemies = [
            self.game.board[b][1]
            for b in self.game.board
            if self.game.board[b][1] != None and self.game.board[b][1].color != col
        ]
        empty_fields = [b for b in self.game.board.keys() if self.game.board[b][1] == None]
        for interceptor in interceptors:
            origin = interceptor.field
            # check if someone on my team an kill someone of theirs to save the king
            for enemy in enemies:
                go_back_to_bo()
                mv = Move(
                    old_field=self.game.board[interceptor.field][0],
                    new_field=self.game.board[enemy.field][0],
                    piece=interceptor,
                    old_occupant=enemy,
                    game=self.game
                )
                # look if we can take down piece
                if mv.isthisallowed() and mv.noroadblocks():
                    self.game.update(
                        interceptor,
                        self.game.board[interceptor.field][0][0],
                        self.game.board[interceptor.field][0][1],
                        intercept=True,
                    )
                    at = Attacked_fields(self.game.board_intercept, self.game.board_code)
                    # find all attacked fields but exclude the "taken" enemy
                    self.game.board_check = at.get_dict_of_fields((enemy.name(), enemy.field))
                    # piece = set_up_piece(piece.color, (piecex, piecey), Queen, field)
                    self.game.update(
                        interceptor, self.game.board[origin][0][0], self.game.board[origin][0][1]
                    )
                    go_back_to_bo()
                    if not self.king_in_check():
                        return True

        for interceptor in interceptors:
            origin = interceptor.field
            # Hail mary
            for field in empty_fields:
                go_back_to_bo()
                mv = Move(
                    old_field=self.game.board[interceptor.field][0],
                    new_field=self.game.board[field][0],
                    piece=interceptor,
                    old_occupant=None,
                    game=self.game
                )
                if mv.isthisallowed() and mv.noroadblocks():
                    self.game.update(
                        interceptor,
                        self.game.board[field][0][0],
                        self.game.board[field][0][1],
                        intercept=True,
                    )
                    at = Attacked_fields(self.game.board_intercept, self.game.board_code)
                    self.game.board_check = at.get_dict_of_fields()
                    # put interceptor back where he was so that his field does not change for loop
                    self.game.update(
                        interceptor, self.game.board[origin][0][0], self.game.board[origin][0][1]
                    )
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
        color = 'black'
        if self.color == 'black':
            color = 'white'
        self.king = self.game.find_king(color)
        check = False

        if self.king.color == 'black' and self.game.board_check[self.king.field] in [-1, 1]:
            check = True

        if self.king.color == 'white' and self.game.board_check[self.king.field] in [1, 2]:
            check = True

        if check:
            if not self.run_away():
                if not self.interception():
                    return True, True
            return False, True
        else:
            return False, False
