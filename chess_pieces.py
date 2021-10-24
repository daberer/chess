import pygame
import utils
WHITE = (255, 255, 255)


#Set up pieces
def set_up_piece(color, coordinate_tuple, kind, field):
    piece = kind(color, field)
    piece.rect.x = coordinate_tuple[0]
    piece.rect.y = coordinate_tuple[1]
    return piece

def update(piece, piecex, piecey, intercept=False):
    """
    Update dictionary with positions
    :param piece:
    :param piecex:
    :param piecey:
    :param intercept: if the updated dict is a hypothetical dict not real board
    :return:
    """
    if piece.name() == 'Pawn' and ((piece.color == 'white' and piecey == 0) or (piece.color == 'black' and piecey == 700)):
        field = piece.field
        piece.kill()
        piece = set_up_piece(piece.color, (piecex, piecey), Queen, field)
        utils.all_sprites_list.add(piece)


    if intercept:
        utils.intercept_bo[utils.ob[piecex, piecey]][1] = piece
        utils.intercept_bo[piece.field][1] = None
        piece.field = utils.ob[piecex, piecey]
    else:
        utils.bo[utils.ob[piecex, piecey]][1] = piece
        utils.bo[piece.field][1] = None
        piece.field = utils.ob[piecex, piecey]
        return True

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, field):
        super().__init__()
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field

    def name(self):
        return self.__class__.__name__

class Pawn(Piece):
    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)


        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_pawn.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_pawn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()



class Knight(Piece):
    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_knight.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_knight.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class Bishop(Piece):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_bishop.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_bishop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

class Rook(Piece):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)
        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_rook.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_rook.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class Queen(Piece):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_queen.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_queen.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class King(Piece):
    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_king.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_king.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    """
    This class represents the player
    """
    def __init__(self):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.set_alpha(128)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.carry_pieces_list = []

    def name(self):
        return self.__class__.__name__

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        for piece in self.carry_pieces_list:
            piece.rect.center = (pos[0], pos[1])









