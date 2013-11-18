import pygame
from pygame.locals import *
from sys import exit


import load

def mousePressed(data):
    pass

def checkKeys(data):
    keyStatus = pygame.key.get_pressed()
    if keyStatus[K_RIGHT] == 1:
        moveMap(data, (-30,0))
        #print 'Right Pressed'
    if keyStatus[K_LEFT] == 1:
        moveMap(data, (30,0))
        #print 'Left Pressed'
    if keyStatus[K_UP] == 1:
        moveMap(data, (0,30))
        #print 'Up Pressed'
    if keyStatus[K_DOWN] == 1:
        moveMap(data, (0,-30))
        #print 'Down Pressed'

def checkMouse(data):
    if data.mouseX < 100 and data.mouseY < 100:
        moveMap(data, (30,30))

    elif data.mouseX < 100 and data.mouseY > data.screenSize[1] - 100:
        moveMap(data, (30,-30))

    elif data.mouseX > data.screenSize[0] - 100 and data.mouseY < 100:
        moveMap(data, (-30,30))

    elif data.mouseX > data.screenSize[0] - 100 and data.mouseY > data.screenSize[1] - 100:
        moveMap(data, (-30,-30))

    elif data.mouseX < 100 and (100< data.mouseY < data.screenSize[1] - 100):
            moveMap(data, (30,0))

    elif data.mouseX > data.screenSize[0] - 100 and (100< data.mouseY < data.screenSize[1] - 100):
            moveMap(data, (-30,0))

    elif data.mouseY < 100 and (100< data.mouseX < data.screenSize[0] - 100):
            moveMap(data, (0,30))

    elif data.mouseY > data.screenSize[1] - 100 and (100< data.mouseX < data.screenSize[0] - 100):
            moveMap(data, (0,-30))



def moveMap(data,(dx,dy)):
    data.mapX += dx
    data.mapY += dy
    if data.mapX > 0:
        data.mapX = 0
    elif data.mapX < -4096:
        data.mapX = -4096
    if data.mapY > 0:
        data.mapY = 0
    if data.mapY < -4096:
        data.mapY = -4096





def timerFired(data):
    data.mouseX, data.mouseY = pygame.mouse.get_pos()
    redrawAll(data)
    data.clock.tick(50)
    checkKeys(data)
    checkMouse(data)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = 'quit'

def redrawAll(data):

    data.screen.fill((0,0,0))
    data.screen.blit(data.map,(data.mapX,data.mapY))
    data.screen.blit(data.pointerImage, (data.mouseX, data.mouseY))
    pygame.display.flip()

def init(data):
    data.mode = 'run'
    data.mapFileName = 'maps/PamirPlateau.jpg'
    data.map = load.load_image_smooth(data.mapFileName, 1.5)
    data.mapX = 0
    data.mapY = 0
    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile,1)
    pygame.mouse.set_visible(False)

def run():
    pygame.init()

    class Struct:pass
    data = Struct()

    data.screenSize = (1000,1000)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption('Test')

    data.clock = pygame.time.Clock()
    init(data)
    timerFired(data)
    while 1:
        if data.mode == 'quit':
            exit()
        timerFired(data)


run()