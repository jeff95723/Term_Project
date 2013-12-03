import pygame
from pygame.locals import *

import load
import Unit
import Building
import TerranBuildings

class TerranUnit(Unit.Unit):
    TerranUnits = [ ]

    @classmethod
    def drawFogOfWarBoard(cls,index):
        for unt in cls.TerranUnits:
            inSight = unt.checkSight(10)
            for (r,c) in inSight:
                unt.Map.fogOfWarBoard[index][r][c] = 1

            for row in xrange(unt.sizeRow):
                for col in xrange(unt.sizeCol):
                    unt.Map.fogOfWarBoard[index][unt.row+row][unt.col+col] = 1

    def __init__(self,row,col,sizeRow, sizeCol,health,sheild,sheildRegen,healthRegen, attack, AttRange, MovRange, imageName):
        imageName = 'Terran/' + imageName
        super(TerranUnit,self).__init__(row,col,sizeRow,sizeCol,health,sheild,sheildRegen,healthRegen,attack,AttRange,MovRange,imageName)
        self.Avatar = load.load_avatar(imageName)

        TerranUnit.TerranUnits.append(self)

    def die(self):
        TerranUnit.TerranUnits.remove(self)
        super(TerranUnit,self).die()

class Marine(TerranUnit):
    image = 'Units/Terran/Marine.gif'
    cost = 50
    population = 2
    def __init__(self,row,col):
        imageName = 'Marine.gif'
        super(Marine,self).__init__(row,col,1,1,40,0,0,0,24,5,7,imageName)
        sounds = load.load_sounds_in_Folder('Terran/Marine/')
        self.deathSound = [sounds[0]]
        self.hitSound = [sounds[2]]
        self.idleSounds = sounds[3:]
        self.xerror =  5
        self.yerror = 5
        self.population = 2

class Medic(TerranUnit):
    image = 'Units/Terran/Medic.gif'
    cost = 75
    population = 2

    def __init__(self,row,col):
        imageName = 'Medic.gif'
        super(Medic,self).__init__(row,col,1,1,40,0,0,0,-20,6,6,imageName)
        sounds = load.load_sounds_in_Folder('Terran/Medic/')
        self.deathSound = [sounds[0]]
        self.hitSound = [sounds[-1]]
        self.idleSounds = sounds[2:len(sounds)-1]
        self.xerror =  5
        self.yerror = 5
        self.population = 2


class FireBat(TerranUnit):
    image = 'Units/Terran/FireBat.gif'
    cost = 150
    population = 2

    def __init__(self,row,col):
        imageName = 'FireBat.gif'
        super(FireBat,self).__init__(row,col,1,1,50,0,0,0,30,3,6,imageName)
        sounds = load.load_sounds_in_Folder('Terran/Firebat/')
        self.deathSound = [sounds[1]]
        self.hitSound = [sounds[3]]
        self.idleSounds = sounds[5:]
        self.population = 2

class SiegeTank(TerranUnit):
    image = 'Units/Terran/Siege Tank.gif'
    cost = 350
    population = 4
    def __init__(self,row,col):
        imageName = 'Siege Tank.gif'
        super(SiegeTank,self).__init__(row,col,2,2,150,0,0,0,100,10,3,imageName)
        sounds = load.load_sounds_in_Folder('Terran/Tank/')
        self.deathSound = [sounds[0]]
        self.hitSound = [sounds[1]]
        self.idleSounds = sounds[2:]
        self.population = 4

        self.xerror = 0
        self.yerror = 0


class Ghost(TerranUnit):
    image = 'Units/Terran/Ghost.gif'
    cost = 250
    population = 2
    def __init__(self,row,col):
        imageName = 'Ghost.gif'
        super(Ghost,self).__init__(row,col,1,1,40,0,0,0,30,8,6,imageName)
        Trimage = self.image.copy()
        alpha = 100
        Trimage.fill((255,255,255,alpha), None, pygame.BLEND_RGBA_MULT)
        self.image = Trimage
        sounds = load.load_sounds_in_Folder('Terran/Ghost/')
        self.deathSound = [sounds[0]]
        self.hitSound = [sounds[2]]
        self.idleSounds = sounds[3:]
        self.population = 2
        self.stealth = True

class BattleCrusier(TerranUnit):
    image = 'Units/Terran/Battlecruiser.gif'
    cost = 350
    population = 6
    def __init__(self,row,col):
        imageName = 'Battlecruiser.gif'
        super(BattleCrusier,self).__init__(row,col,2,2,500,0,0,0,60,5,8,imageName)
        self.image = load.load_image_smooth('Units/Terran/Battlecruiser.gif',scale = 1.2)
        sounds = load.load_sounds_in_Folder('Terran/Battle/')
        self.deathSound = [sounds[0]]
        self.hitSound = [sounds[-1]]
        self.idleSounds = sounds[2:len(sounds)-1]
        self.population = 6

        self.xerror = 0

class SCV(TerranUnit):
    image = 'Units/Terran/SCV.gif'
    cost = 50
    population = 1
    def __init__(self,row,col):
        imageName = 'SCV.gif'
        super(SCV,self).__init__(row,col,1,1,60,0,0,0,10,1,12,imageName)
        sounds = load.load_sounds_in_Folder('Terran/SCV/')
        self.deathSound = [sounds[0]]
        self.hitSound = sounds[1:3]
        self.idleSounds = sounds[3:]
        self.population = 1

        self.canBuild = True
        self.Build = [TerranBuildings.CommandCenter,TerranBuildings.SupplyDepot,
                      TerranBuildings.Gas,TerranBuildings.Barrack,TerranBuildings.EngineeringBay,
                      TerranBuildings.MissileTurret,TerranBuildings.Academy]

        self.AdvancedBuild = [TerranBuildings.Factory,TerranBuildings.Starport,
                              TerranBuildings.EngineeringBay,TerranBuildings.Armory]

        self.xerror = 5
