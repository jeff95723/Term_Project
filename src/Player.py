import pygame
from pygame.locals import *

import load
import Unit
import ProtossUnit
import TerranUnit
import Building
import ProtossBuildings
import TerranBuildings


class player(object):
    def __init__(self, race, startRow, startCol,index):
        self.index = index
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
            self.UntCls = ProtossUnit.ProtossUnit
            self.BldCls = ProtossBuildings.ProtossBuilding

            MenuFile = 'Other/Menu/Protoss Menu.png'
            self.MenuImage = load.load_image(MenuFile)
        if race == 'Terran':
            cc = TerranBuildings.CommandCenter(startRow,startCol)
            Building.building.addTofinishedBuildings(cc)
            TerranUnit.SCV(startRow,startCol-1)
            TerranUnit.SCV(startRow-1,startCol-1)
            TerranUnit.SCV(startRow+1,startCol-1)
            TerranUnit.SCV(startRow+2,startCol-1)
            TerranUnit.SCV(startRow+3,startCol-1)
            self.xPos = startCol - 10
            self.yPos = startRow - 10
            self.Units = ProtossUnit.ProtossUnit.ProtossUnits

            self.UntCls = TerranUnit.TerranUnit
            self.BldCls = TerranBuildings.TerranBuilding

            MenuFile = 'Other/Menu/Terran Menu.png'
            self.MenuImage = load.load_image(MenuFile)

    def drawFogOfWar(self):
        self.UntCls.drawFogOfWarBoard(self.index)
        self.BldCls.drawFogOfWarBoard(self.index)

