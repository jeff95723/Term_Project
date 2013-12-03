import pygame
from pygame.locals import *
from sys import exit


import load
import map
import Building
import ProtossBuildings
import ProtossUnit

import TerranBuildings
import TerranUnit
import Unit
import Menu
import Player

def mousePressed(data):
    row, col = mouse2RC(data)
    mouseStatus = pygame.mouse.get_pressed()
    mouseRegion = Menu.checkRegion(data)

    # due to performance issues, update the fogofwar board only when the mouse if pressed.

    data.map.resetFogOfWarBoard(data.currentPlayer.index)
    data.currentPlayer.drawFogOfWar()
    # if in unit selection region
    if mouseRegion == 0:
        if mouseStatus[0] == 1:
            if data.map.board[row][col] == 0:
                # if the previous selection is a unit, move that unit if possible
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canMove:
                        if data.buttonStatus[0] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.move(row,col)
                    elif data.selected.canAttack:
                        if data.buttonStatus[1] == 1:# and data.buildMode == False:
                            data.selected.attack(row,col)
                else:
                    data.selected = None
            elif data.map.board[row][col] == 1:
                # if the previous selection is a unit, move that unit if possible
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canMove and data.selected.AirUnit:
                        if data.buttonStatus[0] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.move(row,col)
                    elif data.selected.canAttack:
                        if data.buttonStatus[1] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.attack(row,col)
                else:
                    data.selected = None
            elif isinstance(data.map.board[row][col],Unit.Unit):
                # if the previously selected is a unit, attack if possible, else select the unit
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canAttack:
                        if data.buttonStatus[1] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.Attack(row,col)
                        else:
                            data.selected = data.map.board[row][col]
                            data.selected.playSound(data.selected.idleSounds)
                    else:
                        data.selected = data.map.board[row][col]
                        data.selected.playSound(data.selected.idleSounds)
                else:
                    data.selected = data.map.board[row][col]
                    data.selected.playSound(data.selected.idleSounds)

            elif isinstance(data.map.board[row][col],Building.building):
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canAttack:
                        if data.buttonStatus[1] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.Attack(row,col)
                        else:
                            data.selected = data.map.board[row][col]
                            data.selected.playSound(data.selected.idleSounds)
                    else:
                        data.selected = data.map.board[row][col]
                        data.selected.playSound(data.selected.idleSounds)
                else:
                    data.selected = data.map.board[row][col]
                    data.selected.playSound(data.selected.idleSounds)
            else:
                data.selected = data.map.board[row][col]
        elif mouseStatus[2] == 1:
            data.selected = None

    if data.buildMode == True:
        if mouseRegion == 2:
            data.currentBuildIndex = Menu.getButtonStatus(data)
        if data.currentBuildIndex != None:
            data.placeMode = True

    if data.placeMode == True:
        if isinstance(data.selected,Unit.Unit):
            if mouseRegion == 0:
                mRow, mCol = mouse2RC(data)
                data.currentBuildClass(mRow,mCol)
                data.currentBuildClass = None
                data.placeMode = False
                data.buildMode = False
                data.currentBuildIndex = None


    #update the button Status
    # MUST POST UPDATE, OTHERWISE THE UNITS WONT MOVE
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
        data.currentPlayer.xPos = data.map.x
        data.currentPlayer.yPos = data.map.y
        data.currentPlayer, data.otherPlayer = data.otherPlayer, data.currentPlayer
        data.currentPlayer.drawFogOfWar()
        data.map.x = data.currentPlayer.xPos
        data.map.y = data.currentPlayer.yPos

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

def checkNextRound(data):
    mouseStatus = pygame.mouse.get_pressed()
    if Menu.checkRegion(data) == 3 and mouseStatus[0] == 1:
        print ' Next Round !'
        Building.building.nextRound()
        Unit.Unit.nextRound()
        data.currentPlayer.xPos = data.map.x
        data.currentPlayer.yPos = data.map.y
        data.currentPlayer, data.otherPlayer = data.otherPlayer, data.currentPlayer
        data.currentPlayer.drawFogOfWar()
        data.map.x = data.currentPlayer.xPos
        data.map.y = data.currentPlayer.yPos
        data.selected = None

