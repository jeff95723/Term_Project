import pygame
from pygame.locals import *
import load

class Unit(object):
    Units = []
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
    def drawAllUnits(cls):
        for unt in cls.Units:
            unt.drawUnit()

    def __init__(self,row,col,sizeRow, sizeCol,health,sheild,sheildRegen,healthRegen, attack, AttRange, MovRange, imageName):
        self.row = row
        self.col = col
        self.sizeRow = sizeRow
        self.sizeCol = sizeCol

        self.health = health
        self.sheild = sheild
        self.sheildRegen = sheildRegen
        self.healthRegen = healthRegen

        self.attack = attack
        self.AttRange = AttRange
        self.MovRange = MovRange

        self.AirUnit = False

        self.image = load.load_image_smooth('Units/' + imageName, 1.5)
        self.xerror = 0
        self.yerror = 0
        self.Map = Unit.Map



        Unit.Units.append(self)

    def __eq__(self, other):
        return type(self) == type(other) and (self.row,self.col) == (other.row,other.col)


    def move(self, DestRow, DestCol):
        if self.AirUnit:
            dRow = DestRow - self.row
            dCol = DestCol - self.col
            board = Unit.Map.board
            if dRow + dCol <= self.moveRange and board[DestRow][DestCol] == 0:
                self.row = DestRow
                self.col = DestCol
                self.undrawUnit()

        # ground unit
        else:
            pass


    def checkGroundMoves(self, range):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        groundMoves = []
        for dir in dirs:
            if self.sizeRow == 1 or self.sizeCol == 1:
                result = self.checkGroundMovesInDir(range-1,self.row, self.col, dir)
            else:
                result = self.checkGroundMovesInDirForBigUnits(range-1,self.row, self.col, dir)

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
                board[row+1][col] or board[row+1][col+1]:
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
                self.Map.board[self.row + r][self.col + c] = self

    def undrawUnit(self):
        rect = self.image.get_rect()
        cW,cH = self.Map.getCellsize()
        surface = Unit.mapSurface
        surface.blit(Unit.originalSurface,(self.col*cW,self.row*cH),
                     pygame.Rect(self.col*cW,self.row*cH,rect[2],rect[3]))

    def drawMoves(self,color):
        for (row,col) in self.checkGroundMoves(self.MovRange):
            for r in xrange(self.sizeRow):
                for c in xrange(self.sizeCol):
                    self.Map.drawBlock(row+r,col+c,color)







