# Import modules
import pygame

# Import classes
from classes.game import Game

def main ():
    # Initialize PyGame
    pygame.init()
    # Instantiate game
    game = Game ("Snake")
    # Load game
    game.load()
    
    # ------ Main Program Loop ------
    while game.is_running():
        # Process events (e.g. keystrokes, mouseclicks)
        game.process_events()
        # Run game logic (e.g. object positions, player attributes)
        game.run_logic()
        # Draw the current frame (e.g. the graphics)
        game.display_frame()
        # Pause until next frame
        game.update_clock()

    # Once the main program loop has stopped (program finished running),
    # Close all open windows
    pygame.quit()

if __name__ == '__main__':
    main()