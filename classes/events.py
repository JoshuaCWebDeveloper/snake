# define event class
class Event(object):
    """ Creates handler functionality for an event
        Holds multiple listeners to be executed when an event is triggered
    """
        
    def __init__ (self, e_type, listeners=False):
        #set event type and listeners
        self.e_type = e_type
        #If we received a list
        if isinstance(listeners, list):
            self.listeners = listeners
        # Else, if no listeners were passed
        elif listeners is False:
            # default value
            self.listeners = []
        else:
            TypeError("Event arg listeners not instance of list")
     
    def handle (self, e_obj):
        """Executes event listeners
        e_obj --    (e_obj) An event object to pass to
                            each individual listener
        returns --  (none)
        """
        for func in self.listeners:
            #If func is callable
            if callable(func):
                #Pass the event
                func(e_obj)
    
    def add_listener (self, listener):
        """ Adds an event listener
        listener -- (callable) The listener to be called on an event
        returns --  (bool) Whether or not listener was added
        """
        #If listener is callable
        if callable(listener):
            # Add
            self.listeners.append(listener)
            return True
        else:
            TypeError("Event.add_listener arg listener is not callable")
            return False


# define events class
class Events(object):
    """ Represents all the events for a particular
        object (e.g. window, game, process).
        Holds all the event handlers for each event
    """
    
    def __init__(self):
        # create dictionary to store event handlers
        self.event_handlers = {}
        
    
    def add(self, event):
        """ Creates an event handler for an event.
        event --    (mixed) An identifier for an event (typically int).
                            Must be hashable.
        returns --  (none)
        """
        # If the event handler hasn't already been created
        if event not in self.event_handlers:
            # Then create and add it now
            self.event_handlers[event] = Event (event)
    
    def listener(self, event):
        """ Creates a decorator to add an event listener to an event.
        event --    (mixed) An identifier for an event (typically int).
                            Must be hashable.
        returns --  (callable)  The decorator that will accpet an event listener
                                and will return the same event listener.
        """
        # Make sure the event has been added
        self.add(event)
        # Define decorator
        def listen(func):
            # Add listener to event
            self.event_handlers[event].add_listener(func)
            return func
        return listen
    
    def handle (self, e_type, e_obj):
        """ Executes an event handler if it exists. If it doesn't, do nothing.
        e_type --   (mixed) An identifier for an event (typically int).
                            Must be hashable.
        e_obj --    (e_obj) An event object to pass to
                            each individual listener
        returns --  (none)
        """
        # If we have a handler for this event
        if e_type in self.event_handlers:
            # Handle the event
            self.event_handlers[e_type].handle(e_obj)
    
    