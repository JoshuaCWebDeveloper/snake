# import modules
import pygame
import math
# import classes
from .messages import Text
# define class
class Panel(pygame.Surface):
    """ Represents an instance of the game panel.
    Inherits -- PyGame Surface class
    """
    
    def __init__(self, game):
        # run parent surface constructor
        super().__init__(game.PANEL_SIZE)
        
        # set the game reference
        self.game = game
    
    def draw (self, panel=False):
        """ Draws the game panel to display relevant info.
        panel --   (object -- pygame.Surface)   A surface to draw the panel on
                                                defaults to self
        returns -- (None)
        """
        # If we didn't receive an alternate panel surface
        if not panel:
            # then use our own surface
            panel = self
        # reference size for easy refernce
        size = self.game.PANEL_SIZE
        # get reference to level and messages
        level = self.game.get_level()
        msgs = self.game.messages
        # create default padding
        pad = 20
        # copy font color
        txt_color = self.game.colors["panel_text"]
        # create arial font
        arial = ["Arial", 16, True]
        # fill panel
        panel.fill(self.game.colors["panel"])
        # create score
        scr = msgs.render_text(
            "{{STRID|info001score}}: {0}".format(self.game.score), txt_color
        )
        # horizontally center score
        scr_cx = msgs.center(scr, size, True, False)
        # copy to panel, centered top
        panel.blit(scr, [scr_cx, 10])
        # create lives
        liv = msgs.render_text(
            "{{STRID|info005lives}}: {0}".format(self.game.lives),
            txt_color,
            arial
        )
        # copy to panel, top right corner
        panel.blit(liv, [size[0]-liv.get_width()-25, 15])
        # create surface to store level progress info
        progress_height = 20
        progress = pygame.Surface([500, progress_height])
        progress.fill(self.game.colors["panel"])
        # get number of mice, and mice needed to complete level
        num_mice = level.mice_count
        req_mice = level.mice_finish
        # Create progress bar
        prog_width = 425
        prog_bar = pygame.Surface([prog_width, progress_height])
        # If the level is NOT complete
        if not level.complete:
            # progress bar is not full, color grey
            prog_bar.fill(self.game.GREY)
            # Create yellow bar to show our progress so far
            # width is percentage of progress bar based on num_mice and req_mice
            percent_width = math.ceil(prog_width * (num_mice/req_mice))
            percent_bar = pygame.Surface([percent_width, progress_height])
            percent_bar.fill(self.game.YELLOW)
            # blit percent bar on top of empty progress bar
            prog_bar.blit(percent_bar, [0, 0])
        else:
            # level is complete, progress bar is full, color green
            prog_bar.fill(self.game.GREEN)
            # create level complete
            lvl_font = list(arial)
            lvl_font[1] = 18
            lvl_comp = msgs.render_text(
                "STRID|info003complete", self.game.BLACK, lvl_font
            )
            # horizontally center level complete
            lvl_cx = msgs.center(
                lvl_comp, [prog_width], True, False
            )
            # output level complete text to progress bar
            prog_bar.blit(lvl_comp, [lvl_cx, 0])
        # blit progress bar into progress surgace
        progress.blit(prog_bar, [0, 0])
        # Create mice count
        mce = msgs.render_text(
            "{0}/{1} {{STRID|info002mice}}".format(num_mice, req_mice),
            txt_color,
            arial
        )
        # output mice to progress
        progress.blit(mce, [prog_width+10, 2])
        # output progress to panel, bottom left corner
        panel.blit(progress, [pad, size[1]-progress_height-pad])
        # if the level is complete
        if level.complete:
            # create bonus mode
            bonus = msgs.render_text("STRID|info004bonus", self.game.RED, arial)
            # output bonus to panel, bottom right corner
            panel.blit(
                bonus,
                [
                    size[0] - bonus.get_width() - pad,
                    size[1] - bonus.get_height() - pad
                ]
            )
        # output bottom border to panel
        border = pygame.Surface([size[0], 5])
        panel.blit(border, [0, size[1]-5])
    