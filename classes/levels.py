# import modules
import pygame
import random
# import classes
from .wall import Wall
from .player import Player
# Defines all levles in the game
class Level(object):
    """ Base class for all levels. """
    
    def __init__(self, game, color=False, wall_color=False):
        """ Constructor, create groups
        game --     (object -- Game) A reference to the current game
        color --    (list) Background color of level in RGB values
        returns --  (none)
        """
        # Set game
        self.game = game
        # Create easy reference to board size
        self.b_size = self.game.BOARD_SIZE
        # Calculate center of screen
        self.bcx = self.b_size[0]/2
        self.bcy = self.b_size[1]/2
        # set colors
        if color is False:
            color = game.BLACK
        self.color = color
        if wall_color is False:
            wall_color = game.BLUE
        # set background image
        self.background = None
        # initialize level properties
        self.num_mice = 0
        self.player_props = {
            "pos": [0, 0],
            "size": [0, 0],
            "speed": 0,
            "accel": 0
        }
        self.mice_finish = 0
        # 10 mice in a bonus round per new life
        self.life_value = 10
        self.next_life = 0
        # Create base walls
        self.walls_list = [
            [wall_color, [0, 0], [game.BOARD_SIZE[0], 20]],
            [wall_color, [game.BOARD_SIZE[0]-20, 20], [20, game.BOARD_SIZE[1]-40]],
            [wall_color, [0, game.BOARD_SIZE[1]-20], [game.BOARD_SIZE[0], 20]],
            [wall_color, [0, 20], [20, game.BOARD_SIZE[1]-40]]
        ]
        
    def create_mouse (self):
        from .mouse import Mouse
        # funtion to generate random position for mouse
        def position ():
            return [
                random.randrange(0, self.game.BOARD_SIZE[0]),
                random.randrange(0, self.game.BOARD_SIZE[1])
            ]
        
        # create position
        pos = position()
        mouse = Mouse (pos, [10, 10])
        # move mouse until it doesn't collide with something else
        # (player, wall, mouse)
        hits = pygame.sprite.spritecollide(mouse, self.all_sprites, False)
        while hits:
            # generate new position
            new_pos = position()
            mouse.rect.x = new_pos[0]
            mouse.rect.y = new_pos[1]
            # look for collisions
            hits = pygame.sprite.spritecollide(mouse, self.all_sprites, False)
        # mouse has been positioned, add to sprites
        self.mice.add(mouse)
        self.all_sprites.add(mouse)
    
    def load (self):
        """ Loads resources and sprites for level.
        returns --  (None)
        """
        # create sprite groups
        self.walls = pygame.sprite.Group()
        self.mice = pygame.sprite.Group()
        self.collideables = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        # create player
        self.player = Player(
            self.game,
            self.player_props["pos"],
            self.player_props["size"],
            self.player_props["speed"]
        )
        # Add player segments to all sprites group
        self.all_sprites.add(self.player.segments)
        # create walls
        for i in range(len(self.walls_list)):
            # create wall
            w = self.walls_list[i]
            # Use Wall to create standard platform
            wall = Wall(w[0], w[1], w[2])
            # add to groups
            self.walls.add(wall)
            self.collideables.add(wall)
            self.all_sprites.add(wall)
        # create mice
        for i in range(self.num_mice):
            self.create_mouse()
        # reset counters
        self.mice_count = 0
        self.next_life = 0
        self.complete = False
        
    def update(self):
        """ Update all of the sprites in this level """
        # update player
        self.player.update()
        # If we have satisfied level requirements
        if self.mice_count >= self.mice_finish:
            # Level is complete
            self.complete = True
        # If we have completed this level
        if self.complete:
            # Keep speeding the player up
            self.player.change_velocity(.05)
            # If we have enough mice for a new life
            if self.next_life >= self.life_value:
                # Give us a life
                self.game.lives += 1
                # Subtract the value of a life
                self.next_life -= self.life_value
    
    def count_mice (self, num_mice):
        """ Update the count of mice eaten.
        num_mice --     (int) The number of mice to add to the count
        returns --  (None)
        """
        # Add points
        points = num_mice
        # If in bonus mode
        if self.complete:
            # Double points
            points *= 2
            # Count mice towards next life
            self.next_life += num_mice
        self.game.add_points(points)
        # Add to the mouse count
        self.mice_count += num_mice
        # Speed the player up
        self.player.change_velocity(num_mice * self.player_props["accel"])
    
    def draw(self, screen, player=True):
        """ Draw everything in this level
        screen --   (object -- pygame.Surface) The surface to draw the level on
        player --   (bool) Whether or not to draw the player (usually True)
        returns --  (None)
        """
        # Draw background
        screen.fill(self.color)
        # Draw objects
        if player:
            self.player.draw(screen)
        self.mice.draw(screen)
        self.walls.draw(screen)
    
    
