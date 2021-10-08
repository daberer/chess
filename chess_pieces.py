import pygame
import math

WHITE = (255, 255, 255)
GREEN = (20, 255, 140)

centers = []
for x in range(0, 700, 100):
    for y in range(0, 700, 100):
        centers.append((x,y))

class Pawn(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_pawn.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_pawn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

class Knight(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color

        # Instead we could load a proper pciture of a car...
        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_knight.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_knight.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()





class Bishop(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_bishop.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_bishop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

class Rook(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_rook.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_rook.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class Queen(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color

        if self.color == 'black':
            self.image = pygame.image.load("pieces/black_queen.png").convert_alpha()
        else:
            self.image = pygame.image.load("pieces/white_queen.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()


class King(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA, 16)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color

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
        #self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.carry_pieces_list = []

    def update(self):
        pos = pygame.mouse.get_pos()

        diff_x = self.rect.x - pos[0]
        diff_y = self.rect.y - pos[1]

        self.rect.x = pos[0]
        self.rect.y = pos[1]


        for piece in self.carry_pieces_list:
            print(piece.__class__.__name__)
            piece.rect.x -= diff_x
            piece.rect.y -= diff_y
            if (math.hypot(int(str(piece.rect.x)[-2:]), int(str(piece.rect.y)[-2:])) < 30 or \
                    math.hypot(abs(int(str(piece.rect.x)[-2:])-100), abs(int(str(piece.rect.y)[-2:])-100)) < 30):
                #and (piece.rect.x % 100 != 0 and piece.rect.y % 100 != 0):
                piece.rect.x = round(piece.rect.x, -2)
                piece.rect.y = round(piece.rect.y, -2)
            break









