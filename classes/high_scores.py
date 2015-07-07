# import modules
import tkinter
from tkinter import ttk
import json
import os
# import classes

# define class
class HighScores(object):
    """ Reads, displays, updates, and writes high scores for a game.
    Inherits -- object
    """
    #Define basic colors
    BLACK   = (0x00, 0x00, 0x00)
    WHITE   = (0xFF, 0xFF, 0xFF)
    GREY    = (0xBB, 0xBB, 0xBB)
    
    max_scores = 15
    
    def __init__(self, location=False):
        """ Reads the high scores from the file at the specified location.
        location --     (str) (optional) The location of the high scores db
        """
        # Store location
        if location:
            self.filename = location
        else:
            self.filename = "data/scores.dat"
        # initialize window
        self.root = None
        self.open = False
        
        # open the high scores db
        file = open(self.filename, 'r')
        # parse the high scores db
        self.list = json.load(file)
        # close the db
        file.close()
    
    def add_score(self, name, score):
        """ Adds a score to the list.
        name --     (str) The name of the person who scored.
        score --    (int) The score to add.
        returns --  (None)
        """
        # append the score
        self.list.append([name, score])
        # sort the list
        self.list.sort(key=lambda v: v[1], reverse=True)
        # If we already have max scores
        if len(self.list) > self.max_scores:
            # remove the last (lowest) score
            self.list = self.list[:-1]
        # open the db
        file = open(self.filename, 'w')
        # write the new list
        json.dump(self.list, file)
        # close the db
        file.close()
    
    def get_game_window_pos(self):
        """ Attempts to get the position of the window of the parent game.
        returns --  (tuple) x, y coordinates of the window.
                            If we can't get the position, returns (0, 0)
        """
        """ PyGame uses the SDL library to display graphics.
            The following documentation reference the
            "SDL_VIDEO_WINDOW_POS" environment variable:
            http://www.pygame.org/wiki/SettingWindowPosition
        """
        if "SDL_VIDEO_WINDOW_POS" in os.environ:
            x, y = os.environ["SDL_VIDEO_WINDOW_POS"].split(", ")
            return (x, y)
        return (0, 0)
        
    def open_list(self, title=False):
        """ Opens and displays the high scores list in a Tk window.
        title --    (str) (optional) The title of the window
        returns --  (None)
        """
        # set title
        title = title if title else "High Scores"
        # get position of window
        win_pos = (500, 250)
        # set size of window
        win_size = (300, 450)
        
        # create high scores window
        self.root = tkinter.Tk()
        self.root.title(title)
        # formate geometry string for window
        win_geo = "{}x{}+{}+{}"\
                  .format(win_size[0], win_size[1], win_pos[0], win_pos[1])
        # set position and size of window
        self.root.geometry(win_geo)
        # lock window size
        self.root.resizable(False, False)
        
        # Create main high scores frame
        mframe = ttk.Frame(self.root,
            padding="10"
        )
        # Create content frame
        content = ttk.LabelFrame(mframe,
            text="High Scores",
            labelanchor="n",
            padding=(5),
            borderwidth=2,
            relief='sunken'
        )
        # Create options frame
        options = ttk.Frame(mframe,
            padding=5
        )
        # create cancel button
        cancel = ttk.Button(options,
            text="Cancel",
            default="active",
            command=self.close_list
        )   
        
        # Create base layout
        mframe.pack(
            fill="both"
        )
        content.pack(
            fill="x"
        )
        content.grid_propagate(False)
        content["height"] = win_size[1] - 100
        options.pack(
            fill="x",
            pady=(30, 0)
        )
        
        # Create high scores content
        for i in range(len(self.list)):
            score = self.list[i]
            ttk.Label(content, text=str(i+1) + ". ").grid(
                row=i,
                column=0,
                sticky=(tkinter.W),
                pady=1
            )
            ttk.Label(content, text=score[0]).grid(
                row=i,
                column=1,
                sticky=(tkinter.W),
                padx=(0, 10)
            )
            ttk.Label(content, text=score[1]).grid(
                row=i,
                column=2,
                sticky=(tkinter.W)
            )
        
        # Create options content
        cancel.pack()
        
        # Open the window
        self.root.mainloop()
        # We are now open
        self.open = True
    
    def close_list(self):
        """ Closes the high scores list.
        returns --  (None)
        """
        # Destroy the window
        self.root.destroy()
        # We are no longer open
        self.open = False
    
    def open_submit_score(self, score, title=False):
        """ Opens the submit score form in a Tk window.
        score --    (int) The score to submit
        title --    (str) (optional) The title of the window
        returns --  (None)
        """
        # set title
        title = title if title else "New High Score! Enter Your Name: "
        # get position of window
        win_pos = (500, 250)
        # set size of window
        win_size = (450, 150)
        
        # create high scores window
        self.root = tkinter.Tk()
        self.root.title(title)
        # formate geometry string for window
        win_geo = "{}x{}+{}+{}"\
                  .format(win_size[0], win_size[1], win_pos[0], win_pos[1])
        # set position and size of window
        self.root.geometry(win_geo)
        # lock window size
        self.root.resizable(False, False)
        
        # Create main frame
        mframe = ttk.Frame(self.root,
            padding="10"
        )
        # Create form
        label = ttk.Label(mframe,
            text="Congratulations, new high score! \
Enter your name below: "
        )
        #create input
        name = tkinter.StringVar()
        nameinput = ttk.Entry(mframe,
            width=50,
            textvariable=name
        )
        nameinput.insert(0, "Your Name Here")
        # Auto select entry
        nameinput.focus()
        nameinput.selection_range(0, tkinter.END)
        def submit_score(*args):
            # close the open window
            self.close_list()
            # add the score
            self.add_score(name.get(), score)
            # open the list
            self.open_list()
        submit = ttk.Button(mframe,
            text="Submit",
            default="active",
            command=submit_score
        )
        self.root.bind('<Return>', submit_score)

        # Layout
        mframe.grid(
            row=0,
            column=0
        )
        label.grid(
            row=0,
            column=0,
            padx=50,
            pady=10,
            sticky=(tkinter.W)
        )
        nameinput.grid(
            row=1,
            column=0
        )
        submit.grid(
            row=2,
            column=0
        )
        
        # open window
        self.root.mainloop()
        # we are now open
        self.open = True
        
        
    
    def check_high_score(self, score):
        """ Checks and sees if a score is high enough to be on the list.
        score --    (int) The score to check for placement.
        returns --  (none)
        """
        # The list should be sorted,
        # if the score is higher than the last item
        # Or if we aren't full of scores yet
        num = len(self.list)
        if score > self.list[num-1][1] or num < self.max_scores:
            # Then submit the score
            self.open_submit_score(score)
        
        