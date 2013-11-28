import pygame
from pygame.locals import *
import load
import random
import Menu

class Unit(object):
    Units = []
    Drawed = False
    Map = None
    mapSurface = None
    originalSurface = None
    screen = None

    @classmethod
    def getUnits(cls):
        return Unit.Units

    @classmethod
    def setMap(cls, Map):
        cls.Map = Map
        cls.mapSurface = Map.image
        cls.originalSurface = Map.original

    @classmethod
    def setScreen(cls,screen):
        cls.screen = screen

    @classmethod
    def nextRound(cls):
        for unt in cls.Units:
            unt.canMove = True
        Unit.Drawed = False


    @classmethod
    def drawAllUnits(cls):
        for unt in cls.Units:
            unt.drawUnit()

    @classmethod
    def drawAllUnitsOnMiniMap(cls):
        for unt in cls.Units:
            for r in xrange(unt.sizeRow):
                for c in xrange(unt.sizeCol):
                    Menu.drawMiniMapCell(Unit.screen,unt.row+r, unt.col+c,(0,200,0))

    def __init__(self,row,col,sizeRow, sizeCol,health,sheild,sheildRegen,healthRegen, attack, AttRange, MovRange, imageName):

        self.row = row
        self.col = col
        self.sizeRow = sizeRow
        self.sizeCol = sizeCol

        self.health = health
        self.sheild = sheild
        self.CURhealth = health
        self.CURsheild = sheild
        self.sheildRegen = sheildRegen
        self.healthRegen = healthRegen

        self.population = 0

        self.attack = attack
        self.AttRange = AttRange
        self.MovRange = MovRange
        self.canMove = True

        self.AirUnit = False
        self.stealth = False
        self.dectection = False

        self.image = load.load_image_smooth('Units/' + imageName, 1.5)
        self.xerror = 0
        self.yerror = 0
        self.Map = Unit.Map

        self.tile_cache = [0] * self.sizeRow * self.sizeCol


        Unit.Units.append(self)

    def __eq__(self, other):
        return type(self) == type(other) and (self.row,self.col) == (other.row,other.col)


    def move(self, DestRow, DestCol):
        if self.AirUnit == True:
            if (DestRow, DestCol) in self.checkAirMoves(self.MovRange):
                i = 0
                for r in xrange(self.sizeRow):
                    for c in xrange(self.sizeCol):
                        self.Map.board[self.row+r][self.col+c] = self.tile_cache[i]
                        i += 1
                #self.undrawUnit()
                self.row = DestRow
                self.col = DestCol
                # set the tile cache
                self.tile_cache = []
                for r in xrange(self.sizeRow):
                    for c in xrange(self.sizeCol):
                        self.tile_cache.append(self.Map.board[self.row+r][self.col+c])
                self.canMove = False

        # ground unit
        else:
            if (DestRow,DestCol) in self.checkGroundMoves(self.MovRange):
                i = 0
                for r in xrange(self.sizeRow):
                    for c in xrange(self.sizeCol):
                        self.Map.board[self.row+r][self.col+c] = 0
                        i += 1
                #self.undrawUnit()
                self.row = DestRow
                self.col = DestCol
                self.canMove = False


    def checkAirMoves(self, range):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        AirMoves = []
        for dir in dirs:
            if self.sizeRow == 1 or self.sizeCol == 1:
                result = self.checkAirMovesInDir(range-1,self.row+dir[0], self.col + dir[1], dir)
            else:
                result = self.checkAirMovesInDirForBigUnits(range-max(self.sizeCol,self.sizeRow),self.row + self.sizeRow * dir[0],
                                                               self.col+ self.sizeCol* dir[1], dir)

            if result != None:
                AirMoves.extend(result)
        AirMoves = list(set(AirMoves))
        if (self.row, self.col) in AirMoves:
            AirMoves.remove((self.row,self.col))
        return sorted(AirMoves)

    def checkAirMovesInDir(self, range, row, col, (drow, dcol)):
        board = Unit.Map.board
        if (row) >= len(board) or (row) < 0 \
            or (col) >= len(board[0]) or (col) < 0:
            return None
        elif board[row][col] != 0 and board[row][col] != 1:
            return None

        elif range == 0:
            return [(row, col)]

        else:
            possibleMoves = [ ]
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            for dir in dirs:
                if dir != (-drow,-dcol):
                    result = self.checkAirMovesInDir(range-1,row+dir[0], col + dir[1],dir)
                    if result != None:
                        possibleMoves.extend(result + [(row,col)])
            return possibleMoves

    def checkAirMovesInDirForBigUnits(self, range, row, col, (drow, dcol)):
        board = Unit.Map.board
        legalTiles = [0,1]
        if (row) >= len(board)-1 or (row) < 0 \
            or (col) >= len(board[0])-1 or (col) < 0:
            return None
        elif board[row][col] not in legalTiles or  board[row][col+1] not in legalTiles or \
              board[row+1][col] not in legalTiles or board[row+1][col+1] not in legalTiles:
            return None

        elif range == 0:
            return [(row, col)]

        else:
            possibleMoves = [ ]
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            for dir in dirs:
                if dir != (-drow,-dcol):
                    result = self.checkAirMovesInDirForBigUnits(range-1,row+dir[0], col + dir[1],dir)
                    if result != None:
                        possibleMoves.extend(result + [(row,col)])
            return possibleMoves


    def checkGroundMoves(self, range):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        groundMoves = []
        for dir in dirs:
            if self.sizeRow == 1 or self.sizeCol == 1:
                result = self.checkGroundMovesInDir(range-1,self.row+dir[0], self.col + dir[1], dir)
            else:
                result = self.checkGroundMovesInDirForBigUnits(range-max(self.sizeCol,self.sizeRow),self.row + self.sizeRow * dir[0],
                                                               self.col+ self.sizeCol* dir[1], dir)

            if result != None:
                groundMoves.extend(result)
        groundMoves = list(set(groundMoves))
        if (self.row, self.col) in groundMoves:
            groundMoves.remove((self.row,self.col))
        return sorted(groundMoves)


    def checkGroundMovesInDir(self, range, row, col, (drow, dcol)):
        board = Unit.Map.board
        if (row) >= len(board) or (row) < 0 \
                 or (col) >= len(board[0]) or (col) < 0:
            return None
        elif board[row][col] != 0:
            return None

        elif range == 0:
            return [(row, col)]

        else:
            possibleMoves = [ ]
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            for dir in dirs:
                if dir != (-drow,-dcol):
                    result = self.checkGroundMovesInDir(range-1,row+dir[0], col + dir[1],dir)
                    if result != None:
                        possibleMoves.extend(result + [(row,col)])
            return possibleMoves

    def checkGroundMovesInDirForBigUnits(self, range, row, col, (drow, dcol)):
        board = Unit.Map.board
        if (row) >= len(board)-1 or (row) < 0 \
            or (col) >= len(board[0])-1 or (col) < 0:
            return None
        elif board[row][col] != 0 or board[row][col+1] != 0 or\
                board[row+1][col] != 0 or board[row+1][col+1] != 0:
            return None

        elif range == 0:
            return [(row, col)]

        else:
            possibleMoves = [ ]
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            for dir in dirs:
                if dir != (-drow,-dcol):
                    result = self.checkGroundMovesInDirForBigUnits(range-1,row+dir[0], col + dir[1],dir)
                    if result != None:
                        possibleMoves.extend(result + [(row,col)])
            return possibleMoves

    def drawUnit(self):
        surface = Unit.mapSurface
        cellWidth, cellHeight = self.Map.getCellsize()
        x = cellWidth * self.col + self.xerror
        y = cellHeight * self.row + self.yerror
        surface.blit(self.image,(x,y))

        for r in xrange(self.sizeRow):
            for c in xrange(self.sizeCol):
                # set the data on map board
                self.Map.board[self.row + r][self.col + c] = self
                # draw the unit on the mini map





    def undrawUnit(self):
        rect = self.image.get_rect()
        cW,cH = self.Map.getCellsize()
        surface = Unit.mapSurface
        surface.blit(Unit.originalSurface,(self.col*cW+self.xerror,self.row*cH+self.yerror),
                     pygame.Rect(self.col*cW+self.xerror,self.row*cH+self.yerror,rect[2],rect[3]))

    def drawMoves(self,color):
        cW,cH = self.Map.getCellsize()
        screen = self.screen
        block = pygame.Surface((cW,cH),pygame.SRCALPHA)
        block.fill(color)

        if self.AirUnit == False:

            for (row,col) in self.checkGroundMoves(self.MovRange):
                for r in xrange(self.sizeRow):
                    for c in xrange(self.sizeCol):
                        localX = (col+c)*cW- abs(self.Map.x)
                        localY = (row+r)*cH- abs(self.Map.y)
                        self.screen.blit(block,(localX,localY))
                    #self.Map.drawBlock(row+r,col+c,color)

        else:
            for (row,col) in self.checkAirMoves(self.MovRange):
                for r in xrange(self.sizeRow):
                    for c in xrange(self.sizeCol):
                        localX = (col+c)*cW- abs(self.Map.x)
                        localY = (row+r)*cH- abs(self.Map.y)
                        self.screen.blit(block,(localX,localY))

    def playSound(self,soundList):
        sound = random.choice(soundList)
        sound.play()









