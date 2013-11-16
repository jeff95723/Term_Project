import pygame
from pygame.locals import *
import load

class Unit(object):
    Units = []
    @classmethod
    def getUnits(cls):
        return Unit.Units

    def __init__(self):
        self.row = 0
        self.col = 0
        self.health = 0
        self.sheild = 0
        self.regen = 0
        self.attack = 0
        self.AttRange = 0
        self.moveRange = 0
        self.image = None

    def move(self, DestRow, DestCol):
        dRow = DestRow - self.row
        dCol = DestCol - self.col
        if dRow + dCol < self.moveRange:
            self.row = DestRow
            self.col = DestCol
            return True

        return False
