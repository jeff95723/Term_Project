import pygame
from pygame.locals import *

import load
import Menu
import time

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
        # fog of war
            inSight = bld.checkSight(10)
            for (r,c) in inSight:
                bld.Map.fogOfWarBoard[r][c] = 1

            for row in xrange(bld.sizeRow):
                for col in xrange(bld.sizeCol):
                    bld.Map.fogOfWarBoard[bld.row+row][bld.col+col] = 1

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
            if bld.buildQueue != []:
                bld.currentBuildRoundLeft[-1] -= 1
                if bld.currentBuildRoundLeft[-1] == 0:
                    bld.build(bld.buildQueue[-1])
                    bld.buildQueue = bld.buildQueue[:-1]
                    bld.currentBuildRoundLeft = bld.currentBuildRoundLeft[:-1]

    @classmethod
    def drawAllBuildingsOnMiniMap(cls):
        for bld in cls.buildings:
            for r in xrange(bld.sizeRow):
                for c in xrange(bld.sizeCol):
                    Menu.drawMiniMapCell(building.screen,bld.row+r, bld.col+c,(0,200,0))

    def __init__(self, row, col, sizeRow, sizeCol, health, sheild, healthRegen, sheildRegen, imageName):
        self.row = row
        self.col = col
        self.sizeRow = sizeRow
        self.sizeCol = sizeCol
        self.image = load.load_image_smooth('Buildings/' + imageName, 1.5)
        self.Map = building.Map

        self.health = health
        self.CURhealth = health
        self.sheild = sheild
        self.CURsheild = sheild
        # set the x, y error for the image
        self.xerror = 10
        self.yerror = 0

        self.Build = [ ]
        self.BuildSize = []
        self.BuildRound = []
        self.buildQueue = []
        self.currentBuildRoundLeft = []

        building.buildings.append(self)
        building.buildingBuildings.append(self)

    def __eq__(self, other):
        return type(self) == type(other) and (self.row,self.col) == (other.row,other.col)

    def checkSight(self,range):
        inSight = []
        board = self.Map.board
        rows, cols = len(board), len(board[0])
        uRow, uCol = self.row, self.col
        for row in xrange(max(0,uRow-range-1),min(uRow+range+1,rows)+1):
            for col in xrange(max(0,uCol - range-1),min(uCol+range+1,cols)+1):
                if abs(row-uRow)+abs(col-uCol) <= range:
                    for r in xrange(self.sizeRow):
                        for c in xrange(self.sizeCol):
                            inSight.append((row+r,col+c))
        inSight = list(set(inSight))
        return inSight

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

    def addQueue(self,index):
        self.buildQueue.append(index)
        self.currentBuildRoundLeft.append(self.BuildRound[index])

    def build(self,index):
        buildSizeRow, buildSizeCol = self.BuildSize[index]
        if self.getBuildingBorder(buildSizeRow,buildSizeCol) != []:
            result = self.Build[index](self.getBuildingBorder(buildSizeRow,buildSizeCol)[0][0],
                                          self.getBuildingBorder(buildSizeRow,buildSizeCol)[0][1])

    def getBuildingBorder(self, sizeRow, sizeCol):
        result = []
        board = self.Map.board
        originR, originC = self.row, self.col
        edgeR, edgeC = self.row + self.sizeRow, self.col+self.sizeCol
        rows, cols = len(board), len(board[0])
        for r in xrange(max(0,originR-sizeRow), min(edgeR+sizeRow,rows)):
            for c in xrange(max(0,originC-sizeCol),min(edgeC+sizeCol,cols)):
                for sr in xrange(sizeRow):
                    for sc in xrange(sizeCol):
                        if board[r+sr][c+sc] == 0:
                            result.append((r,c))
        return result

        pass

    def die(self):
        time.sleep(1)
        self.playSound(self.deathSound)
        building.buildings.remove(self)


