# pygame module requried
import pygame
#import classes
from .segment import Segment 
# define class
class Player(object):
    """ Class that defines the player snake
    Inherits -- PyGame Sprite class
    """
    
    # How much we grow
    GROW_LENGTH = 20
    
    def __init__(self, game, position, size, velocity):
        """ Constructor
        game --         (object -- Game) reference to the game
        position --     (list -- int) x, y coordinates of snake's top left corner
        size  --        (list -- int) starting length, thickness dimensions of snake
        velocity --     (int) the starting spped of the player
        """
        # call parent Sprite constructor
        super().__init__()
        # set game
        self.game = game
        # set thickness
        self.thickness = size[1]
        # store starting position and length
        self.start = {
            "pos": position,
            "length": size[0]
        }
        # set velocity
        self.velocity = velocity
        # create new player
        self._new(position, size[0])
        
    def resurrect (self):
        """ Removes the current player, and creates a new player at same speed."""
        # draw level without player
        self.game.get_level().draw(self.game.board, False)
        # draw current player with transparent background
        player = pygame.Surface(self.game.BOARD_SIZE)
        player.fill(self.game.BLACK)
        player.set_colorkey(self.game.BLACK)
        self.draw(player)
        # fade out player
        self.game.fade_out([player], [self.game.board])
        # remove player segments from collideables
        self.game.get_level().collideables.remove(self.segments)
        # reset player
        self._new(self.start["pos"], self.start["length"])
        # draw new player
        player.fill(self.game.BLACK)
        self.draw(player)
        # fade in player
        self.game.fade_in([player], [self.game.board])
        # pause game
        self.game.paused = True
        
    def _new (self, position, length):
        """ Performs operations involved in the creation of a new player."""
        # set direction
        self.direction = "left"
        # set segments
        self.segment_list = []
        self.segments = pygame.sprite.Group()
        self.create_segment(position)
        # set length
        self.segment_list[0].add_length(length)
    
    def create_segment(self, position=False):
        """ Creates a new snake segment and makes it the new head.
        direction --      (str) Whether segment is horizontal or vertical
        position --     (list -- int) x, y coordinates of snake's top left corner
        returns -- (none)
        """
        # If there is more than one segment
        if len(self.segment_list) > 1:
            # If the second segment is
            # running the opposite direction as this new segment
            seg2 = self.segment_list[1]
            seg1 = self.segment_list[0]
            if      self.direction == "up" and seg2.direction == "down" or\
                    self.direction == "down" and seg2.direction == "up" or\
                    self.direction == "left" and seg2.direction == "right" or\
                    self.direction == "right" and seg2.direction == "left":
                #keep us heading in the previous direction for now
                new_direct = self.direction
                self.direction = seg1.direction
                # Because we are going to be running parallel
                # with the second segment, if we aren't at least one segment
                # thickness away from the second segment, we will collide with
                # the second segment. To prevent that, wait until our first
                # segment is at least twice as long as our thickness.
                # This runs an internal game loop for the duration of the loop.
                while seg1.length <= (self.thickness * 2) + 1:
                    # Don't listen for events while we are wating
                    # (easy way to ignore turns)
                    # Run logic
                    self.game.run_logic()
                    # Draw frame
                    self.game.display_frame()
                    # tick clock
                    self.game.update_clock()
                # now we can head our new direction
                self.direction = new_direct
                
        # if we were not given a position, set to arbitrary
        if not position:
            pos = [0, 0]
        else:
            pos = position
        seg = Segment (self.game.GREEN, pos, self.thickness, self.direction)
        self.segment_list.insert(0, seg)
        self.segments.add(seg)
        self.game.get_level().all_sprites.add(seg)
        # add the thickness of the previous segment to our length
        seg.add_length(self.thickness)
        # if we weren't given a position, position now
        if not position:
            # get previous head
            head = self.segment_list[1]
            # use our direction (seg) and head's direciton to position ourselves
            # we should evenly overlap the previous segment by our thickness
            # -- (overlap at corner)
            if head.direction == "up":
                seg.rect.top = head.rect.top
                if seg.direction == "left":
                    seg.rect.right = head.rect.right
                else:
                    seg.rect.left = head.rect.left
            if head.direction == "left":
                if seg.direction == "up":
                    seg.rect.bottom = head.rect.bottom
                else:
                    seg.rect.top = head.rect.top
                seg.rect.left = head.rect.left
            if head.direction == "down":
                seg.rect.bottom = head.rect.bottom
                if seg.direction == "left":
                    seg.rect.right = head.rect.right
                else:
                    seg.rect.left = head.rect.left
            if head.direction == "right":
                if seg.direction == "up":
                    seg.rect.bottom = head.rect.bottom
                else:
                    seg.rect.top = head.rect.top
                seg.rect.right = head.rect.right
            # Update the realPos of our segment
            seg.update_realPos()
        
        # If there are more than two segments
        if len(self.segment_list) > 3:
            # make the third segment collideable
            # (first two player segments aren't collideable)
            self.game.get_level().collideables.add(self.segment_list[3])
    
    def remove_segment (self):
        """ Removes the tail segment from the snake.
            The next segment up is the tail
        returns -- (None)
        """
        tail = self.segment_list[-1]
        # If there are more than three segments
        if len(self.segment_list) > 3:
            # remove this from collideables
            self.game.get_level().collideables.remove(tail)
        # Remove from all sprites
        self.game.get_level().all_sprites.remove(tail)
        self.segments.remove(tail)    
        # Delete segment
        del self.segment_list[-1]           
    
    def get_vector (self):
        """ Uses our direction to create a vector for our player
        returns --  (object) The vector for our player
        """
        # If we are headed left
        if self.direction == "left":
            return {
                "x": -self.velocity,
                "y": 0
            }
        # If we are headed right
        if self.direction == "right":
            return {
                "x": self.velocity,
                "y": 0
            }
        # If we are headed up
        if self.direction == "up":
            return {
                "x": 0,
                "y": -self.velocity
            }
        # If we are headed down
        if self.direction == "down":
            return {
                "x": 0,
                "y": self.velocity
            }
            
    def update(self):
        """ Updates the player position based on vector.
        Handles collisions with mice.
        returns -- (none)
        """
        # Get player vector
        vector = self.get_vector()
        # Get length change from combined vector (one should be zero)
        length = abs(vector["x"] + vector["y"])
        # Move head segment
        head = self.segment_list[0]
        # If we have more than one segment
        if len(self.segment_list) > 1:
            # Lengthen head segment
            head.add_length(length)
        # Else, if we are headed down or right
        elif head.direction in ["down", "right"]:
            # Update head segment position
            head.move_pos([vector["x"], vector["y"]])
        # Update head segment position
        if head.direction in ["up", "left"]:
            head.move_pos([vector["x"], vector["y"]])
        # If we have more than one segment
        if len(self.segment_list) > 1:
            # Shorten tail segment
            while length > 0:
                # Get last segment
                tail = self.segment_list[-1]
                # Subtract length, and get new length of segment
                new_len = tail.add_length(-length)
                # If the new length is less than or equal to our thickness
                if new_len <= self.thickness:
                    # Delete the segment
                    self.remove_segment()
                    # Update remaining length to remove from next segment
                    length = abs(new_len - self.thickness)
                else:
                    # The segment still exists
                    # Update tail segment position
                    if tail.direction == "down":
                        tail.move_pos([0, length])
                    elif tail.direction == "right":
                        tail.move_pos([length, 0])
                    # there is no more length to remove
                    length = 0
        
        # Check and see if we have collided with any mice (remove hit mice)
        mouse_hits = pygame.sprite.spritecollide(head, self.game.get_level().mice, True)
        # Loop through hit mice
        for m in mouse_hits:
            # Count mice
            self.game.get_level().count_mice(1)
            # Get last segment
            tail = self.segment_list[-1]
            # Add length to tail
            tail.add_length(self.GROW_LENGTH)
            # Update tail segment position
            if tail.direction == "down":
                tail.move_pos([0, -self.GROW_LENGTH])
            elif tail.direction == "right":
                tail.move_pos([-self.GROW_LENGTH, 0])
            # create new mouse
            self.game.get_level().create_mouse()
        
        # Check and see if our head has collided with a wall or ourselves
        collisions = pygame.sprite.spritecollide(head, self.game.get_level().collideables, False)
        # If we have
        if collisions:
            # If the level is complete
            if self.game.get_level().complete:
                # Level up!
                self.game.level_up()
            # Else, if we have any lives
            elif self.game.lives > 0:
                # Use one
                self.game.lives -= 1
                # Resurrect ourselves
                self.resurrect()
            else:
                # Whoops! Game over!
                self.game.end()
            
    def draw(self, screen):
        """ Draws the player's segments.
        returns -- (None)
        """
        self.segments.draw(screen)
                
    def move_left(self):
        """ Calculate user movement: left """
        # If we aren't moving left/right
        if self.direction not in ["left", "right"]:
            # Change our direction
            self.direction = "left"
            # Create new segment
            self.create_segment()
    
    def move_right(self):
        """ Calculate user movement: right """
        # If we aren't moving left/right
        if self.direction not in ["left", "right"]:
            # Change our direction
            self.direction = "right"
            # Create new segment
            self.create_segment()
       
    def move_up(self):
        """ Calculate user movement: up """
        # If we aren't moving up/down
        if self.direction not in ["up", "down"]:
            # Change our direction
            self.direction = "up"
            # Create new segment
            self.create_segment()
       
    def move_down(self):
        """ Calculate user movement: down """
        # If we aren't moving up/down
        if self.direction not in ["up", "down"]:
            # Change our direction
            self.direction = "down"
            # Create new segment
            self.create_segment()
      
    def change_velocity(self, change):
        """ Changes the velocity of the player.
        change --   (int) The amount to increase the velocity by.
        returns --  (none)
        """
        self.velocity += change
        