# Import modules
import pygame, math, os, sys
# Import classes
from .events import Events
from .panel import Panel
from .levels import *
from .messages import Messages
from .high_scores import HighScores

class Game(object):
    """ Represents instance of the game.
    A new game can be created by creating a new instance of this class.
    """
    
    #Define basic colors
    BLACK   = (0x00, 0x00, 0x00)
    WHITE   = (0xFF, 0xFF, 0xFF)
    RED     = (0xFF, 0x00, 0x00)
    GREEN   = (0x00, 0xFF, 0x00)
    BLUE    = (0x00, 0x00, 0xFF)
    YELLOW  = (0xFF, 0xFF, 0x00)
    MAGENTA = (0xFF, 0x00, 0xFF)
    CYAN    = (0x00, 0xFF, 0xFF)
    GREY    = (0xDD, 0xDD, 0xDD)
    MAROON  = (0x80, 0x00, 0x00)
    FOREST  = (0x00, 0x80, 0x00)
    NAVY    = (0x00, 0x00, 0x80)
    # Define Pi
    PI = math.pi
    # Define window size and structure
    WINDOW_SIZE = (700, 600)
    PANEL_SIZE = (700, 100)
    PANEL_POS = (0, 0)
    BOARD_SIZE = (700, 500)
    BOARD_POS = (0, 100)
    
    # Define default values
    defaults = {
        "fps": 60,
    }
    
    def __init__ (self, title, pygclock=False, fps=False):
        """
        title --    (str) Used to title game window
        fps --      (int) Frames per second (.g. speed) of the game
        pygclock -- (object -- pygame.time.Clock) Used for setting the FPS
        """
        # set and store current working directory
        os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
        self.cwd = os.getcwd()
        self.title = title
        # If we weren't given a clock
        if pygclock is False:
            # create a new clock
            self.clock = pygame.time.Clock()
        else:
            self.clock = pygclock
        # If we weren't passed FPS
        if fps is False:
            self.fps = self.defaults["fps"]
        else:
            self.fps = fps
        # create events object for the game
        self.events = Events()
        # set score and lives to 0
        self.score = 0
        self.lives = 0
        # create dictionary to store colors
        self.colors = {}
        # game is not currently running
        self.screen = False
        self.running = False
        self.game_over = True
        # initiate levels
        self.current_level = False
        self.levels = []
        # add event listeners
        self.setup_events()
        # initialize messages
        self.messages = Messages(self)
        # initialize high scores list
        self.high_scores = HighScores(self.cwd+'/')
        # initialize structure
        self.board = False
        self.panel = False
    
    def setup_events (self):
        # Add event listeners
        # Move player
        @self.events.listener(pygame.KEYDOWN)
        def e_handle_move(e):
            if not self.game_over and not self.paused:
                if e.key == pygame.K_LEFT:
                    self.get_level().player.move_left()
                if e.key == pygame.K_RIGHT:
                    self.get_level().player.move_right()
                if e.key == pygame.K_UP:
                    self.get_level().player.move_up()
                if e.key == pygame.K_DOWN:
                    self.get_level().player.move_down()
        # Handle pause and restart
        @self.events.listener(pygame.KEYDOWN)
        def e_handle_pause_restart(e):
            # If space was pressed
            if e.key == pygame.K_SPACE:
                # Restart when game over
                if self.game_over:
                    self.restart()
                # Un-pause game when paused
                if self.paused:
                    self.paused = False
            # If game isn't paused, and 'p' was pressed
            if not self.paused and e.key == pygame.K_p:
                # pause game
                self.paused = True
        # Exit game on close
        @self.events.listener(pygame.QUIT)
        def e_handle_exit(e):
            # Exit main program loop
            self.stop()
        
    def get_title (self):
        """ Get the game title
        returns -- (str)
        """
        return self.title
        
    def get_score (self):
        """ Get the game score
        returns -- (int)
        """
        return self.score
        
    def get_level(self):
        """ Get the current level in the list of levels
        returns -- (object Level) The current level
        """
        return self.levels[self.current_level]
    
    def is_running(self):
        """ Check if loop is still active
        returns -- (bool)
        """
        return self.running
    
    def add_points(self, points):
        """ Add points to score
        points --   (int) The points to add
        return --   (int) The new score
        """
        self.score += int(points)
        return self.get_score()
    
    def load (self):
        """ Opens a window and loads resources for game.
        size --     (list) The width, height of the game window
        returns --  (bool) Whether or not load was successful
        """
        # start game
        self.game_over = False
        self.paused = True
        # Reset score and lives
        self.score = 0
        self.lives = 0
        # set game colors
        self.colors.update({
            "fill": self.BLACK,
            "game_text": self.WHITE,
            "text": self.BLACK,
            "text_fill": self.WHITE,
            "panel": self.BLUE,
            "panel_text": self.WHITE
        })
        
        # Create structure
        self.board = pygame.Surface(self.BOARD_SIZE)
        self.panel = Panel(self)
        # Create levels
        self.levels = [
            Level_01(self), Level_02(self), Level_03(self), Level_04(self),
            Level_05(self), Level_06(self), Level_07(self), Level_08(self),
            Level_09(self)
        ]
        # Load level 1
        self.current_level = 0
        self.get_level().load()
             
        # set title
        pygame.display.set_caption(self.title)
        # create dispaly (open window)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        # hide mouse
        pygame.mouse.set_visible(False)
        # game is now running
        self.running = True
        
    def level_up(self):
        """ Progress by one level.
        returns --  (none)
        """
        # If there is no next level
        if self.current_level >= len(self.levels) - 1:
            # All levels are complete, game over
            self.end()
            return
        # draw message
        message = self.messages.draw_level_complete()
        # draw level
        self.get_level().draw(self.board)
        # Fade out level, don't fade message
        self.fade_out([self.board], [message], 4)
        # Pause game
        self.paused = True
        # Update level
        self.current_level += 1
        # Load new level
        self.get_level().load()
        # Update panel
        self.panel.draw()
        self.screen.blit(self.panel, self.PANEL_POS)
        # draw and fade in new level
        self.get_level().draw(self.board)
        self.fade_in([self.board], [message], 1)
                
    def process_events (self):
        """ Processes all of the in game events.
        returns --  (none)
        """
        # Get and loop PyGame events
        for event in pygame.event.get():
            # Call the handler for the event
            # (If no handler exists, nothing will be done)
            self.events.handle(event.type, event)
            
    def run_logic (self):
        """ Execute any game logic (e.g. object positions, player attributes)
        returns --  (none)
        """
        # If the game isn't over and isn't paused
        if not self.game_over and not self.paused:
            # update level
            self.get_level().update()
        
    def display_frame (self):
        """ Display all the graphics in this frame
        fill --     (list) Screen fill (background) color in RGB values
        returns --  (none)
        """
        # draw panel
        self.panel.draw()
        
        # If the game is NOT over
        if not self.game_over:
            # draw level
            self.get_level().draw(self.board)
            # If the game is paused
            if self.paused:
                # draw a pause message to a screen
                self.board.blit(self.messages.draw_paused(), [0, 0])
        else:
            # create game over message
            message = self.messages.draw_game_over()
            self.board.blit(message, [0, 0])
        
        # Fill the screen with fill color
        self.screen.fill(self.colors["fill"])
        # Blit panel and board to screen
        self.screen.blit(self.panel, self.PANEL_POS)
        self.screen.blit(self.board, self.BOARD_POS)
        
        # update the graphics
        pygame.display.flip()
        
    def _fade(self, fades=[], direction="out", noFades=[], speed=1.5):
        """ Take a PyGame Surface and slowly fade it in or out.
        This runs an internal game loop for the duration of the fade.
        fades --     (list) A list of PyGame surfaces to fade
        direction -- (str) "in" or "out" (If not "in", assumes "out")
        noFades --   (list) A list of PyGame surfaces that don't fade
        speed --     (float) The number of seconds for the fade to last
        returns --  (none)
        """
        # Create surfaces to store graphics
        fade = pygame.Surface(self.BOARD_SIZE)
        noFade = pygame.Surface(self.BOARD_SIZE)
        # Make fade transparent
        fade.fill(self.BLACK)
        fade.set_colorkey(self.BLACK)
        # add fades to fade surface
        for s in fades:
            fade.blit(s, [0, 0])
        # add no fades to noFade surface
        for s in noFades:
            noFade.blit(s, [0, 0])
        # Calculate number of frames for the fade to last
        frames = math.ceil(speed * self.fps)
        # Calculate how to spread 255 over our number of frames
        step = 255/frames
        # Iterate for each frame
        # -- Start internal game loop --
        for i in range(0, frames):
            # Determine our current alpha for this frame based on step
            a = math.ceil(i * step)
            # Set alpha (fade in our out)
            alpha = (0 + a) if direction == "in" else (255 - a) 
            # Set fade level for fade surface
            fade.set_alpha(alpha)
            # Fill the board with fill color
            self.board.fill(self.colors["fill"])
            # Copy surfaces to screen
            self.board.blit(noFade, [0, 0])
            self.board.blit(fade, [0, 0])
            self.screen.blit(self.board, self.BOARD_POS)
            # update graphics
            pygame.display.flip()
            # tick clock
            self.update_clock()
    
    def fade_in(self, fades=[], noFades=[], speed=1.5):
        """ Take a PyGame Surface and slowly fade it in.
        args -- fades(list), noFades(list), speed(int) See Game._fade docstring.
        returns --  (none)
        """
        # Use internal fade method, uses internal game loop
        self._fade(fades, "in", noFades, speed)
        
    def fade_out(self, fades=[], noFades=[], speed=1.5):
        """ Take a PyGame Surface and slowly fade it out.
        args -- fades(list), noFades(list), speed(int) See Game._fade docstring.
        returns --  (none)
        """
        # Use internal fade method, uses internal game loop
        self._fade(fades, "out", noFades, speed)
        
    def update_clock (self):
        """ Updates the PyGame clock and delays loop to maintain max FPS
        returns -- (none)
        """
        self.clock.tick(self.fps)
    
    def end (self):
        """ Ends the current game and displays game over message. """
        # Game is now over
        self.game_over = True
        # draw message
        message = self.messages.draw_game_over()
        # draw and fade out level
        level = pygame.Surface(self.BOARD_SIZE)
        self.get_level().draw(level)
        self.fade_out([level])
        # fade in message
        self.fade_in([message])
        # Check high scores
        self.high_scores.check_high_score(self.score)
        
    def restart (self):
        # Reload game
        self.load()
    
    def stop (self):
        """ Stop the game """
        self.running = False
