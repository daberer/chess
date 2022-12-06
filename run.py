import pygame, random
from move import Move
from procedure import Game, Sprites
from game_over import Check_game_over
from chess_pieces import Player

def main(start_fen = None, move_count = 0, moves_dict ={0 : 'rnbqkbnrppppppppooooooooooooooooooooooooooooooooPPPPPPPPRNBQKBNR'}):
    pygame.init()

    # COLORS
    BLACK = (0, 0, 0)
    LIGHT = (242, 218, 182)
    DARK = (181, 135, 99)
    LIGHT_GREEN = (204, 208, 129)
    DARK_GREEN = (171, 160, 81)
    RED = (157, 61, 70)

    SCREENWIDTH = 1000
    SCREENHEIGHT = 800

    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Chess - whites turn")

    whose_turn = False
    if move_count % 2 == 0:
        whose_turn = True
    game = Game(move_count=move_count, moves=moves_dict, turn=whose_turn)

    # This will be a list that will contain all the sprites we intend to use in our game.
    Sprites.all_sprites_list = pygame.sprite.Group()
    game.create_boards()
    if start_fen:
        game.fill_board(start_fen)
    else:
        game.fill_board()


    # Allowing the user to close the window...
    carryOn = True
    clock = pygame.time.Clock()
    score = 0
    pl = Player()
    Sprites.all_sprites_list.add(pl)


    # Drawing on Screen
    screen.fill(BLACK)

    # board = pygame.sprite.Group()
    fields = [(i * 100, j * 100) for j in range(8) for i in range(8)]

    game_over = False

    def text_to_screen(screen, text, x, y, size = 50, color = (255, 255, 255), button=False):
        if button:
            clicker = pygame.Rect(x-10, y-5, 180, 35)
            pygame.draw.rect(screen, [80, 80, 90], clicker)  # draw button
        text = str(text)
        font = pygame.font.SysFont(None, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
        if button:
            return clicker
        return

    restart_button = text_to_screen(screen=screen, text='New Game', x=820, y=30, size=45, button=True)
    takeback_button = text_to_screen(screen=screen, text='Take back', x=820, y=80, size=45, button=True)



    def get_weights(p_name, col):
        if p_name == 'Pawn' and col == 'white':
            pass
        elif p_name == 'Pawn' and col == 'black':
            pass
        elif p_name == 'Knight':
            return ['D4', 'D4', 'D5', 'D5', 'E4', 'E4', 'E5', 'E5']
        return []


    def worth_of_piece(piece):
        """
        returns the value of each piece
        :param piece: int, value of piece
        :return:
        """
        if piece.name() == 'King':
            return 2000
        if piece.name() == 'Queen':
            return 900
        if piece.name() == 'Rook':
            return 500
        if piece.name() == 'Bishop':
            return 301
        if piece.name() == 'Knight':
            return 300
        if piece.name() == 'Pawn':
            return 100


    def find_best_move(possible_pieces, enemy_pieces):
        """
        tries to find the best move in iterations
        :param possible_pieces:
        :param enemy_pieces:
        :return:
        """
        highest = [0, None, None, None, None]
        for piece in possible_pieces:
            for enemy in enemy_pieces:
                mv = Move(
                    old_field=game.board[piece.field][0],
                    new_field=game.board[enemy.field][0],
                    piece=piece,
                    old_occupant=enemy,
                    game=game,
                )
                if mv.isthisallowed() and mv.noroadblocks():
                    net_worth = worth_of_piece(enemy)
                    if net_worth > highest[0]:
                        highest = [worth_of_piece(enemy), piece, enemy, mv]
        # TODO: Next step: add one counter move by the other player -> will attack hanging pieces only (not protected)..?
        if highest[0] > 0:
            return highest
        return []


    def execute_move(white_move, computer_move=False):
        game.recreate_checkdict()
        col = 'black'
        if white_move:
            col = 'white'
        game.enpassant_expired(col)  # possible enpassant only for 1 round

        if computer_move:
            possible_pieces = [
                game.board[b][1]
                for b in game.board
                if game.board[b][1] != None and game.board[b][1].color == col
            ]
            enemy_pieces = [
                game.board[b][1]
                for b in game.board
                if game.board[b][1] != None and game.board[b][1].color != col
            ]
            VIP_target = find_best_move(possible_pieces, enemy_pieces)

            if VIP_target:
                game.legal(
                    VIP_target[3],
                    VIP_target[1],
                    game.board[VIP_target[2].field][0][0],
                    game.board[VIP_target[2].field][0][1],
                    VIP_target[2],
                )
                return True

            piece = random.choice(possible_pieces)

            possible_fields = [
                b
                for b in game.board
                if not game.board[b][1]
                or (game.board[b][1] and game.board[b][1].color != col)
            ]

            weights = get_weights(piece.name(), col)

            if len(weights):
                for way in weights:
                    possible_fields.insert(random.randint(0, len(possible_fields)), way)

            while len(possible_fields):
                goal = random.choice(possible_fields)
                possible_fields.remove(goal)
                old_occupant = game.board[goal][1]
                mv = Move(
                    old_field=game.board[piece.field][0],
                    new_field=game.board[goal][0],
                    piece=piece,
                    old_occupant=old_occupant,
                    game=game,
                )
                if game.legal(
                    mv, piece, game.board[goal][0][0], game.board[goal][0][1], old_occupant
                ):
                    return True

        if len(pl.carry_pieces_list) > 0:
            piece = pl.carry_pieces_list[0]
            game.activate_piece(pl.carry_pieces_list[0])
            pl.carry_pieces_list = []

            if game.turn and game.active_piece.color == 'black':
                game.go_home(game.active_piece)
            elif not game.turn and game.active_piece.color == 'white':
                game.go_home(game.active_piece)
            game.active_piece.rect.x = round(game.active_piece.rect.x, -2)
            game.active_piece.rect.y = round(game.active_piece.rect.y, -2)

            old_occupant = game.board[
                game.board_code[game.active_piece.rect.x, game.active_piece.rect.y]
            ][1]
            origin = game.board[piece.field][0]
            new_field = (game.active_piece.rect.x, game.active_piece.rect.y)
            mv = Move(
                old_field=origin,
                new_field=new_field,
                piece=piece,
                old_occupant=old_occupant,
                game=game,
            )
            ret = game.legal(
                mv, piece, game.active_piece.rect.x, game.active_piece.rect.y, old_occupant
            )
            game.recreate_checkdict()
            go = Check_game_over(piece.color, game)
            return ret, go.checkmate(), origin, new_field


    def end_game():
        if game.turn:
            color = 'Black'
        else:
            color = 'White'
        text_to_screen(screen=screen, text=f'{color} wins!', x=200, y=350, size=100, color=((64, 224, 208)))
        pygame.display.flip()
        import time
        time.sleep(5)
        pygame.quit()


    def draw_field(color, x, y):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 100, 100))


    def draw_board(origin_field=None, destination_field=None, check=None):
        king_field = (-99, -99)
        if check:
            color = 'black'
            if game.turn:
                color = 'white'
            king_field = game.board[game.find_king(color).field][0]

        for i, field in enumerate(fields):
            if field == king_field:
                draw_field(RED, field[0], field[1])
            elif (field == origin_field) or (field == destination_field):
                col = LIGHT_GREEN
                if (i + int(i / 8)) % 2 == 0:
                    col = DARK_GREEN
                draw_field(col, field[0], field[1])
            else:
                col = LIGHT
                if (i + int(i / 8)) % 2 == 0:
                    col = DARK
                draw_field(col, field[0], field[1])


    game.recreate_checkdict()
    correct_move = False
    origin = (0, 0)
    new_field = (0, 0)


    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    main()
                if takeback_button.collidepoint(mouse_pos):
                    if game.move_count > 0:
                        del game.moves[game.move_count]
                        last_move = game.move_count - 1
                        main(start_fen=game.moves[last_move], move_count=last_move, moves_dict=game.moves)

                blocks_hit_list = pygame.sprite.spritecollide(
                    pl, Sprites.all_sprites_list, False
                )
                for i, block in enumerate(blocks_hit_list):
                    if block.name() == 'Player':
                        blocks_hit_list.pop(i)
                # prevent more than one pieces from being picked up
                if len(blocks_hit_list) > 1:
                    pl.carry_pieces_list = [blocks_hit_list[0]]
                else:
                    pl.carry_pieces_list = blocks_hit_list


            elif event.type == pygame.MOUSEBUTTONUP:
                if (
                    len(pl.carry_pieces_list) > 0
                ):  # False if just clicking into an empty field
                    correct_move, check_status, origin, new_field = execute_move(
                        game.turn, computer_move=False
                    )
                    game_over, check_given = check_status
                    if correct_move:
                        game.next_move()
                        if game.turn:
                            cap = "Chess - whites turn "
                        else:
                            cap = "Chess - blacks turn "
                        if check_given:
                            cap += '- check'
                            game.check_given = True
                        else:
                            game.check_given = False
                        pygame.display.set_caption(cap)
                    else:
                        if len(
                            blocks_hit_list
                        ):  # if touched piece is going to some illegal field, hop back where it came from
                            game.go_home(blocks_hit_list[0])

            if correct_move:
                draw_board(
                    origin_field=origin, destination_field=new_field, check=game.check_given
                )
            else:
                draw_board()

            Sprites.all_sprites_list.update()

            # Now let's draw all the sprites in one go.
            Sprites.all_sprites_list.draw(screen)

            # Refresh Screen
            pygame.display.flip()
            if game_over:
                end_game()

            # Number of frames per secong e.g. 60
            clock.tick(200)

    pygame.quit()


if __name__ == '__main__':
    main()
