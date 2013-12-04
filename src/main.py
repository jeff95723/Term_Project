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
                            data.map.resetFogOfWarBoard(data.currentPlayer.index)
                            data.currentPlayer.drawFogOfWar()
                    elif data.selected.canAttack:
                        if data.buttonStatus[1] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            print data.selected
                            data.selected.Attack(row,col)
                            data.map.resetFogOfWarBoard(data.currentPlayer.index)
                            data.currentPlayer.drawFogOfWar()
                else:
                    data.selected = None
            elif data.map.board[row][col] == 1:
                # if the previous selection is a unit, move that unit if possible
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canMove and data.selected.AirUnit:
                        if data.buttonStatus[0] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.move(row,col)
                            data.map.resetFogOfWarBoard(data.currentPlayer.index)
                            data.currentPlayer.drawFogOfWar()
                    elif data.selected.canAttack:
                        if data.buttonStatus[1] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.Attack(row,col)
                            data.map.resetFogOfWarBoard(data.currentPlayer.index)
                            data.currentPlayer.drawFogOfWar()
                else:
                    data.selected = None
            elif isinstance(data.map.board[row][col],Unit.Unit):
                # if the previously selected is a unit, attack if possible, else select the unit
                if isinstance(data.selected,Unit.Unit):
                    if data.selected.canAttack:
                        if data.buttonStatus[1] == 1 and data.buildMode == False\
                            and data.placeMode == False:
                            data.selected.Attack(row,col)
                            data.map.resetFogOfWarBoard(data.currentPlayer.index)
                            data.currentPlayer.drawFogOfWar()
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
                            data.map.resetFogOfWarBoard(data.currentPlayer.index)
                            data.currentPlayer.drawFogOfWar()
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
                if data.currentBuildClass.cost <= data.currentPlayer.resources:
                    data.currentBuildClass(mRow,mCol)
                    data.currentPlayer.resources -= data.currentBuildClass.cost
                    data.map.resetFogOfWarBoard(data.currentPlayer.index)
                    data.currentPlayer.drawFogOfWar()
                else:
                    print 'Not enough minerals'
                    data.currentPlayer.playSound(data.currentPlayer.NoMineralSound)
                data.currentBuildClass = None
                data.placeMode = False
                data.buildMode = False
                data.currentBuildIndex = None


    #update the button Status
    # MUST POST UPDATE, OTHERWISE THE UNITS WONT MOVE
    Menu.updateButtonStatus(data)

    # due to performance issues, update the fogofwar board only when the mouse if pressed.

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
        data.selected = None
        data.currentPlayer.xPos = data.map.x
        data.currentPlayer.yPos = data.map.y
        data.currentPlayer, data.otherPlayer = data.otherPlayer, data.currentPlayer
        data.currentPlayer.UntCls.nextRound()
        data.currentPlayer.BldCls.nextRound(data)
        data.currentPlayer.updateCurrentPopulation()
        data.currentPlayer.updateCurrentPopulationAvaliable()
        data.otherPlayer.addResources()
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
        data.selected = None
        data.currentPlayer.xPos = data.map.x
        data.currentPlayer.yPos = data.map.y
        data.currentPlayer, data.otherPlayer = data.otherPlayer, data.currentPlayer
        data.currentPlayer.UntCls.nextRound()
        data.currentPlayer.BldCls.nextRound(data)
        data.currentPlayer.updateCurrentPopulation()
        data.currentPlayer.updateCurrentPopulationAvaliable()
        data.otherPlayer.addResources()
        data.currentPlayer.drawFogOfWar()
        data.map.x = data.currentPlayer.xPos
        data.map.y = data.currentPlayer.yPos

def checkMenuClick(data):
    mouseStatus = pygame.mouse.get_pressed()
    if Menu.checkRegion(data) == 4 and mouseStatus[0] == 1:
        print 'menu clicked'
        if data.mode == 'run':
            data.mode = 'pause'
        elif data.mode == 'pause':
            data.mode = 'run'

def checkWin(data):
    if data.otherPlayer.Buildings == []:
        data.currentPlayer.playSound(data.currentPlayer.winSound)

def checkBuild(data):
    if isinstance(data.selected, Building.building):
        if data.selected in Building.building.finishedBuildings:
            index = None
            if data.selected.Build != []:
                for i in xrange(len(data.buttonStatus)):
                    if data.buttonStatus[i] == 1:
                        index = i

                if index != None:
                    if data.currentPlayer.resources >= data.selected.Build[index].cost:
                        data.currentPlayer.resources -= data.selected.Build[index].cost
                        data.selected.addQueue(index)
                    else:
                        print 'Not enough resources!!!'
                        data.currentPlayer.playSound(data.currentPlayer.NoMineralSound)
                    data.buttonStatus = [0] * 9

