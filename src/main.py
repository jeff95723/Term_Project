import pygame
from pygame.locals import *
from sys import exit


import load
import map
import Building
import ProtossBuildings
import ProtossUnit
import Unit
import Menu

def mousePressed(data):
    row, col = mouse2RC(data)
    mouseStatus = pygame.mouse.get_pressed()
    mouseRegion = Menu.checkRegion(data)

    # if in unit selection region
    if mouseRegion == 0:
        if mouseStatus[0] == 1:
            if data.map.board[row][col] == 0:
                # if the previous selection is a unit, move that unit if possible
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canMove:
                        if data.buttonStatus[0] == 1:
                            data.selected.move(row,col)
                else:
                    data.selected = None
            elif data.map.board[row][col] == 1:
                # if the previous selection is a unit, move that unit if possible
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canMove and data.selected.AirUnit:
                        if data.buttonStatus[0] == 1:
                            data.selected.move(row,col)
                else:
                    data.selected = None
            elif isinstance(data.map.board[row][col],Unit.Unit):
                # if the previously selected is a unit, if now display the range
                data.selected = data.map.board[row][col]
                data.selected.playSound(data.selected.idleSounds)
            elif isinstance(data.map.board[row][col],Building.building):
                data.selected = data.map.board[row][col]
            else:
                data.selected = data.map.board[row][col]
        elif mouseStatus[2] == 1:
            data.selected = None

    #update the button Status
    Menu.updateButtonStatus(data)


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
        data.selected = None
    if keyStatus[K_x] == 1:
        data.zealot.undrawUnit()

def checkAutoScroll(data):

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

def checkMiniMapScroll(data):
    mouseStatus = pygame.mouse.get_pressed()
    mouseRegion = Menu.checkRegion(data)
    if mouseRegion == 1:
        mMapx, mMapy = Menu.getMiniMapOrigin()
        if mouseStatus[0] == 1:
            DestX, DestY = data.mouseX - 20, data.mouseY-20
            data.ViewBox.x = DestX - mMapx
            data.ViewBox.y = DestY - mMapy
            if data.ViewBox.x < 0:
                data.ViewBox.x = 0
            if data.ViewBox.x > 128-40:
                data.ViewBox.x = 128-40
            if data.ViewBox.y < 0:
                data.ViewBox.y = 0
            if data.ViewBox.y > 128-40:
                data.ViewBox.y = 128-40
            data.map.x =  -(data.ViewBox.x)*24
            data.map.y = -(data.ViewBox.y)*24

def updateMiniMap(data):
    data.ViewBox.x = -data.map.x/24.0
    data.ViewBox.y = -data.map.y/24.0

def timerFired(data):
    data.mouseX, data.mouseY = pygame.mouse.get_pos()
    #print data.mouseX, data.mouseY
    print data.buttonStatus
    redrawAll(data)
    data.clock.tick(30)
    checkKeys(data)
    checkMiniMapScroll(data)
    updateMiniMap(data)
    checkAutoScroll(data)
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

def drawMenu(data):
    #print Menu_h
    #print ScreenHeight
    Menu_y = data.ScreenHeight - data.MenuHeight
    data.screen.blit(data.MenuImage,(0,Menu_y))
    data.screen.blit(data.map.mini_map,(40,795))

def redrawAll(data):

    data.map.resetMap()
    ProtossBuildings.ProtossBuilding.drawAllBuildings()
    Unit.Unit.drawAllUnits()
    data.map.draw(data.screen)
    if isinstance(data.selected,Unit.Unit):
        if data.selected.canMove:
            if data.buttonStatus[0] == 1:
                data.selected.drawMoves((0,200,0,100))
    #drawGrid(data)
    drawMenu(data)
    Menu.drawMenu(data.screen, data.selected)
    Unit.Unit.drawAllUnitsOnMiniMap()
    Building.building.drawAllBuildingsOnMiniMap()
    data.ViewBox.draw()
    #data.screen.blit(data.pointerImage, (data.mouseX, data.mouseY))
    pygame.display.flip()

def init(data):
    data.mode = 'run'


    data.ScreenHeight = data.screen.get_height()
    data.map = map.map('fastest', 64, 64,scale = 1.5)
    data.cellWidth, data.cellHeight = data.map.getCellsize()


    MenuFile = 'Other/Menu/Protoss Menu.png'
    data.MenuImage = load.load_image(MenuFile)
    Menu_h = data.MenuImage.get_height()
    data.MenuHeight = Menu_h

    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile)
    #pygame.mouse.set_visible(False)
    data.AutoScrollWidth = 20

    data.ViewBox = Menu.ViewBox(data.map)


    data.selected = None
    data.buttonStatus = [0]*9

    data.buildings = Building.building.buildings
    Building.building.setMap(data.map)
    Unit.Unit.setMap(data.map)
    Unit.Unit.setScreen(data.screen)
    data.zealot = ProtossUnit.Zealot(1,1)
    data.archon = ProtossUnit.Archon(3,3)
    data.darkTemplar = ProtossUnit.DarkTemplar(5,0)
    data.Dragoon = ProtossUnit.Dragoon(6,0)
    data.Arbiter = ProtossUnit.Arbiter(0,20)
    data.Probe = ProtossUnit.Probe(8,0)
    data.Nexus = ProtossBuildings.Nexus(20, 20)


def run():
    pygame.init()
    pygame.mixer.init()

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