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
        self.resources = 50
        if race == 'Protoss':
            nexus = ProtossBuildings.Nexus(startRow,startCol)
            Building.building.addTofinishedBuildings(nexus)
            ProtossUnit.Probe(startRow,startCol-1)
            ProtossUnit.Probe(startRow-1,startCol-1)
            ProtossUnit.Probe(startRow+1,startCol-1)
            ProtossUnit.Probe(startRow+2,startCol-1)
            ProtossUnit.Probe(startRow+3,startCol-1)
            self.xPos = 0
            self.yPos = 0
            self.Units = ProtossUnit.ProtossUnit.ProtossUnits
            self.Buildings = ProtossBuildings.ProtossBuilding.protossBuildings
            self.UntCls = ProtossUnit.ProtossUnit
            self.BldCls = ProtossBuildings.ProtossBuilding

            self.NoMineralSound = load.load_sound('Protoss/PAdErr00.wav')

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
            self.xPos = 0
            self.yPos = 0
            self.Units = TerranUnit.TerranUnit.TerranUnits
            self.Buildings = TerranBuildings.TerranBuilding.terranBuildings

            self.UntCls = TerranUnit.TerranUnit
            self.BldCls = TerranBuildings.TerranBuilding

            self.NoMineralSound = load.load_sound('Terran/tadErr00.wav')

            MenuFile = 'Other/Menu/Terran Menu.png'
            self.MenuImage = load.load_image(MenuFile)

    def drawFogOfWar(self):
        self.UntCls.drawFogOfWarBoard(self.index)
        self.BldCls.drawFogOfWarBoard(self.index)

    def getHarvesterCount(self):
        count = 0
        for unt in self.Units:
            if unt.canBuild:
                count += 1

        return count

    def addResources(self):
        count = self.getHarvesterCount()
        self.resources += count * 5

    def playSound(self,sound):
        sound.play()



