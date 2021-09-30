import pygame
WHITE = (255, 255, 255)

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
            self.image = pygame.image.load("black_pawn.png").convert_alpha()
        else:
            self.image = pygame.image.load("white_pawn.png").convert_alpha()
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
            self.image = pygame.image.load("black_knight.png").convert_alpha()
        else:
            self.image = pygame.image.load("white_knight.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y


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
            self.image = pygame.image.load("black_bishop.png").convert_alpha()
        else:
            self.image = pygame.image.load("white_bishop.png").convert_alpha()
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
            self.image = pygame.image.load("black_rook.png").convert_alpha()
        else:
            self.image = pygame.image.load("white_rook.png").convert_alpha()
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
            self.image = pygame.image.load("black_queen.png").convert_alpha()
        else:
            self.image = pygame.image.load("white_queen.png").convert_alpha()
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
            self.image = pygame.image.load("black_king.png").convert_alpha()
        else:
            self.image = pygame.image.load("white_king.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()