class Level_01(Level):
    """ Level 01:
        - Player:
            - standard length
            - at center
            - speed of 240
            - acceleration of 1.8
        - 10 mice
        - 75 mice to finish
        - Base wall layout
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.BLACK)
        
        # set player size, position, speed
        self.player_props["size"] = [100, 10]
        # calculate center of screen
        cx = self.game.BOARD_SIZE[0]/2 - self.player_props["size"][0]/2
        cy = self.game.BOARD_SIZE[1]/2 - self.player_props["size"][1]/2
        self.player_props["pos"] = [cx, cy]
        self.player_props["speed"] = 240
        self.player_props["accel"] = 1.8
        # set number of mice
        self.num_mice = 10
        # set number of mice required to finish
        self.mice_finish = 75
        # no extra walls for this level
        

class Level_02(Level):
    """ Level 02:
        - Player:
            - standard length
            - at center
            - speed of 180
            - acceleration of 3.0
        - 10 mice
        - 50 mice to finish
        - Wall layout:
            
            ----    ---
            |         |
            
            |         |
            ---     ---
    
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.BLACK, game.FOREST)
        
        # set player size, position, speed
        self.player_props["size"] = [100, 10]
        # calculate center of screen
        cx = self.game.BOARD_SIZE[0]/2 - self.player_props["size"][0]/2
        cy = self.game.BOARD_SIZE[1]/2 - self.player_props["size"][1]/2
        self.player_props["pos"] = [cx, cy]
        self.player_props["speed"] = 180
        self.player_props["accel"] = 3.0
        # set number of mice
        self.num_mice = 10
        # set number of mice required to finish
        self.mice_finish = 50
        # define walls [color, [x, y], [width, height]]
        self.walls_list.extend([
            [game.FOREST, [100, 100],                    [200, 20]],
            [game.FOREST, [100, 120],                    [20, 50]],
            [game.FOREST, [100, game.BOARD_SIZE[1]-170], [20, 50]],
            [game.FOREST, [100, game.BOARD_SIZE[1]-120], [200, 20]],
            
            [game.FOREST, [game.BOARD_SIZE[0]-300, 100], [200, 20]],
            [game.FOREST, [game.BOARD_SIZE[0]-120, 120], [20, 50]],
            [game.FOREST, [game.BOARD_SIZE[0]-120,
                           game.BOARD_SIZE[1]-170],      [20, 50]],
            [game.FOREST, [game.BOARD_SIZE[0]-300,
                           game.BOARD_SIZE[1]-120],      [200,  20]]
        ])


