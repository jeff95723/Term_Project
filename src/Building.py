import pygame
from pygame.locals import *

import load
import Menu

class building(object):
    buildings = []
    buildingBuildings = []
    finishedBuildings = []
    # the surfaces for buildings for each player
    Map = None
    mapSurface = None
    originalSurface = None

    @classmethod
    def getAllBuildings(cls):
        return building.buildings

    @classmethod
    def setMap(cls, Map):
        building.mapSurface=Map.image
        building.originalSurface = Map.original
        building.Map = Map
        building.screen = Map.display


    @classmethod
    def drawAllBuildings(cls):
        for bld in cls.buildings:
            if bld in cls.buildingBuildings:
                bld.drawUnfinishedBuilding()
            else:
                bld.drawBuilding()

    @classmethod
    def nextRound(cls):
        for bld in cls.buildings:
            bld.buildRound -= 1
            if bld.buildRound == 0:
                building.buildingBuildings.remove(bld)
                bld.undrawUnfinishedBuilding()
                building.finishedBuildings.append(bld)

    @classmethod
    def drawAllBuildingsOnMiniMap(cls):
        for bld in cls.buildings:
            for r in xrange(bld.sizeRow):
                for c in xrange(bld.sizeCol):
                    Menu.drawMiniMapCell(building.screen,bld.row+r, bld.col+c,(0,200,0))

    def __init__(self, row, col, sizeRow, sizeCol, imageName):
        self.row = row
        self.col = col
        self.sizeRow = sizeRow
        self.sizeCol = sizeCol
        self.image = load.load_image_smooth('Buildings/' + imageName, 1.5)
        self.Map = building.Map

        # set the x, y error for the image
        self.xerror = 10
        self.yerror = 0


        building.buildings.append(self)
        building.buildingBuildings.append(self)



    def __eq__(self, other):
        return type(self) == type(other) and (self.row,self.col) == (other.row,other.col)

    def drawBuilding(self):
        surface = building.mapSurface
        cellWidth, cellHeight = self.Map.getCellsize()
        x = cellWidth * self.col + self.xerror
        y = cellHeight * self.row + self.yerror
        surface.blit(self.image,(x,y))

        for r in xrange(self.sizeRow):
            for c in xrange(self.sizeCol):
                self.Map.board[self.row + r][self.col + c] = self

    def drawUnfinishedBuilding(self, unfinishedBuildingImage):
        surface = building.mapSurface
        cellWidth, cellHeight = self.Map.getCellsize()
        x = cellWidth * self.col
        y = cellHeight * self.row
        surface.blit(unfinishedBuildingImage,(x,y))

        for r in xrange(self.sizeRow):
            for c in xrange(self.sizeCol):
                self.Map.board[self.row + r][self.col + c] = self

    def undrawUnfinishedBuilding(self):
        '''Each building class for each race must implement this function'''
        pass

    def removeBuilding(self):
        building.buildings.remove(self)
        building.finishedBuildings.remove(self)
        for r in xrange(self.sizeRow):
            for c in xrange(self.sizeCol):
                self.Map.board[self.row + r][self.col + c] = 0
        self.undrawBuilding()


