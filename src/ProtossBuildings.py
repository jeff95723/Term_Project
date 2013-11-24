import pygame
from pygame.locals import *

import Building
import load

class ProtossBuilding(Building.building):
    protossBuildings = []
    unfinishedBuildingImage = None

    @classmethod
    def getAllProtossBuildings(cls):
        return cls.protossBuildings


    def drawUnfinishedBuilding(self, buildingSurfaceIndex):
        unfinishedBuildingImage = load.load_image('Buildings/Protoss/ProtossCore.png')
        ProtossBuilding.unfinishedBuildingImage = unfinishedBuildingImage
        super(ProtossBuilding,self).drawUnfinishedBuilding(buildingSurfaceIndex,unfinishedBuildingImage)
        ProtossBuilding.protossBuildings.append(self)

    def undrawBuilding(self, buildingSurfaceIndex):
        rect = ProtossBuilding.unfinishedBuildingImage.get_rect()
        cW, cH = self.Map.getCellsize()
        surface = ProtossBuilding.buildingSurfaces[buildingSurfaceIndex]
        surface.blit(ProtossBuilding.originalSurface,(self.col*cW,self.row*cH),
                     pygame.Rect(self.col*cW,self.row*cH,rect[2],rect[3]))

    def __init__(self, row, col, sizeRow, sizeCol, imageName, Map):
        super(ProtossBuilding, self).__init__(row, col, sizeRow, sizeCol, imageName, Map)
        self.buildRound = 3

class Nexus(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Nexus.gif'
        super(Nexus,self).__init__(row,col,3,4,imageName,Map)
        self.xerror = 0
        self.yerror = -40
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.3)

class Gas(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Gas.gif'
        super(Gas,self).__init__(row,col,2,4,imageName,Map)
        self.xerror = 0
        self.yerror = -30

class CyberneticsCore(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Cybernetics Core.gif'
        super(CyberneticsCore,self).__init__(row,col,3,3,imageName,Map)
        self.xerror = 5
        self.yerror = 0

class FleetBeacon(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Fleet Beacon.gif'
        super(FleetBeacon, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = -35
        self.yerror = 0

class Forge(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Forge.gif'
        super(Forge, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = 0
        self.yerror = 15

class Gateway(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Gateway.gif'
        super(Gateway, self).__init__(row, col, 3,3, imageName, Map)
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.2)
        self.xerror = 0
        self.yerror = 10

class Observatory(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Observatory.gif'
        super(Observatory, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = 0
        self.yerror = 15

class Cannon(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Photon Cannon.gif'
        super(Cannon, self).__init__(row, col, 2,2, imageName, Map)
        self.xerror = 0
        self.yerror = 40


class Pylon(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Pylon.gif'
        super(Pylon, self).__init__(row, col, 2,2, imageName, Map)
        self.xerror = 8
        self.yerror = 0


class RoboticsFacility(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Robotics Facility.gif'
        super(RoboticsFacility, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = 0
        self.yerror = 0


class RoboticsSupportBay(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Robotics Support Bay.gif'
        super(RoboticsSupportBay, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = 0
        self.yerror = 10


class Stargate(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Stargate.gif'
        super(Stargate, self).__init__(row, col, 3,3, imageName, Map)
        self.image = load.load_image_smooth('Buildings/'+imageName, scale= 1.2)
        self.xerror = 0
        self.yerror = 0


class TemplarArchives(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Templar Archives.gif'
        super(TemplarArchives, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = -10
        self.yerror = 0


class TwilightCouncil(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Citadel of Adun.gif'
        super(TwilightCouncil, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = 0
        self.yerror = 10



class ArbiterTribunal(ProtossBuilding):
    def __init__(self, row, col, Map):
        imageName = 'Protoss/Arbiter Tribunal.gif'
        super(ArbiterTribunal, self).__init__(row, col, 3,3, imageName, Map)
        self.xerror = 0
        self.yerror = 10


