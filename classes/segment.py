# pygame and random modules requried
import pygame
import math
# define class
class Segment(pygame.sprite.Sprite):
    """ Class that defines a segment of our snake
    Inherits -- PyGame Sprite class
    """
    
    def __init__(self, color, position, thickness, direction):
        """ Constructor
        color --       (tuple) Group of RGB values
        position --    (list -- int) x, y coordinates of segment's top left corner
                                    (i.e. screen dimensions)
        thickness  --  (int) thickness of snake
        orientation -- (str)    Whether this segment is moving
                                "up", "right", "down", or "left"
        """
        # call parent Sprite constructor
        super().__init__()
        
        self.direction = direction
        # Create block image
        if self.direction in ["left", "right"]:
            self.image = pygame.Surface([1, thickness])
        else:
            self.image = pygame.Surface([thickness, 1])
        self.image.fill(color)
        # Get rectangle object of our image from pygame
        # draw player, position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        # init length
        self.length = 1
        # track the real position (float) of segment
        self.realPos = {
            "x": self.rect.x,
            "y": self.rect.y
        }
        
    def add_length (self, l):
        """ Adds or subtracts from length, modifiying dimensions as neccessary.
        l --        (float) The amount of length to add (negative values subtract)
        returns --  (int) The new length
        """
        # Update length
        self.length += l
        # Update dimensions
        new_width = self.rect.width
        new_height = self.rect.height
        if self.direction in ["left", "right"]:
            new_width = math.floor(self.length)
            if new_width < 0:
                new_width = 0
        else:
            new_height = math.floor(self.length)
            if new_height < 0:
                new_height = 0
        self.image = pygame.transform.scale(self.image, [new_width, new_height])
        # get new rect
        self.rect = self.image.get_rect()
        self.rect.x = math.floor(self.realPos["x"])
        self.rect.y = math.floor(self.realPos["y"])
        # If we are moving down or right
        return self.length
    
    def move_pos (self, vector):
        """ Moves the segments by updating the x, y coordinates using the vector.
        vector --   (list) x, y values, the amount to move the segment right/down
        returns --  (object) The new real position
        """
        #x = self.rect.x
        #y = self.rect.y
        # update the real position
        self.realPos["x"] += vector[0]
        self.realPos["y"] += vector[1]
        # use the real position to update rect
        self.rect.x = math.floor(self.realPos["x"])
        self.rect.y = math.floor(self.realPos["y"])
        #print (vector, [self.rect.x-x, self.rect.y-y])
        # return the real position
        return self.realPos
     
    def update_realPos (self):
        """ Updates the realPos to the x, y properties of our rect.
        returns --  (None)
        """
        self.realPos["x"] = self.rect.x
        self.realPos["y"] = self.rect.y
    