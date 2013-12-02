import pygame
from pygame import *

import load
import map
import Unit
import Building

def drawMenu(screen, obj, data):
    SmallFont= pygame.font.SysFont('monospace', 12, bold = True)
    InfoWhite = (255,255,255)
    nextRound = SmallFont.render('Next Round!', 1, InfoWhite)
    screen.blit(nextRound,(113,733))
    if isinstance(obj,Unit.Unit) or isinstance(obj, Building.building):
        drawAvatar(screen, obj)
        drawIcon(screen,obj)
        drawText(screen, obj)
        drawButtons(screen, obj, data)
        drawBuildBuilding(screen,data)

    if data.buildMode:
        print getButtonStatus(data)

def getMiniMapOrigin():
    return (40, 795)

def drawAvatar(screen, obj):
    image = obj.Avatar
    screen.blit(image,(628,868))

def drawIcon(screen, obj):
    image = obj.image
    imageW, imageH = image.get_size()
    scale = 75.0/max(imageW,imageH)
    icon = pygame.transform.smoothscale(image,(int(scale*imageW), int(scale*imageH)))
    screen.blit(icon, (235,835))

def drawText(screen, obj):
    Namefont = pygame.font.SysFont('monospace', 25, bold = True)
    SmallFont= pygame.font.SysFont('monospace', 15, bold = True)

    SheildBlue = (102,218,239)
    HealthGreen = (7,149,1)
    InfoWhite = (255,255,255)

    Namestring = str(type(obj))
    Namestring = Namestring.split('.')[-1][:-2]
    healthStr = str(obj.CURhealth) + '/' + str(obj.health)

    if isinstance(obj,Unit.Unit):
        MoveRangeStr = 'Move Range: ' + str(obj.MovRange)
        AttackRangeStr = 'Attack Range: ' + str(obj.AttRange)
        AttackStr = 'Attack: ' + str(obj.attack)
        MoveRange = SmallFont.render(MoveRangeStr, 1, InfoWhite)
        AttackRange = SmallFont.render(AttackRangeStr,1,InfoWhite)
        Attack = SmallFont.render(AttackStr,1,InfoWhite)
        screen.blit(MoveRange,(320,902))
        screen.blit(AttackRange,(320,915))
        screen.blit(Attack, (320,931))

        if obj.stealth:
            stealthStr = 'Stealth Unit'
            stealth = SmallFont.render(stealthStr,1, SheildBlue)
            screen.blit(stealth,(320,869))

    if isinstance(obj,Building.building):
        if obj in Building.building.finishedBuildings:
            if obj.buildQueue != []:
                buildQueueStr = str(obj.Build[obj.buildQueue[0]]).split('.')[-1][:-2]
                buildStr = 'Building: ' + buildQueueStr + ' and %d more.' %(len(obj.buildQueue)-1)
                roundLeft = obj.currentBuildRoundLeft[0]
                roundStr = 'Will finish %s in %d rounds.' %(buildQueueStr,roundLeft)
                round = SmallFont.render(roundStr,1,InfoWhite)
                screen.blit(round,(320,902))
            else:
                buildStr = 'Nothing is building right now.'
            build = SmallFont.render(buildStr,1,InfoWhite)
            screen.blit(build,(320,869))

    if obj.sheild != 0:
        sheildStr = str(obj.CURsheild)+'/'+str(obj.sheild)
        sheild= SmallFont.render(sheildStr,1,SheildBlue)
        screen.blit(sheild,(247,931))

    Name = Namefont.render(Namestring,1,InfoWhite)
    Health = SmallFont.render(healthStr,1,HealthGreen)
    screen.blit(Name,(358,830))
    screen.blit(Health,(247,918))

def drawMiniMapCell(screen,row, col,color):
    minimapCell = pygame.Surface((2,2))
    minimapCell.fill(color)
    cellW, cellH = minimapCell.get_size()
    mapX, mapY = getMiniMapOrigin()
    screen.blit(minimapCell,(mapX+col*cellW,mapY + row*cellH))

def drawButtons(screen, obj, data):
    if isinstance(obj,Unit.Unit):
        originX, originY = getButtonRegionOrigin()
        edgeX, edgeY = getButtonRegionEdge()
        cellW, cellH = (edgeX - originX)/3.0, (edgeY-originY)/3.0

        attackB = load.load_button('Attack.png')
        moveB = load.load_button('Move.png')
        build = load.load_button('Build.png')
        AdvancedBuild = load.load_button('AdvancedBuild.png')
        aRow,aCol = 0,1
        mRow,mCol = 0,0
        bRow,bCol = 2,0
        abRow, abCol = 2,1

        if obj.canAttack:
            screen.blit(attackB,(originX + aCol*cellW,originY+ aRow*cellH))

        if obj.canMove:
            screen.blit(moveB,(originX+mCol*cellW,originY + mRow*cellH))


        if obj.canBuild:
            screen.blit(build,(originX+bCol*cellW,originY + bRow*cellH))
            screen.blit(AdvancedBuild,(originX+abCol*cellW,originY + abRow*cellH))
            #if data.buildMode == False:
            if pygame.key.get_pressed()[K_b] == 1:
                data.buildMode = True
                menuImage = data.MenuImage

                x = originX
                y = originY - data.ScreenHeight + data.MenuHeight
                width = edgeX - originX
                height = edgeY - originY

                screen.blit(menuImage,(originX,originY),(x,y,width,height))
                originX, originY = getButtonRegionOrigin()
                edgeX, edgeY = getButtonRegionEdge()
                cellW, cellH = (edgeX - originX)/3.0, (edgeY-originY)/3.0

                for i in xrange(len(obj.Build)):
                    image = obj.Build[i].image
                    row = i/3
                    col = i%3
                    button = load.load_button_from_file(image)
                    screen.blit(button,(originX+col*cellW,originY+row*cellH))

            elif pygame.key.get_pressed()[K_v] == 1:
                data.buildMode = True
                menuImage = data.MenuImage

                x = originX
                y = originY - data.ScreenHeight + data.MenuHeight
                width = edgeX - originX
                height = edgeY - originY

                screen.blit(menuImage,(originX,originY),(x,y,width,height))
                originX, originY = getButtonRegionOrigin()
                edgeX, edgeY = getButtonRegionEdge()
                cellW, cellH = (edgeX - originX)/3.0, (edgeY-originY)/3.0

                for i in xrange(len(obj.AdvancedBuild)):
                    image = obj.AdvancedBuild[i].image
                    row = i/3
                    col = i%3
                    button = load.load_button_from_file(image)
                    screen.blit(button,(originX+col*cellW,originY+row*cellH))


            else:
                data.buildMode = False

    elif isinstance(obj, Building.building):
        if obj in Building.building.finishedBuildings:
            originX, originY = getButtonRegionOrigin()
            edgeX, edgeY = getButtonRegionEdge()
            cellW, cellH = (edgeX - originX)/3.0, (edgeY-originY)/3.0
            for i in xrange(len(obj.Build)):
                image = obj.Build[i].image
                row = i/3
                col = i%3
                button = load.load_button_from_file(image)
                screen.blit(button,(originX+col*cellW,originY+row*cellH))


