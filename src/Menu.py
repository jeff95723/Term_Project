import pygame
from pygame import *

import load
import Unit
import Building

def drawMenu(screen,obj):
    if isinstance(obj,Unit.Unit) or isinstance(obj, Building.building):
        drawAvatar(screen, obj)

def getMiniMapOrigin():
    return (40, 795)

def drawAvatar(screen, obj):
    image = obj.Avatar
    screen.blit(image,(628,868))

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