class Level_03(Level):
    """ Level 03:
        - Player:
            - long length
            - below center
            - speed of 300
            - acceleration of 3.0
        - 10 mice
        - 40 mice to finish
        - Wall layout:
            
            
              -|-   -|-    
            
    
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.BLACK, game.RED)
        
        # set player size, position, speed
        self.player_props["size"] = [200, 10]
        # calculate center of screen
        cx = self.game.BOARD_SIZE[0]/2 - self.player_props["size"][0]/2
        self.player_props["pos"] = [cx, self.game.BOARD_SIZE[1]-50]
        self.player_props["speed"] = 300
        self.player_props["accel"] = 3.0
        # set number of mice
        self.num_mice = 10
        # set number of mice required to finish
        self.mice_finish = 50
        # define walls [color, [x, y], [width, height]]
        self.walls_list.extend([
            [game.RED, [125, 240],                    [150, 20]],
            [game.RED, [190, 175],                    [20, 150]],
            
            [game.RED, [game.BOARD_SIZE[0]-255, 240], [150, 20]],
            [game.RED, [game.BOARD_SIZE[0]-190, 175], [20, 150]]
        ])
 
        
class Level_04(Level):
    """ Level 04:
        - Player:
            - standard length
            - left center
            - speed of 300
            - acceleration of 1.8
        - 15 mice
        - 60 mice to finish
        - Wall layout:
                    
                |    
                |     
                |       
    
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.BLACK, game.YELLOW)
        
        # set player size, position, speed
        self.player_props["size"] = [100, 10]
        # calculate center of screen
        bcx = self.b_size[0]/2
        cx = bcx - self.player_props["size"][0] - 30
        cy = self.b_size[1]/2 - self.player_props["size"][1]/2
        self.player_props["pos"] = [cx, cy]
        self.player_props["speed"] = 300
        self.player_props["accel"] = 1.8
        # set number of mice
        self.num_mice = 15
        # set number of mice required to finish
        self.mice_finish = 60
        # define walls [color, [x, y], [width, height]]
        self.walls_list.extend([
            [game.YELLOW, [bcx-10, 50], [20, self.b_size[1]-100]]
        ])


class Level_05(Level):
    """ Level 05:
        - Player:
            - standard length
            - center
            - speed of 180
            - acceleration of 1.2
        - 15 mice
        - 55 mice to finish
        - Wall layout:
                    
            ---------    
                     
            ---------       
    
    """
    
    def __init__(self, game):
        # set wall color
        # Call parent constructor, color black
        super().__init__(game, game.BLACK, game.FOREST)
        
        # set player size, position, speed
        self.player_props["size"] = [100, 10]
        # calculate center of screen
        bcx = self.b_size[0]/2
        bcy = self.b_size[1]/2
        # calculate player position off of screen center
        cx = bcx - self.player_props["size"][0]/2
        cy = bcy - self.player_props["size"][1]/2
        self.player_props["pos"] = [cx, cy]
        self.player_props["speed"] = 180
        self.player_props["accel"] = 1.2
        # set number of mice
        self.num_mice = 15
        # set number of mice required to finish
        self.mice_finish = 55
        # define walls [color, [x, y], [width, height]]
        self.walls_list.extend([
            [game.MAROON, [50, bcy-95], [self.b_size[0]-100, 20]],
            [game.MAROON, [50, bcy+75], [self.b_size[0]-100, 20]]
        ])


class Level_06(Level):
    """ Level 06:
        - Player:
            - long length
            - below center
            - speed of 180
            - acceleration of 3.6
        - 10 mice
        - 65 mice to finish
        - Wall layout:
                    
            ---------    
               ---         
            ---------       
    
    """
    
    def __init__(self, game):
        # set wall color
        # Call parent constructor, color black
        super().__init__(game, game.BLACK, game.BLUE)
        
        # set player size, position, speed
        self.player_props["size"] = [200, 10]
        # calculate player position off of screen center
        cx = self.bcx - self.player_props["size"][0]/2
        self.player_props["pos"] = [cx, self.b_size[1]-50]
        self.player_props["speed"] = 180
        self.player_props["accel"] = 3.6
        # set number of mice
        self.num_mice = 10
        # set number of mice required to finish
        self.mice_finish = 65
        # define walls [color, [x, y], [width, height]]
        self.walls_list.extend([
            [game.YELLOW, [100, self.bcy-95], [self.b_size[0]-200, 20]],
            [game.BLUE,   [250, self.bcy-10], [self.b_size[0]-500, 20]],
            [game.YELLOW, [100, self.bcy+75], [self.b_size[0]-200, 20]]
        ])


