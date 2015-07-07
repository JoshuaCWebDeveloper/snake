# pygame and module requried
import pygame
# define class
class Wall(pygame.sprite.Sprite):
    """ Class that defines walls
    Inherits -- PyGame Sprite class
    """
    
    def __init__(self, color, position, size):
        """ Constructor
        color --        (tuple) Group of RGB values
        position --     (list -- int) x, y coordinates of wall's top left corner
        size  --        (list -- int) width, height dimensions of block
        """
        # call parent Sprite constructor
        super(Wall, self).__init__()
        # Create wall image
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(color)
        # Get rectangle object of our image from pygame
        self.rect = self.image.get_rect()
        # set position
        self.rect.x = position[0]
        self.rect.y = position[1]
        
    