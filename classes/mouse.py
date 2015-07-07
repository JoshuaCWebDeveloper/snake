# pygame module requried
import pygame
# import classes
from .game import Game
# define class
class Mouse(pygame.sprite.Sprite):
    """ Class that defines a mouse
    Inherits -- PyGame Sprite class
    """
    
    def __init__(self, position, size):
        """ Constructor
        position --     (list -- int) x, y coordinates of mouse's top left corner
        size  --        (list -- int) width, height of mouse
        """
        # call parent Sprite constructor
        super().__init__()
        # Create block image
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(Game.GREY)
        # Get rectangle object of our image from pygame
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
    