import pygame
from pygame.locals import *
from sys import exit


import load
import map

def mousePressed(data):
    pass

def checkKeys(data):
    keyStatus = pygame.key.get_pressed()
    if keyStatus[K_RIGHT] == 1:

        data.map.move((-30,0))
        #print 'Right Pressed'
    if keyStatus[K_LEFT] == 1:
        data.map.move((30,0))
        #print 'Left Pressed'
    if keyStatus[K_UP] == 1:
        data.map.move((0,30))
        #print 'Up Pressed'
    if keyStatus[K_DOWN] == 1:
        data.map.move((0,-30))
        #print 'Down Pressed'

def checkMouse(data):
    if data.mouseX < data.AutoScrollWidth and data.mouseY < data.AutoScrollWidth:
        data.map.move((30,30))

    elif data.mouseX < data.AutoScrollWidth and data.ViewSize[1] > data.mouseY > data.ViewSize[1] - data.AutoScrollWidth:
        data.map.move((30,-30))

    elif data.mouseX > data.ViewSize[0] - data.AutoScrollWidth and data.mouseY < data.AutoScrollWidth:
        data.map.move((-30,30))

    elif data.mouseX > data.ViewSize[0] - data.AutoScrollWidth and data.ViewSize[1] > data.mouseY > data.ViewSize[1] - data.AutoScrollWidth:
        data.map.move((-30,-30))

    elif data.mouseX < data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseY < data.ViewSize[1] - data.AutoScrollWidth):
            data.map.move((30,0))

    elif data.mouseX > data.ViewSize[0] - data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseY < data.ViewSize[1] - data.AutoScrollWidth):
            data.map.move((-30,0))

    elif data.mouseY < data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseX < data.ViewSize[0] - data.AutoScrollWidth):
            data.map.move((0,30))

    elif data.ViewSize[1] > data.mouseY > data.ViewSize[1] - data.AutoScrollWidth and (data.AutoScrollWidth< data.mouseX < data.ViewSize[0] - data.AutoScrollWidth):
            data.map.move((0,-30))




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

def redrawAll(data):

    data.screen.fill((0,0,0))
    data.map.draw(data.screen)
    data.screen.blit(data.pointerImage, (data.mouseX, data.mouseY))
    pygame.display.flip()

def init(data):
    data.mode = 'run'
    data.map = map.map('PamirPlateau.jpg', 128,128,scale = 1.5)
    data.cellWidth, data.cellHeight = data.map.getCellsize()
    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile)
    pygame.mouse.set_visible(False)
    data.AutoScrollWidth = 75


def run():
    pygame.init()

    class Struct:pass
    data = Struct()

    data.ViewSize = ( 960, 640)
    data.MenuSize = (data.ViewSize[0], 320)
    data.screen = pygame.display.set_mode((data.ViewSize[0],data.MenuSize[1] + data.ViewSize[1]),HWSURFACE)
    pygame.display.set_caption('Test')

    data.clock = pygame.time.Clock()
    init(data)
    print data.map.getCellsize()
    while 1:
        if data.mode == 'quit':
            exit()
        timerFired(data)



run()