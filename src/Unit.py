import pygame
from pygame.locals import *
import load

class Unit(object):
    Units = []
    Map = None

    @classmethod
    def getUnits(cls):
        return Unit.Units

    @classmethod
    def setMap(cls, Map):
        cls.Map = Map

    def __init__(self,row,col,health,sheild,sheildRegen,healthRegen, attack, AttRange, MovRange, image):
        self.row = row
        self.col = col
        self.health = health
        self.sheild = sheild
        self.sheildRegen = sheildRegen
        self.healthRegen = healthRegen
        self.attack = attack
        self.AttRange = AttRange
        self.MovRange = MovRange
        self.AirUnit = False
        self.image = image

    def move(self, DestRow, DestCol):
        if self.AirUnit:
            dRow = DestRow - self.row
            dCol = DestCol - self.col
            board = Unit.Map.board
            if dRow + dCol <= self.moveRange and board[DestRow][DestCol] == 0:
                self.row = DestRow
                self.col = DestCol
                return True

        return False

    def checkGroundMoves(self, range):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        groundMoves = []
        for dir in dirs:
            groundMoves.extend(self.checkGroundMovesInDir(range, dir))
        return groundMoves


    def checkGroundMovesInDir(self, range, (drow, dcol)):
        board = Unit.Map.board
        if range == 0:
            return (self.row, self.col)
        elif board[self.row + drow][self.col + dcol] != 0:
            return None
        else:
            possibleMoves = [ ]
            dirs = [(drow,dcol), (-drow,dcol), (drow,-dcol)]
            for dir in dirs:
                result = self.checkGroundMovesInDir(range-1,dir)
                if result != None:
                    possibleMoves.extend(result)
            return possibleMoves

    def drawUnit(self):
        mapSurface = self.Map.image
        pass



