import pygame
from pygame.locals import *

import load
import Unit
import ProtossUnit
import Building
import ProtossBuildings


class player(object):
    def __init__(self, race, startRow, startCol):
        if race == 'Protoss':
            nexus = ProtossBuildings.Nexus(startRow,startCol)
            Building.building.addTofinishedBuildings(nexus)
            ProtossUnit.Probe(startRow,startCol-1)
            ProtossUnit.Probe(startRow-1,startCol-1)
            ProtossUnit.Probe(startRow+1,startCol-1)
            ProtossUnit.Probe(startRow+2,startCol-1)
            ProtossUnit.Probe(startRow+3,startCol-1)
            self.xPos = startCol - 10
            self.yPos = startRow - 10
            self.Units = ProtossUnit.ProtossUnit.ProtossUnits

            MenuFile = 'Other/Menu/Protoss Menu.png'
            self.MenuImage = load.load_image(MenuFile)

