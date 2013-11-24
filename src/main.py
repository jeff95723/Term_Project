import pygame
from pygame.locals import *
from sys import exit


import load
import map
import Building
import ProtossBuildings
import Unit

def mousePressed(data):
    pass

def mouse2RC(data):
    x,y = pygame.mouse.get_pos()
    row = (y - data.map.y)/data.cellHeight
    col = (x - data.map.x)/data.cellWidth
    return (row,col)

def checkKeys(data):
    keyStatus = pygame.key.get_pressed()
    if keyStatus[K_RIGHT] == 1:

        data.map.move((-data.cellWidth,0))
        #print 'Right Pressed'
    if keyStatus[K_LEFT] == 1:
        data.map.move((data.cellWidth,0))
        #print 'Left Pressed'
    if keyStatus[K_UP] == 1:
        data.map.move((0,data.cellHeight))
        #print 'Up Pressed'
    if keyStatus[K_DOWN] == 1:
        data.map.move((0,-data.cellHeight))
        #print 'Down Pressed'
    if keyStatus[K_z] == 1:
        print ' Next Round !'
        print Building.building.finishedBuildings
        Building.building.nextRound()

def checkMouse(data):
    if data.mouseX < data.AutoScrollWidth and data.mouseY < data.AutoScrollWidth:
        data.map.move((data.cellWidth,data.cellHeight))

    elif data.mouseX < data.AutoScrollWidth and data.ViewSize[1] > data.mouseY > data.ViewSize[1] - data.AutoScrollWidth:
        data.map.move((data.cellWidth,-data.cellHeight))

    elif data.mouseX > data.ViewSize[0] - data.AutoScrollWidth and data.mouseY < data.AutoScrollWidth:
        data.map.move((-data.cellWidth,data.cellHeight))

    elif data.mouseX > data.ViewSize[0] - data.AutoScrollWidth and data.ViewSize[1] > data.mouseY > data.ViewSize[1] - data.AutoScrollWidth:
        data.map.move((-data.cellWidth,-data.cellHeight))

    elif data.mouseX < data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseY < data.ViewSize[1] - data.AutoScrollWidth):
            data.map.move((data.cellWidth,0))

    elif data.mouseX > data.ViewSize[0] - data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseY < data.ViewSize[1] - data.AutoScrollWidth):
            data.map.move((-data.cellWidth,0))

    elif data.mouseY < data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseX < data.ViewSize[0] - data.AutoScrollWidth):
            data.map.move((0,data.cellHeight))

    elif data.ViewSize[1] > data.mouseY > data.ViewSize[1] - data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseX < data.ViewSize[0] - data.AutoScrollWidth):
            data.map.move((0,-data.cellHeight))


def timerFired(data):
    data.mouseX, data.mouseY = pygame.mouse.get_pos()
    redrawAll(data)
    data.clock.tick(60)
    checkKeys(data)
    checkMouse(data)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = 'quit'
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(data)

def drawGrid(data):
    cW, cH = data.map.getCellsize()
    # get the width and height of the screen
    rows, cols = (data.ViewSize[1])/cH,data.ViewSize[0]/cW
    display = pygame.display.get_surface()
    width, height = pygame.Surface.get_size(display)
    for row in xrange(rows):
        pygame.draw.lines(data.screen, (0,0,0),False, [(0,row * cH),(width,row * cH)])
    for col in xrange(cols):
        pygame.draw.lines(data.screen, (0,0,0),False, [(col * cW, 0),(col * cW, height)])

def redrawAll(data):

    data.screen.fill((0,0,0))
    data.map.draw(data.screen)
    ProtossBuildings.ProtossBuilding.drawAllBuildings()
    drawGrid(data)
    data.screen.blit(data.pointerImage, (data.mouseX, data.mouseY))
    pygame.display.flip()

def init(data):
    data.mode = 'run'

    data.map = map.map('fastest', 64, 64,scale = 1.5)
    data.cellWidth, data.cellHeight = data.map.getCellsize()


    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile)
    pygame.mouse.set_visible(False)
    data.AutoScrollWidth = 75

    data.buildings = Building.building.buildings
    Building.building.setMap(data.map)
    nexus = ProtossBuildings.Nexus(8, 9)
    gas = ProtossBuildings.Gas(8, 3)
    by = ProtossBuildings.CyberneticsCore(15, 0)
    vf = ProtossBuildings.FleetBeacon(15, 3)
    bf = ProtossBuildings.Forge(15, 6)
    bg = ProtossBuildings.Gateway(15, 9)
    vo = ProtossBuildings.Observatory(15, 12)
    bc = ProtossBuildings.Cannon(18, 0)
    bp = ProtossBuildings.Pylon(18, 2)
    vr = ProtossBuildings.RoboticsFacility(15, 15)
    vb = ProtossBuildings.RoboticsSupportBay(12, 0)
    vs = ProtossBuildings.Stargate(12, 3)
    vt = ProtossBuildings.TemplarArchives(12, 6)
    vc = ProtossBuildings.TwilightCouncil(12, 9)
    va = ProtossBuildings.ArbiterTribunal(12, 12)


def run():
    pygame.init()

    class Struct:pass
    data = Struct()

    data.ViewSize = ( 960, 960)
    data.screen = pygame.display.set_mode((data.ViewSize),HWSURFACE)
    pygame.display.set_caption('Test')

    data.clock = pygame.time.Clock()
    init(data)
    while 1:
        if data.mode == 'quit':
            exit()
        timerFired(data)



run()