def checkBuild(data):
    if isinstance(data.selected, Building.building):
        if data.selected in Building.building.finishedBuildings:
            index = None
            if data.selected.Build != []:
                for i in xrange(len(data.buttonStatus)):
                    if data.buttonStatus[i] == 1:
                        index = i

                if index != None:
                    data.selected.addQueue(index)
                    data.buttonStatus = [0] * 9

def updateMiniMap(data):
    data.ViewBox.x = -data.map.x/24.0
    data.ViewBox.y = -data.map.y/24.0

def timerFired(data):
    data.mouseX, data.mouseY = pygame.mouse.get_pos()
    data.MenuImage = data.currentPlayer.MenuImage #load.load_image(MenuFile)
    Menu_h = data.MenuImage.get_height()
    data.MenuHeight = Menu_h
    redrawAll(data)
    data.clock.tick(30)
    checkKeys(data)
    checkMiniMapScroll(data)
    checkNextRound(data)
    updateMiniMap(data)
    checkBuild(data)
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
    #ProtossBuildings.ProtossBuilding.drawAllBuildings()
    Building.building.drawAllBuildings()
    Unit.Unit.drawAllUnits()
    data.map.draw(data.screen)
    data.map.drawFogOfWar(data.screen,data.currentPlayer.index)
    if isinstance(data.selected,Unit.Unit):
        if data.buildMode == False and data.placeMode == False:
            if data.selected.canMove:
                if data.buttonStatus[0] == 1:
                    data.selected.drawMoves((0,200,0,100))

            if data.selected.canAttack:
                if data.buttonStatus[1] == 1:
                    data.selected.drawAttack((200,0,0,100))
    #drawGrid(data)
    drawMenu(data)
    Menu.drawMenu(data.screen, data.selected, data)
    #Unit.Unit.drawAllUnitsOnMiniMap()
    #Building.building.drawAllBuildingsOnMiniMap()
    Menu.drawAllBuildingsOnMiniMap(data.screen,data)
    Menu.drawAllUnitsOnMiniMap(data.screen,data)
    data.map.drawFogOfWarOnMiniMap(data.screen,data.currentPlayer.index)
    data.ViewBox.draw()
    pygame.display.flip()

def init(data):
    data.mode = 'run'


    data.ScreenWidth = data.screen.get_width()
    data.ScreenHeight = data.screen.get_height()
    data.map = map.map('fastest', 64, 64,scale = 1.5)
    data.cellWidth, data.cellHeight = data.map.getCellsize()


    data.buildings = Building.building.buildings
    Building.building.setMap(data.map)
    Unit.Unit.setMap(data.map)
    Unit.Unit.setScreen(data.screen)

    player1 = Player.player('Protoss', 8,9,0)
    player2 = Player.player('Terran', 53,51,1)

    data.currentPlayer = player1
    data.otherPlayer = player2

    #MenuFile = 'Other/Menu/Protoss Menu.png'
    data.MenuImage = data.currentPlayer.MenuImage #load.load_image(MenuFile)
    Menu_h = data.MenuImage.get_height()
    data.MenuHeight = Menu_h

    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile)
    #pygame.mouse.set_visible(False)
    data.AutoScrollWidth = 20

    data.ViewBox = Menu.ViewBox(data.map)

    data.buildMode = False
    data.placeMode = False
    data.currentBuildIndex = None
    data.currentBuildClass = None

    data.selected = None
    data.buttonStatus = [0]*9

    data.currentPlayer.drawFogOfWar()

'''
    data.Marine = TerranUnit.Marine(1,1)
    data.fb = TerranUnit.FireBat(2,2)
    data.tank = TerranUnit.SiegeTank(4,0)
    data.ghost = TerranUnit.Ghost(6,0)
    data.bc = TerranUnit.BattleCrusier(15,15)

    data.zealot = ProtossUnit.Zealot(1,1)
    data.archon = ProtossUnit.Archon(3,3)
    data.darkTemplar = ProtossUnit.DarkTemplar(5,0)
    data.Dragoon = ProtossUnit.Dragoon(6,0)
    data.Arbiter = ProtossUnit.Arbiter(0,20)
    data.Probe = ProtossUnit.Probe(8,0)
    data.Nexus = ProtossBuildings.Nexus(20, 20)
    '''


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