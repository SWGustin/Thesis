import pygame
import viewer_config 

class Display:
    def __init__(self, arpel=None):
        self._arrowLength = config.maxArrowLength
        self._arrowWidth = config.arrowWidth
        self._onColour = config.onColour
        self._offColour = config.offColour 
        self._arpel = arpel

        pygame.init()
        self.display = pygame.display.set_mode(config.screenSize)
        #self.display.title(config.displayTitle)
        self.display.fill(config.bgColour)

    def _drawWing(self):
        pygame.draw.polygon(screen,(200,200,200),self._arpel.geometry)
        pygame.display.update()    

    def _drawPEl(self):
        pass        

    def update(self):
        self.wn.update()