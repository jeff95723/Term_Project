import pygame
from pygame.locals import *
import random

import Building
import Unit
import ProtossUnit
import load

class ProtossBuilding(Building.building):
    protossBuildings = []
    unfinishedBuildingImage = None

    @classmethod
    def getAllProtossBuildings(cls):
        return cls.protossBuildings

    @classmethod
    def drawFogOfWarBoard(cls,index):
        for bld in cls.protossBuildings:
            inSight = bld.checkSight(10)
            for (r,c) in inSight:
                bld.Map.fogOfWarBoard[index][r][c] = 1

        for row in xrange(bld.sizeRow):
            for col in xrange(bld.sizeCol):
                bld.Map.fogOfWarBoard[index][bld.row+row][bld.col+col] = 1

    @classmethod
    def addTofinishedBuildings(cls, bld):
        cls.buildingBuildings.remove(bld)
        cls.finishedBuildings.append(bld)

    @classmethod
    def nextRound(cls, data):
        for bld in cls.protossBuildings:
            bld.buildRound -= 1
            if bld.buildRound == 0:
                if bld in Building.building.buildingBuildings:
                    Building.building.buildingBuildings.remove(bld)
                    bld.undrawUnfinishedBuilding()
                Building.building.finishedBuildings.append(bld)

        data.currentPlayer.updateCurrentPopulation()
        data.currentPlayer.updateCurrentPopulationAvaliable()

        for bld in cls.protossBuildings:
            if bld.buildQueue != []:
                CURsup = data.currentPlayer.currentPopulation
                AVBsup = data.currentPlayer.PopulationAvaliable
                if AVBsup-CURsup >= bld.Build[bld.buildQueue[0]].population:
                    bld.currentBuildRoundLeft[0] -= 1
                    if bld.currentBuildRoundLeft[0] == 0:
                        bld.build(bld.buildQueue[0])
                        bld.buildQueue = bld.buildQueue[1:]
                        bld.currentBuildRoundLeft = bld.currentBuildRoundLeft[1:]
                else:
                    print 'No more supply!!'
                    data.currentPlayer.playSound(data.currentPlayer.NoMoreSupplySound)

    def drawUnfinishedBuilding(self):
        scale = min(self.sizeCol, self.sizeRow)/2.0
        unfinishedBuildingImage = load.load_image('Buildings/Protoss/ProtossCore.png',scale = scale)
        ProtossBuilding.unfinishedBuildingImage = unfinishedBuildingImage
        super(ProtossBuilding, self).drawUnfinishedBuilding(unfinishedBuildingImage)
        ProtossBuilding.protossBuildings.append(self)

    def undrawUnfinishedBuilding(self):
        rect = ProtossBuilding.unfinishedBuildingImage.get_rect()
        cW, cH = self.Map.getCellsize()
        surface = ProtossBuilding.mapSurface
        surface.blit(ProtossBuilding.originalSurface,(self.col*cW,self.row*cH),
                     pygame.Rect(self.col*cW,self.row*cH,rect[2],rect[3]))

    def __init__(self, row, col, sizeRow, sizeCol, health, sheild, imageName):
        super(ProtossBuilding, self).__init__(row, col, sizeRow, sizeCol, health, sheild, 0, 5, imageName)
        self.buildRound = 3
        self.Avatar = load.load_avatar('Protoss/Advisor.gif')
        self.idleSounds = [load.load_sound('Protoss/Bldg/pneWht00.wav')]
        self.deathSound = [load.load_sound('Misc/explo4.wav')]

        ProtossBuilding.protossBuildings.append(self)

    def die(self):
        ProtossBuilding.protossBuildings.remove(self)
        if self in ProtossBuilding.buildingBuildings:
            ProtossBuilding.buildingBuildings.remove(self)
        elif self in ProtossBuilding.finishedBuildings:
            ProtossBuilding.finishedBuildings.remove(self)
        super(ProtossBuilding,self).die()

    def playSound(self, soundList):
        sound = random.choice(soundList)
        sound.play()

class Nexus(ProtossBuilding):

    image= 'Buildings/Protoss/Nexus.gif'
    scale = 1.3
    sizeRow = 3
    sizeCol = 4
    xerror = 0
    yerror = -40

    cost = 500
    def __init__(self, row, col):
        imageName = 'Protoss/Nexus.gif'
        super(Nexus, self).__init__(row, col, 3, 4, 750, 750, imageName)
        self.xerror = 0
        self.yerror = -40
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.3)
        self.buildRound = 5
        self.supply = 10
        self.Build = [ProtossUnit.Probe]
        self.BuildSize = [(1,1)]
        self.BuildRound = [2]

class Gas(ProtossBuilding):
    image= 'Buildings/Protoss/Gas.gif'
    scale = 1.5
    sizeRow = 2
    sizeCol = 4
    xerror = 0
    yerror = -30

    cost = 150
    def __init__(self, row, col):
        imageName = 'Protoss/Gas.gif'
        super(Gas, self).__init__(row, col, 2, 4, 150, 150, imageName)
        self.xerror = 0
        self.yerror = -30
        self.buildRound = 1

