import pygame


WHITE = (255, 255, 255)


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

    def return_class(self):
        return type(self)


class Pawn(Piece):
    def __init__(self, color, field, enpassant=False):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_pawn.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_pawn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.enpassant = enpassant


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
    def __init__(self, color, field, castle=True):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)
        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_rook.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_rook.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.castle = castle


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
    def __init__(self, color, field, castle=True):
        # Call the parent class (Sprite) constructor
        super().__init__(color, field)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_king.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_king.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.castle = castle


class Player(pygame.sprite.Sprite):
    """
    This class represents the player
    """

    def __init__(self):
        """Constructor. Pass in the color of the block,
        and its x and y position."""

        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.set_alpha(0)
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
