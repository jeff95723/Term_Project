import pygame
from pygame.locals import *
import random

import Building
import Unit
import TerranUnit
import load

class TerranBuilding(Building.building):
    terranBuildings = []
    unfinishedBuildingImage = None

    @classmethod
    def getAllTerranBuildings(cls):
        return cls.terranBuildings

    def drawUnfinishedBuilding(self):
        scale = min(self.sizeCol,self.sizeRow)/2.0
        unfinishedBuildingImage = load.load_image('Buildings/Terran/TerranCore.png',scale = scale)
        TerranBuilding.unfinishedBuildingImage = unfinishedBuildingImage
        super(TerranBuilding,self).drawUnfinishedBuilding(unfinishedBuildingImage)
        TerranBuilding.terranBuildings.append(self)

    def undrawUnfinishedBuilding(self):
        rect = TerranBuilding.unfinishedBuildingImage.get_rect()
        cW, cH = self.Map.getCellsize()
        surface = TerranBuilding.mapSurface
        surface.blit(TerranBuilding.originalSurface,(self.col*cW,self.row*cH),
                     pygame.Rect(self.col*cW,self.row*cH,rect[2],rect[3]))

    def __init__(self, row, col, sizeRow, sizeCol, health, sheild, imageName):
        super(TerranBuilding, self).__init__(row, col, sizeRow, sizeCol, health, 0, 0, 0, imageName)
        self.buildRound = 3
        self.Avatar = load.load_avatar('Terran/Advisor.gif')
        self.idleSounds = [load.load_sound('Terran/Bldg/TCsSca00.wav')]
        self.deathSound = [load.load_sound('Misc/explo5.wav')]

    def die(self):
        TerranBuilding.terranBuildings.remove(self)
        if self in TerranBuilding.buildingBuildings:
            TerranBuilding.buildingBuildings.remove(self)
        elif self in TerranBuilding.finishedBuildings:
            TerranBuilding.finishedBuildings.remove(self)
        super(TerranBuilding,self).die()

    def playSound(self, soundList):
        sound = random.choice(soundList)
        sound.play()

class CommandCenter(TerranBuilding):
    image = 'Buildings/Terran/Command Center.gif'
    scale = 1.3
    sizeRow = 3
    sizeCol = 4
    xerror = 10
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Command Center.gif'
        super(CommandCenter,self).__init__(row,col,3,4,1500,0,imageName)
        self.xerror = 10
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.3)
        self.buildRound = 5
        self.Build = [TerranUnit.SCV]
        self.BuildSize = [(1,1)]
        self.BuildRound = [2]

class SupplyDepot(TerranBuilding):
    image = 'Buildings/Terran/Supply Depot.gif'
    scale = 1.1
    sizeRow = 2
    sizeCol = 2
    xerror = -5
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Supply Depot.gif'
        super(SupplyDepot,self).__init__(row,col,2,2,500,0,imageName)
        self.xerror = -5
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.1)
        self.buildRound = 1

class Gas(TerranBuilding):
    image = 'Buildings/Terran/Refinery.gif'
    scale = 1.2
    sizeRow = 2
    sizeCol = 4
    xerror = 20
    yerror = -10

    def __init__(self,row,col):
        imageName = 'Terran/Refinery.gif'
        super(Gas,self).__init__(row,col,2,4,750,0,imageName)
        self.xerror = 20
        self.yerror = -10
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.2)
        self.buildRound = 1

class Barrack(TerranBuilding):
    image = 'Buildings/Terran/Barracks.gif'
    scale = 1.2
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Barracks.gif'
        super(Barrack,self).__init__(row,col,3,3,1000,0,imageName)
        self.xerror = 0
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.2)
        self.buildRound = 2

class Academy(TerranBuilding):
    image = 'Buildings/Terran/Academy.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Academy.gif'
        super(Academy,self).__init__(row,col,3,3,600,0,imageName)
        self.xerror = 0
        self.yerror = 0
        self.buildRound = 3

class Factory(TerranBuilding):
    image = 'Buildings/Terran/Factory.gif'
    scale = 1.3
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Factory.gif'
        super(Factory,self).__init__(row,col,3,3,1000,0,imageName)
        self.xerror = 0
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.3)
        self.buildRound = 3

class Starport(TerranBuilding):
    image = 'Buildings/Terran/Starport.gif'
    scale = 1.3
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Starport.gif'
        super(Starport,self).__init__(row,col,3,3,1000,0,imageName)
        self.xerror = 0
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.3)
        self.buildRound = 3

class ScienceFacility(TerranBuilding):
    image = 'Buildings/Terran/Science Facility.gif'
    scale = 1.3
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 20

    def __init__(self,row,col):
        imageName = 'Terran/Science Facility.gif'
        super(ScienceFacility,self).__init__(row,col,3,3,750,0,imageName)
        self.xerror = 0
        self.yerror = 20
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.3)
        self.buildRound = 3

class EngineeringBay(TerranBuilding):
    image = 'Buildings/Terran/Engineering Bay.gif'
    scale = 1.1
    sizeRow = 3
    sizeCol = 3
    xerror = -5
    yerror = 20

    def __init__(self,row,col):
        imageName = 'Terran/Engineering Bay.gif'
        super(EngineeringBay,self).__init__(row,col,3,3,850,0,imageName)
        self.xerror = -5
        self.yerror = 20
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.1)
        self.buildRound = 3

class Armory(TerranBuilding):
    image = 'Buildings/Terran/Armory.gif'
    scale = 1.4
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Armory.gif'
        super(Armory,self).__init__(row,col,3,3,750,0,imageName)
        self.xerror = 0
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.4)
        self.buildRound = 3

class MissileTurret(TerranBuilding):
    image = 'Buildings/Terran/Missile Turret.gif'
    scale = 1.5
    sizeRow = 2
    sizeCol = 2
    xerror = 10
    yerror = 0

    def __init__(self,row,col):
        imageName = 'Terran/Missile Turret.gif'
        super(MissileTurret,self).__init__(row,col,2,2,200,0,imageName)
        self.xerror = 10
        self.yerror = 0
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.5)
        self.buildRound = 2
