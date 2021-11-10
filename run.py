import pygame, random
from move import Move

from game_over import Check_game_over
import utils

pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0,0,0)
LIGHT = (242,218,182)
DARK = (181,135,99)



SCREENWIDTH=800
SCREENHEIGHT=800

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")
font = pygame.font.SysFont(None, 100)

#This will be a list that will contain all the sprites we intend to use in our game.
utils.all_sprites_list = pygame.sprite.Group()


for i, field in enumerate(utils.bo):
    co, ty = utils.fen_code(utils.start_fen[i])
    if ty is not None:
        piece = utils.set_up_piece(co, utils.bo[field][0], ty, field)
        utils.bo[field][1] = piece
        utils.all_sprites_list.add(piece)


#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()
score = 0
pl = utils.Player()
utils.all_sprites_list.add(pl)


#Drawing on Screen
screen.fill(GREEN)


#board = pygame.sprite.Group()
fields = [(i * 100, j * 100) for j in range(8) for i in range(8)]

game_over = False




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
            mv = Move(utils.bo[piece.field][0], utils.bo[enemy.field][0], piece, enemy, utils.bo, utils.ob, utils.check)
            if mv.isthisallowed() and mv.noroadblocks():
                net_worth = worth_of_piece(enemy)
                if net_worth > highest[0]:
                    highest = [worth_of_piece(enemy), piece, enemy, mv]
    # TODO: Next step: add one counter move by the other player -> will attack hanging pieces only (not protected)..?
    if highest[0] > 0:
        return highest
    return []


def execute_move(move_count, computer_move=False):
    utils.recreate_checkdict()
    col = 'black'
    if move_count % 2 == 0:
        col = 'white'
    if computer_move:
        possible_pieces = [utils.bo[b][1] for b in utils.bo if utils.bo[b][1] != None and utils.bo[b][1].color == col]
        enemy_pieces = [utils.bo[b][1] for b in utils.bo if utils.bo[b][1] != None and utils.bo[b][1].color != col]
        VIP_target = find_best_move(possible_pieces, enemy_pieces)

        if VIP_target:
            utils.legal(VIP_target[3], VIP_target[1], utils.bo[VIP_target[2].field][0][0], utils.bo[VIP_target[2].field][0][1], VIP_target[2])
            return True


        piece = random.choice(possible_pieces)

        possible_fields = [b for b in utils.bo if not utils.bo[b][1] or (utils.bo[b][1] and utils.bo[b][1].color != col)]


        weights = get_weights(piece.name(), col)

        if len(weights):
            for way in weights:
                possible_fields.insert(random.randint(0, len(possible_fields)), way)



        while len(possible_fields):
            goal = random.choice(possible_fields)
            possible_fields.remove(goal)
            old_occupant = utils.bo[goal][1]
            mv = Move(utils.bo[piece.field][0], utils.bo[goal][0], piece, old_occupant, utils.bo, utils.ob)
            if utils.legal(mv, piece, utils.bo[goal][0][0], utils.bo[goal][0][1], old_occupant):
                return True


    if len(pl.carry_pieces_list) > 0:
        piece = pl.carry_pieces_list[0]
        pl.carry_pieces_list = []

        if move_count % 2 == 0 and piece.color == 'black':
            utils.go_home(piece)
        elif move_count % 2 != 0 and piece.color == 'white':
            utils.go_home(piece)
        piecex = round(piece.rect.x, -2)
        piecey = round(piece.rect.y, -2)

        old_occupant = utils.bo[utils.ob[piecex, piecey]][1]
        mv = Move(utils.bo[piece.field][0], (piecex, piecey), piece, old_occupant, utils.bo, utils.ob, utils.check)
        ret = utils.legal(mv, piece, piecex, piecey, old_occupant)
        utils.recreate_checkdict()
        go = Check_game_over(piece.color)
        return ret, go.checkmate()




def end_game(move_count):
    if move_count % 2 == 0:
        color = 'White'
    else:
        color = 'Black'
    text_surface = font.render(f'{color} wins!', True, (64, 224, 208))
    screen.blit(text_surface, dest=(200,350))
    pygame.display.flip()
    import time
    time.sleep(5)
    pygame.quit()

def draw_board():
    for i, field in enumerate(fields):
        if (i + int(i / 8)) % 2 == 0:
            pygame.draw.rect(screen, DARK, pygame.Rect(field[0],field[1], 100,100))
        else:
            pygame.draw.rect(screen, LIGHT, pygame.Rect(field[0],field[1], 100,100))

game_over = False
move_count = 0
utils.recreate_checkdict()
auto = False
while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                 carryOn=False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                blocks_hit_list = pygame.sprite.spritecollide(pl, utils.all_sprites_list, False)
                for i, block in enumerate(blocks_hit_list):
                    if block.name() == 'Player':
                        blocks_hit_list.pop(i)
                # prevent more than one pieces from being picked up
                if len(blocks_hit_list) > 1:
                    pl.carry_pieces_list = [blocks_hit_list[0]]
                else:
                    pl.carry_pieces_list = blocks_hit_list

            elif event.type == pygame.MOUSEBUTTONUP:
                correct_move, check_status = execute_move(move_count, computer_move=False)
                game_over, check_given = check_status
                if correct_move:
                    move_count += 1
                    if check_given:
                        print('Check')
                        utils.check_given = True
                    else:
                        utils.check_given = False



            # if move_count % 2!= 0:
            #     import time
            #     time.sleep(0.1)
            #     correct_move = execute_move(move_count, computer_move=True)
            #     if correct_move:
            #         move_count += 1
            #         game_over = check_game_over()


            draw_board()



            utils.all_sprites_list.update()



            #Now let's draw all the sprites in one go.
            utils.all_sprites_list.draw(screen)

            #Refresh Screen
            pygame.display.flip()
            if game_over:
                end_game(move_count -1)

            #Number of frames per secong e.g. 60
            clock.tick(200)

pygame.quit()