def drawBuildBuilding(screen,data):
    if data.buildMode == True:
        x,y = data.mouseX, data.mouseY
        index = data.currentBuildIndex
        if index != None:
            cls = data.selected.Build[index]
            if pygame.key.get_pressed()[K_b] == 1:
                image = load.load_image_smooth(cls.image, cls.scale)
            elif pygame.key.get_pressed()[K_v] == 1:
                image = load.load_image_smooth(cls.image,cls.scale)
            cW,cH = data.map.getCellsize()
            mRow = data.mouseY/cH
            mCol = data.mouseX/cW
            sRow = data.map.y/cH
            sCol = data.map.x/cW
            sizeRow, sizeCol = cls.sizeRow, cls.sizeCol
            y = (mRow) * cH + cls.yerror
            x = (mCol) * cW + cls.xerror

            screen.blit(image,(x,y))

            redBlock = pygame.Surface((cW,cH),pygame.SRCALPHA)
            greenBlock = pygame.Surface((cW,cH),pygame.SRCALPHA)
            redBlock.fill((200,0,0,120))
            greenBlock.fill((0,200,0,120))
            for r in xrange(sizeRow):
                for c in xrange(sizeCol):
                    if (mRow+r-data.selected.row)**2 + (mCol+c-data.selected.col)**2 > 49 or \
                            (data.selected.Map.board[mRow-sRow+r][mCol-sCol+c] != 0 and\
                                    data.selected.Map.board[mRow-sRow+r][mCol-sCol+c] != 2):
                        screen.blit(redBlock,((mCol+c)*cW,(mRow+r)*cH))
                    else:
                        screen.blit(greenBlock,((mCol+c)*cW,(mRow+r)*cH))






def checkRegion(data):
    # 0 for the unit selection region, 1 for the minimap region,
    #2 for the order selection region, 3 for next round button region
    # 4 for pause button region
    x,y = data.mouseX, data.mouseY
    mMapx, mMapy = getMiniMapOrigin()
    if y < data.ScreenHeight - data.MenuHeight:
        return 0
    elif mMapx < x < mMapx + 128 and mMapy < y < mMapy + 128:
        return  1
    elif 753 < x < 944 and 779 < y < 952:
        return 2
    elif 106<x<201 and 726<y<756:
        return 3
    elif 626<x<714 and 831<y<854:
        return 4

def getButtonRegionOrigin():
    return (758,779)

def getButtonRegionEdge():
    return (960,960)

def updateButtonStatus(data):
    if checkRegion(data) == 2:
        x, y = data.mouseX, data.mouseY
        mouseStatus = pygame.mouse.get_pressed()
        originX, originY = getButtonRegionOrigin()
        edgeX, edgeY = getButtonRegionEdge()
        localX, localY = x-originX,y-originY
        cellW, cellH = (edgeX - originX)/3.0, (edgeY-originY)/3.0
        buttonStatus = [0] * 9
        i = int(localX/cellW) + 3*int(localY/cellH)
        if mouseStatus[0] == 1:
            buttonStatus[i] = 1
        else:
            buttonStatus = [0]*9
    else:
        buttonStatus = [0] * 9
    data.buttonStatus = buttonStatus

def getButtonStatus(data):

    if checkRegion(data) == 2:
        x, y = data.mouseX, data.mouseY
        mouseStatus = pygame.mouse.get_pressed()
        originX, originY = getButtonRegionOrigin()
        edgeX, edgeY = getButtonRegionEdge()
        localX, localY = x-originX,y-originY
        cellW, cellH = (edgeX - originX)/3.0, (edgeY-originY)/3.0
        buttonStatus = [0] * 9
        i = int(localX/cellW) + 3*int(localY/cellH)
        if mouseStatus[0] == 1:
            return i

class ViewBox(object):
    def __init__(self, map):
        self.x = 0
        self.y = 0
        self.screen = map.display
        self.map = map

    def draw(self):
        miniMapX, miniMapY = getMiniMapOrigin()
        drawX, drawY = miniMapX+self.x, miniMapY + self.y
        pointList = [(drawX,drawY),(drawX,drawY + 40),(drawX +40,drawY+40),(drawX + 40,drawY)]
        pygame.draw.lines(self.screen, (200,200,200),1,pointList, 1)
