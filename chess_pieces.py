import pygame

WHITE = (255, 255, 255)
GREEN = (20, 255, 140)

centers = []
for x in range(0, 700, 100):
    for y in range(0, 700, 100):
        centers.append((x,y))

class Pawn(pygame.sprite.Sprite):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field
        if color == 'white':
            self.move = (0, 100)
        else:
            self.move = (0, -100)

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_pawn.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_pawn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

class Knight(pygame.sprite.Sprite):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_knight.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_knight.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class Bishop(pygame.sprite.Sprite):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_bishop.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_bishop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

class Rook(pygame.sprite.Sprite):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_rook.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_rook.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class Queen(pygame.sprite.Sprite):

    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_queen.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_queen.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class King(pygame.sprite.Sprite):
    def __init__(self, color, field):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.field = field

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

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        for piece in self.carry_pieces_list:
            piece.rect.center = (pos[0], pos[1])







