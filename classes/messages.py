# import modules
import pygame
from .text import Text
# create class
class Messages (object):
    """ Class for creating in-game messages. """
    
    def __init__(self, game):
        # store the game
        self.game = game
        # create default font
        self.font = pygame.font.SysFont("serif", 25)
        # Load the text for the game
        Text.load()
    
    def render_text (self, txt, color, font=False):
        """ Creates a PyGame surface with the text rendered on it
        txt --      (string) The text to render, may be a string or a STRID|
        color --    (color) The color of the text
        font --     (list)  The typeface, size of the font, default serif, 25
                            May contain optional third, and fourth items
                            specifying bold, italic as boolean flags
        returns --  (object -- pygame.Surface) A surface with the rendered text
        """
        # if we received a custom font
        if font:
            # default bold and italic
            b = i = False
            # if we received a third argument
            if len(font) > 2:
                b = font[2]
            # if we received a fourth argument
            if len(font) > 3:
                i = font[3]
            # create custom font
            font = pygame.font.SysFont(font[0], font[1], b, i)
        else:
            # use default font
            font = self.font
        # if we received a string id in our text
        if 'STRID|' in txt:
            # if our entire text is a string id
            if txt.startswith('STRID|'):
                # replace our string id with the loaded string
                txt = Text.get_string(txt[6:])
            else:
                # loop through all roperly bracketed string ids in our text
                while '{STRID|' in txt:
                    # get begining of id
                    start = txt.index('{STRID|')
                    # get end of id
                    end = txt[start:].find('}')
                    # if our id is properly closed
                    if end >= 0:
                        # replace our string id with the loaded string
                        txt = txt.replace(txt[start:start+end+1], Text.get_string(txt[start+7:start+end]), 1)
                    else:
                        # We can't fetch the string, remove id opening
                        txt = txt.replace(txt[start:start+7], '', 1)
        # render the text
        rendered = font.render(txt, True, color)
        return rendered

    def center (self, msg, size, center_x=True, center_y=True):
        """ Centers the message in the container
        msg --      (object -- pygame.Surface) The message to center
        size --     (list) The w, h of the container to center the message in
        center_x -- (bool) Whether to horizontally center the message
        center_y -- (bool) Whether to vertically center the message
        returns --  (tuple) The x, y coordinates of the centered message
                    (int) When only center_x or center_y returns the single value
        """
        cx = cy = 0
        # If we are to horizontally center
        if center_x:
            cx = (size[0] // 2) - (msg.get_width() // 2)
            # If we are only horizontally centering
            if not center_y:
                return cx
        # If we are to vertically center
        if center_y:
            cy = (size[1] // 2) - (msg.get_height() // 2)
            # If we are only vertically centering
            if not center_x:
                return cy
        # We are centering both or neither, return both
        return (cx, cy)
    
    def _draw_game_overlay (self, txt):
        """ Creates a message with a transparent background
            and white color that displays over the game
        txt --      (string) The text to render
        returns --  (object -- pygame.Surface) The rendered text
        """
        # Create surface
        surface = pygame.Surface(self.game.BOARD_SIZE)
        # make background transparent
        surface.fill(self.game.BLACK)
        surface.set_colorkey(self.game.BLACK)
        # render text
        rendered = self.render_text(txt, self.game.colors["game_text"])
        # center
        center = self.center(rendered, self.game.BOARD_SIZE)
        # output
        surface.blit(rendered, center)
        return surface
    
    def draw_game_over(self):
        """ Creates the game over message as a PyGame surface.
        returns --  (object -- pygame.Surface)
        """
        # Create surface
        message = pygame.Surface(self.game.BOARD_SIZE)
        # Fill with text fill color
        message.fill(self.game.colors["text_fill"])
        # Create game over message
        txt = self.render_text('STRID|play003gameover', self.game.colors["text"])
        center = self.center(txt, self.game.BOARD_SIZE)
        message.blit(txt, [center[0], center[1] - 50])
        # output score
        score_txt = self.render_text(
            "{{STRID|info001score}}: {0}".format(self.game.score),
            self.game.colors["text"]
        )
        cent_s = self.center(score_txt, self.game.BOARD_SIZE, True, False)
        message.blit(score_txt, [cent_s, center[1]+50])
        return message
            
    def draw_paused (self):
        # Use game overlay to draw paused message
        return self._draw_game_overlay('STRID|play001continue')
        
    def draw_level_complete (self):
        # Use game overlay to draw level up message
        return self._draw_game_overlay('STRID|play002levelup')
        