class CyberneticsCore(ProtossBuilding):
    image= 'Buildings/Protoss/Cybernetics Core.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 5
    yerror = 0

    cost = 200
    def __init__(self, row, col):
        imageName = 'Protoss/Cybernetics Core.gif'
        super(CyberneticsCore, self).__init__(row, col, 3, 3, 300, 300, imageName)
        self.xerror = 5
        self.yerror = 0

class FleetBeacon(ProtossBuilding):
    image= 'Buildings/Protoss/Fleet Beacon.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = -35
    yerror = 0

    cost = 350
    def __init__(self, row, col):
        imageName = 'Protoss/Fleet Beacon.gif'
        super(FleetBeacon, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = -35
        self.yerror = 0

class Forge(ProtossBuilding):
    image= 'Buildings/Protoss/Forge.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror =  15

    cost = 200
    def __init__(self, row, col):
        imageName = 'Protoss/Forge.gif'
        super(Forge, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = 0
        self.yerror = 15

class Gateway(ProtossBuilding):
    image= 'Buildings/Protoss/Gateway.gif'
    scale = 1.2
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror =  10

    cost = 200
    def __init__(self, row, col):
        imageName = 'Protoss/Gateway.gif'
        super(Gateway, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.2)
        self.xerror = 0
        self.yerror = 10
        self.buildRound = 2
        self.Build = [ProtossUnit.Zealot]
        self.BuildSize = [(1,1)]
        self.BuildRound = [2]

class Observatory(ProtossBuilding):
    image= 'Buildings/Protoss/Observatory.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror =  15

    cost = 200
    def __init__(self, row, col):
        imageName = 'Protoss/Observatory.gif'
        super(Observatory, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = 0
        self.yerror = 15

class Cannon(ProtossBuilding):
    image= 'Buildings/Protoss/Photon Cannon.gif'
    scale = 1.5
    sizeRow = 2
    sizeCol = 2
    xerror = 0
    yerror = 40

    cost = 150
    def __init__(self, row, col):
        imageName = 'Protoss/Photon Cannon.gif'
        super(Cannon, self).__init__(row, col, 2, 2, 100, 100, imageName)
        self.xerror = 0
        self.yerror = 40
        self.buildRound = 1

class Pylon(ProtossBuilding):
    image= 'Buildings/Protoss/Pylon.gif'
    scale = 1.5
    sizeRow = 2
    sizeCol = 2
    xerror = 8
    yerror = 0

    cost = 100
    def __init__(self, row, col):
        imageName = 'Protoss/Pylon.gif'
        super(Pylon, self).__init__(row, col, 2, 2, 100, 100, imageName)
        self.xerror = 8
        self.yerror = 0
        self.buildRound = 1
        self.supply = 10

class RoboticsFacility(ProtossBuilding):
    image= 'Buildings/Protoss/Robotics Facility.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    cost = 250
    def __init__(self, row, col):
        imageName = 'Protoss/Robotics Facility.gif'
        super(RoboticsFacility, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = 0
        self.yerror = 0
        self.Build = [ProtossUnit.Dragoon]
        self.BuildSize = [(2,2)]
        self.BuildRound = [3]

class RoboticsSupportBay(ProtossBuilding):
    image= 'Buildings/Protoss/Robotics Support Bay.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 10

    cost = 200
    def __init__(self, row, col):
        imageName = 'Protoss/Robotics Support Bay.gif'
        super(RoboticsSupportBay, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = 0
        self.yerror = 10

class Stargate(ProtossBuilding):
    image= 'Buildings/Protoss/Stargate.gif'
    scale = 1.2
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 0

    cost = 250
    def __init__(self, row, col):
        imageName = 'Protoss/Stargate.gif'
        super(Stargate, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.2)
        self.xerror = 0
        self.yerror = 0
        self.Build = [ProtossUnit.Arbiter]
        self.BuildSize = [(2,2)]
        self.BuildRound = [4]

class TemplarArchives(ProtossBuilding):
    image= 'Buildings/Protoss/Templar Archives.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = -10
    yerror = 0

    cost = 300
    def __init__(self, row, col):
        imageName = 'Protoss/Templar Archives.gif'
        super(TemplarArchives, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = -10
        self.yerror = 0
        self.Build = [ProtossUnit.DarkTemplar]
        self.BuildSize = [(1,1)]
        self.BuildRound = [5]

class TwilightCouncil(ProtossBuilding):
    image= 'Buildings/Protoss/Citadel of Adun.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 10

    cost = 300
    def __init__(self, row, col):
        imageName = 'Protoss/Citadel of Adun.gif'
        super(TwilightCouncil, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = 0
        self.yerror = 10
        self.Build = [ProtossUnit.Archon]
        self.BuildSize = [(2,2)]
        self.BuildRound = [7]

class ArbiterTribunal(ProtossBuilding):
    image= 'Buildings/Protoss/Arbiter Tribunal.gif'
    scale = 1.5
    sizeRow = 3
    sizeCol = 3
    xerror = 0
    yerror = 10

    cost = 200
    def __init__(self, row, col):
        imageName = 'Protoss/Arbiter Tribunal.gif'
        super(ArbiterTribunal, self).__init__(row, col, 3, 3, 500, 500, imageName)
        self.xerror = 0
        self.yerror = 10


