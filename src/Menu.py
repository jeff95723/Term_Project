import pygame
from pygame import *

import load
import Unit
import Building

def drawMenu(screen,obj):
    if isinstance(obj,Unit.Unit) or isinstance(obj, Building.building):
        drawAvatar(screen, obj)
        drawIcon(screen,obj)
        drawText(screen, obj)

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
    elif 756 < x < 944 and 782 < y < 952:
        return 2
    elif 106<x<201 and 726<y<756:
        return 3
    elif 626<x<714 and 831<y<854:
        return 4

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
