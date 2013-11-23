import pygame
from pygame.locals import *

import load

class building(object):
    buildings = []
    buildingBuildings = []
    finishedBuildings = []
    # the surfaces for buildings for each player
    buildingSurfaces = []

    @classmethod
    def getAllBuildings(cls):
        return building.buildings

    @classmethod
    def addBuildingSurface(cls, surface):
        building.buildingSurfaces.append(surface)

    @classmethod
    def drawAllBuildings(cls, buildingSurfaceIndex):
        '''BUG HERE'''
        for bld in cls.buildings:
            if bld in cls.buildingBuildings:
                bld.drawUnfinishedBuilding(0)
            else:
                bld.drawBuilding(0)

    @classmethod
    def nextRound(cls):
        for bld in cls.buildings:
            bld.buildRound -= 1
            if bld.buildRound == 0:
                building.buildingBuildings.remove(bld)
                building.finishedBuildings.append(bld)

    def __init__(self, row, col, sizeRow, sizeCol,imageName, Map):
        self.row = row
        self.col = col
        self.sizeRow = sizeRow
        self.sizeCol = sizeCol
        self.image = load.load_image_smooth('Buildings/' + imageName, 1.5)
        self.Map = Map

        # set the x, y error for the image
        self.xerror = 10
        self.yerror = 0
        building.buildings.append(self)
        building.buildingBuildings.append(self)

    def __eq__(self, other):
        return type(self) == type(other) and (self.row,self.col) == (other.row,other.col)

    def drawBuilding(self, buildingSurfaceIndex):
        surface = building.buildingSurfaces[buildingSurfaceIndex]
        cellWidth, cellHeight = self.Map.getCellsize()
        x = cellWidth * self.col + self.xerror
        y = cellHeight * self.row + self.yerror
        surface.blit(self.image,(x,y))

        for r in xrange(self.sizeRow):
            for c in xrange(self.sizeCol):
                self.Map.board[self.row + r][self.col + c] = 1

    def drawUnfinishedBuilding(self, buildingSurfaceIndex, unfinishedBuildingImage):
        surface = building.buildingSurfaces[buildingSurfaceIndex]
        cellWidth, cellHeight = self.Map.getCellsize()
        x = cellWidth * self.col + self.xerror
        y = cellHeight * self.row + self.yerror
        surface.blit(unfinishedBuildingImage,(x,y))

        for r in xrange(self.sizeRow):
            for c in xrange(self.sizeCol):
                self.Map.board[self.row + r][self.col + c] = 1