def checkStartMenuButtons(data):
    mouseStatus = pygame.mouse.get_pressed()
    region = Menu.checkStartRegion(data)
    if mouseStatus[0]  == 1:
        if region == 0:
            data.mode = 'run'
        elif region == 1:
            pass
        elif region == 2:
            # help
            pass
        elif region == 3:
            # credits
            pass
        elif region == 4:
            data.mode = 'quit'


def checkPauseButtons(data):
    mouseStatus = pygame.mouse.get_pressed()
    region = Menu.checkPauseRegion(data)
    if mouseStatus[0] == 1:
        if region == 0:
            pass
        elif  region == 1:
            # return to menu
            data.mode = 'start'
            data.frameCount = 0
        elif region == 2:
            data.mode = 'quit'
        elif region == 3:
            data.mode = 'run'

def updateMiniMap(data):
    data.ViewBox.x = -data.map.x/24.0
    data.ViewBox.y = -data.map.y/24.0

def timerFired(data):
    data.clock.tick(10)
    data.mouseX, data.mouseY = pygame.mouse.get_pos()
    data.MenuImage = data.currentPlayer.MenuImage
    Menu_h = data.MenuImage.get_height()
    data.MenuHeight = Menu_h
    redrawAll(data)
    checkMenuClick(data)
    if data.mode != 'pause':
        checkKeys(data)
        checkMiniMapScroll(data)
        checkNextRound(data)
        updateMiniMap(data)
        checkWin(data)
        checkBuild(data)
        checkAutoScroll(data)

    else:
        checkPauseButtons(data)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = 'quit'
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(data)

def startMenuTimerFired(data):
    data.mouseX, data.mouseY = pygame.mouse.get_pos()
    print data.mouseX, data.mouseY
    redrawAllForStartMenu(data,data.frameCount)
    checkStartMenuButtons(data)
    data.frameCount += 1

def redrawAllForStartMenu(data,frameCount):
    backGroundName = 'Other/backGround.png'
    buttonName = 'Other/buttons.png'
    exitButtonName = 'Other/exitButton.png'
    backGround = load.load_image(backGroundName)
    buttons = load.load_image(buttonName)
    exitButton = load.load_image(exitButtonName)
    exitX = 960
    exitY = 960
    buttonsX = 960
    buttonsY = 75
    data.screen.blit(backGround,(0,0))
    eX = exitX
    eY = exitY
    bX = buttonsX
    bY = buttonsY
    if frameCount >= 6 :
        eX = exitX - frameCount * 25
        eY = exitY - frameCount * 25
        bX = buttonsX - frameCount * 22

    if eX <= 960 - 379:
        eX = 960 - 379
    if eY <= 960 - 222:
        eY = 960 - 222
    if bX <= 960 - 424:
        bX = 960 - 424
    data.screen.blit(buttons,(bX,bY))
    data.screen.blit(exitButton,(eX,eY))

    if data.mode == 'credits':
        pass
    elif data.mode == 'help':
        pass



    pygame.display.flip()

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = 'quit'

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
    Menu.drawAllBuildingsOnMiniMap(data.screen,data)
    Menu.drawAllUnitsOnMiniMap(data.screen,data)
    data.map.drawFogOfWarOnMiniMap(data.screen,data.currentPlayer.index)
    data.ViewBox.draw()

    if data.mode == 'pause':
        data.screen.blit(data.pauseMenu,(180,150))
    pygame.display.flip()

def init(data):
    data.mode = 'start'

    data.frameCount = 0


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

    pMPic = 'Other/PauseMenu.png'
    data.pauseMenu = load.load_image(pMPic)

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



def run():
    pygame.init()
    pygame.mixer.init()

    class Struct:pass
    data = Struct()

    data.ViewSize = ( 960, 960)
    data.screen = pygame.display.set_mode((data.ViewSize),HWSURFACE)
    pygame.display.set_caption('Starcraft Tactics')

    data.clock = pygame.time.Clock()
    init(data)
    while 1:
        if data.mode == 'quit':
            exit()
        elif data.mode == 'start' or data.mode == 'help' or data.mode == 'credits':
            startMenuTimerFired(data)
        elif data.mode == 'run' or data.mode == 'pause':
            timerFired(data)


run()