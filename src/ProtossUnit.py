import pygame
from pygame.locals import *
import os
import copy

import load
import Unit

class ProtossUnit(Unit.Unit):
    ProtossUnits = []

    def __init__(self,row,col,sizeRow, sizeCol,health,sheild,sheildRegen,healthRegen, attack, AttRange, MovRange, imageName):
        imageName = 'Protoss/' + imageName
        super(ProtossUnit,self).__init__(row,col,sizeRow,sizeCol,health,sheild,sheildRegen,healthRegen,attack,AttRange,MovRange,imageName)
        self.Avatar = load.load_avatar(imageName)

        ProtossUnit.ProtossUnits.append(self)

class Zealot(ProtossUnit):
    def __init__(self,row,col):
        imageName = 'Zealot.gif'
        super(Zealot,self).__init__(row,col,1,1,100,100,5,0,32,1,6,imageName)
        sounds = load.load_sounds_in_Folder('Protoss/Zealot/')
        self.deathSound = sounds[2]
        self.hitSound = sounds[3]
        self.idleSounds = sounds[4:]
        self.xerror =  7
        self.population = 2


class Arbiter(ProtossUnit):
    def __init__(self,row,col):
        imageName = 'Arbiter.gif'
        super(Arbiter,self).__init__(row,col,2,2,200,150,10,0,20,5,8,imageName)
        sounds = load.load_sounds_in_Folder('Protoss/Arbiter/')
        self.deathSound = sounds[0]
        self.hitSound = sounds[-1]
        self.idleSounds = sounds[1:len(sounds)-1]
        self.population = 4
        self.AirUnit = True

class Archon(ProtossUnit):
    def __init__(self,row,col):
        imageName = 'Archon.gif'
        super(Archon,self).__init__(row,col,2,2,10,300,15,0,60,2,6,imageName)
        sounds = load.load_sounds_in_Folder('Protoss/Archon/')
        self.deathSound = sounds[0]
        self.hitSound = sounds[1]
        self.idleSounds = sounds[2:]
        self.population = 4

        self.xerror = -10
        self.yerror = -10


class DarkTemplar(ProtossUnit):
    def __init__(self,row,col):
        imageName = 'Dark Templar.gif'
        super(DarkTemplar,self).__init__(row,col,1,1,80,40,5,0,40,1,6,imageName)
        Trimage = self.image.copy()
        alpha = 100
        Trimage.fill((255,255,255,alpha), None, pygame.BLEND_RGBA_MULT)
        self.image = Trimage
        sounds = load.load_sounds_in_Folder('Protoss/DarkTemplar/')
        self.deathSound = sounds[0]
        self.hitSound = sounds[1]
        self.idleSounds = sounds[4:len(sounds)-1]
        self.population = 4
        self.stealth = True

class Dragoon(ProtossUnit):
    def __init__(self,row,col):
        imageName = 'Dragoon.gif'
        super(Dragoon,self).__init__(row,col,2,2,100,80,10,0,40,4,8,imageName)
        sounds = load.load_sounds_in_Folder('Protoss/Dragoon/')
        self.deathSound = sounds[1]
        self.hitSound = sounds[0]
        self.idleSounds = sounds[2:]
        self.population = 2

        self.xerror = 18

class Probe(ProtossUnit):
    def __init__(self,row,col):
        imageName = 'Probe.gif'
        super(Probe,self).__init__(row,col,1,1,20,20, 5,0,10,1,12,imageName)
        sounds = load.load_sounds_in_Folder('Protoss/Probe/')
        self.deathSound = sounds[2]
        self.hitSound = sounds[0:2]
        self.idleSounds = sounds[3:]
        self.population = 1

        self.xerror = 5

