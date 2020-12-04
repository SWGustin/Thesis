import viewer_config 

config_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + config_file_name

class Display:
    
    def __init__(self, arpel=None):
        self._arrowLength = config.maxArrowLength
        self._arrowWidth = config.arrowWidth
        self._onColour = config.onColour
        self._offColour = config.offColour 
        self._arpel = arpel

    def _drawWing(self):
        pass

    def _drawPEl(self):
        pass        

    def update(self):
        self.wn.update()