# import other modules
import xml.etree.ElementTree as ET
# store strings in dict
_strings = {}
# create class
class Text(object):
    """ Module that handles fetching and outputting text for the game. """
    
    def load():
        """ Loads the strings for our game and stores them in memory. """
        # load the strings from the xml file
        tree = ET.parse('data/strings.xml')
        strs = tree.getroot()
        # loop through the strings
        for s in strs:
            # if this string has an id
            if "id" in s.attrib:
                # store the string in the dictionary
                _strings[s.attrib["id"]] = s.text
    
    def get_string(strid):
        """ Gets a string by its id.
        strid --    (string) The id of the string
        returns --  (string)    The string that matches the id,
                                an empty string if id not found
        """
        if strid in _strings:
            return _strings[strid]
        return ""
    