class Level_07(Level):
    """ Level 07:
        - Player:
            - short length
            - center
            - speed of 240
            - acceleration of 3.6
        - 10 mice
        - 70 mice to finish
        - Wall layout:
            
              ---    
            |     |    
              ---
    
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.NAVY, game.FOREST)
        
        # set player size, position, speed
        self.player_props["size"] = [40, 10]
        # calculate center of screen
        cx = self.bcx - self.player_props["size"][0]/2
        cy = self.bcy - self.player_props["size"][1]/2
        self.player_props["pos"] = [cx, cy]
        self.player_props["speed"] = 240
        self.player_props["accel"] = 3.6
        # set number of mice
        self.num_mice = 10
        # set number of mice required to finish
        self.mice_finish = 70
        # define walls [color, [x, y], [width, height]]
        self.walls_list.extend([
            [game.WHITE, [self.bcx-100, self.bcy-170], [200, 20]],
            [game.WHITE, [self.bcx+150, self.bcy-100], [20, 200]],
            [game.WHITE, [self.bcx-100, self.bcy+150], [200, 20]],
            [game.WHITE, [self.bcx-170, self.bcy-100], [20, 200]]
        ])


class Level_08(Level):
    """ Level 08:
        - Player:
            - standard length
            - bottom right corner
            - speed of 360
            - acceleration of 6.0
        - 10 mice
        - 30 mice to finish
        - Wall layout:
            
                |    
            ---   ---    
                |
    
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.NAVY, game.FOREST)
        
        # set player size, position, speed
        self.player_props["size"] = [100, 10]
        # place at bottom left corner
        px = self.b_size[0] - self.player_props["size"][0] - 30
        py = self.b_size[1] - self.player_props["size"][1] - 20
        self.player_props["pos"] = [px, py]
        self.player_props["speed"] = 360
        self.player_props["accel"] = 6.0
        # set number of mice
        self.num_mice = 10
        # set number of mice required to finish
        self.mice_finish = 30
        # define walls [color, [x, y], [width, height]]
        c = game.FOREST
        vl = (self.b_size[1]-220) // 2
        hl = (self.b_size[0]-220) // 2
        self.walls_list.extend([
            [c, [self.bcx-10, 0],            [20, vl]],
            [c, [self.bcx+110, self.bcy-10], [hl, 20]],
            [c, [self.bcx-10, self.bcy+110], [20, vl]],
            [c, [0, self.bcy-10],            [hl, 20]]
        ])


class Level_09(Level):
    """ Level 09:
        - Player:
            - standard length
            - center
            - speed of 240
            - acceleration of 2.4
        - 15 mice
        - 75 mice to finish
        - Wall layout:
            
            __  __  __      
           |          |
           |__  __  __|   
    
    """
    
    def __init__(self, game):
        # Call parent constructor, color black
        super().__init__(game, game.NAVY, game.MAROON)
        
        # set player size, position, speed
        self.player_props["size"] = [100, 10]
        # place at center
        px = self.bcx - self.player_props["size"][0]/2
        py = self.bcy - self.player_props["size"][1]/2
        self.player_props["pos"] = [px, py]
        self.player_props["speed"] = 240
        self.player_props["accel"] = 2.4
        # set number of mice
        self.num_mice = 15
        # set number of mice required to finish
        self.mice_finish = 75
        # define walls [color, [x, y], [width, height]]
        c = game.MAROON
        # use loops to create walls
        walls = []
        for i in range(6):
            a = i*100
            walls.append(    [c, [self.bcx-275+a, 75],                [50, 20]])
            walls.append(    [c, [self.bcx-275+a, self.b_size[1]-95], [50, 20]])
            # only four of these
            if i < 4:
                walls.append([c, [75, self.bcy-175+a],                [20, 50]])
                walls.append([c, [self.b_size[0]-95, self.bcy-175+a], [20, 50]])
        self.walls_list.extend(walls)
        
        