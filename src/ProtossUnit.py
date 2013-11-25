import pygame
from pygame.locals import *

import load
import Unit

class ProtossUnit(Unit.Unit):
    ProtossUnits = []

    def __init__(self,row,col,sizeRow, sizeCol,health,sheild,sheildRegen,healthRegen, attack, AttRange, MovRange, imageName):
        imageName = 'Protoss/' + imageName
        super(ProtossUnit,self).__init__(row,col,sizeRow,sizeCol,health,sheild,sheildRegen,healthRegen,attack,AttRange,MovRange,imageName)

        ProtossUnit.ProtossUnits.append(self)

class Zealot(ProtossUnit):

    def __init__(self,row,col):
        imageName = 'Zealot.gif'
        super(Zealot,self).__init__(row,col,1,1,100,100,5,0,16,1,6,imageName)


