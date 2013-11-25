import pygame
from pygame.locals import *
from sys import exit


import load
import map
import Building
import ProtossBuildings
import ProtossUnit
import Unit

def mousePressed(data):
    row, col = mouse2RC(data)
    mouseStatus = pygame.mouse.get_pressed()
    if mouseStatus[0] == 1:
        if data.map.board[row][col] == 0:
            # if the previous selection is a unit, move that unit if possible
            if isinstance(data.selected,Unit.Unit):
                data.selected.move(row,col)
        elif isinstance(data.map.board[row][col],Unit.Unit):
            # if the previously selected is a unit, if now display the range
            data.selected = data.map.board[row][col]
        elif isinstance(data.map.board[row][col],Building.building):
            print 'selected a building'
        else:
            data.selected = data.map.board[row][col]
    elif mouseStatus[2] == 1:
        data.selected = None


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

    # for testing purposes
    if keyStatus[K_z] == 1:
        print ' Next Round !'
        #print Building.building.finishedBuildings
        Building.building.nextRound()
        Unit.Unit.nextRound()
    if keyStatus[K_x] == 1:
        data.zealot.undrawUnit()

def checkMouse(data):

    # check auto-scrolling
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
    Unit.Unit.drawAllUnits()
    if isinstance(data.selected,Unit.Unit):
        if data.selected.canMove:
            data.selected.drawMoves((0,200,0,100))
    #drawGrid(data)
    #data.screen.blit(data.pointerImage, (data.mouseX, data.mouseY))
    pygame.display.flip()

def init(data):
    data.mode = 'run'

    data.map = map.map('fastest', 64, 64,scale = 1.5)
    data.cellWidth, data.cellHeight = data.map.getCellsize()


    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile)
    #pygame.mouse.set_visible(False)
    data.AutoScrollWidth = 75

    data.selected = None

    data.buildings = Building.building.buildings
    Building.building.setMap(data.map)
    Unit.Unit.setMap(data.map)
    Unit.Unit.setScreen(data.screen)
    '''
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
    '''
    #data.zealot = Unit.Unit(8, 7,1,1,100,100,2,0,10,1,6,'Protoss/Zealot.gif')
    data.zealot = ProtossUnit.Zealot(8,9)
    data.archon = Unit.Unit(4,4,2,2,10,300,3,0,30,3,6,'Protoss/Archon.gif')


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