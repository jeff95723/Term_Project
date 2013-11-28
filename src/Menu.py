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

class ViewBox(object):
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.screen = screen

# Need to FINISH HERE
    def draw(self):
        pointList = [(self.x,self.y)]
        pygame.draw.lines(self.screen, (255,255,255),pointList)
