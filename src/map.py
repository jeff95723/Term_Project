import pygame
from pygame.locals import *

import load
import Menu

class map(object):

    def __init__(self, mapName, rows, cols, scale):
        self.image = load.load_image_smooth(fileName = 'maps/%s.jpg' %mapName, scale = scale)
        self.original= load.load_image_smooth(fileName = 'maps/%s.jpg' %mapName, scale = scale)
        self.mini_map = load.load_image_smooth(fileName = 'maps/%s.jpg' %mapName, scale = 1.0/16)
        self.board = load.load_map_data(fileName = mapName + '.txt')
        self.rows = rows
        self.cols = cols
        self.fogOfWarBoard = [[0] * cols for row in xrange(rows)]
        self.x = 0
        self.y = 0
        self.rect = pygame.Surface.get_rect(self.image)
        self.width,self.height = pygame.Surface.get_size(self.image)
        self.scale = scale
        self.display = pygame.display.get_surface()
        self.displayWidth, self.displayHeight = pygame.Surface.get_size(self.display)

    def draw(self, mainScreen):
        mainScreen.blit(self.image,(0,0),(abs(self.x),abs(self.y),self.displayWidth, self.displayHeight))

    def drawFogOfWarOnMiniMap(self,mainScreen):
        rows, cols = len(self.fogOfWarBoard), len(self.fogOfWarBoard[0])
        fogBlack = (1,1,1,250)
        for row in xrange(rows):
            for col in xrange(cols):
                if self.fogOfWarBoard[row][col] == 0:
                    Menu.drawMiniMapCell(mainScreen,row,col,fogBlack)

    def resetFogOfWarBoard(self):
        self.fogOfWarBoard = [[0] * self.cols for row in xrange(self.rows)]

    def drawFogOfWar(self,mainScreen):
        cW, cH = self.getCellsize()
        onScreenRow, onScreenCol = abs(self.y)/cH, abs(self.x)/cW
        screenRows, screenCols = self.displayHeight/cH, self.displayWidth/cW
        fogBlack = (1,1,1,250)
        fogCell = pygame.Surface((cW,cH),pygame.SRCALPHA)
        fogCell.fill(fogBlack)
        for row in xrange(onScreenRow,onScreenRow+screenRows):
            for col in xrange(onScreenCol, onScreenCol+screenCols):
                if self.fogOfWarBoard[row][col] == 0:
                    localRow = row - onScreenRow
                    localCol = col - onScreenCol
                    mainScreen.blit(fogCell,(localCol*cW,localRow*cH))


    def move(self,(dx,dy)):
        self.x += dx
        self.y += dy
        if self.x > 0:
            self.x = 0
        elif self.x < -self.width + self.displayWidth:
            self.x = -self.width + self.displayWidth
        if self.y > 0:
            self.y = 0
        if self.y < -self.height + self.displayHeight:
           self.y = -self.height + self.displayHeight

    def getCellsize(self):
        return (self.width/self.cols, self.height/self.rows)

    def drawBlock(self,row, col, color):
        cW, cH = self.getCellsize()
        block = pygame.Surface((cW,cH),pygame.SRCALPHA)
        block.fill(color)
        self.image.blit(block,(col*cW, row*cH))
        #pygame.draw.rect(self.image,color,(col*cW,row*cH,cW, cH))

    def undrawBlock(self,row,col):
        cW, cH = self.getCellsize()
        self.image.blit(self.original,(col*cW,row*cH),pygame.Rect(col*cW,row*cH,cW,cH))

    def drawGrid(self):

        rows, cols = self.rows, self.cols
        cW, cH = self.getCellsize()
        for row in xrange(rows):
            pygame.draw.lines(self.image, (0,0,0),False, [(0,row * cH),(self.width,row * cH)])
        for col in xrange(cols):
            pygame.draw.lines(self.image, (0,0,0),False, [(col * cW, 0),(col * cW, self.height)])

    def resetMap(self):

        self.image.blit(self.original,(abs(self.x),abs(self.y)), (abs(self.x),abs(self.y), self.displayWidth, self.displayHeight))


