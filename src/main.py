import pygame
from pygame.locals import *
from sys import exit


import load
import map

def mousePressed(data):
    row, col = mouse2RC(data)
    print row,col
    if data.board[row][col] == 0:
        data.board[row][col] = 1
        data.map.drawBlock(row, col)
    elif data.board[row][col] == 1:
        data.board[row][col] = 0
        data.map.undrawBlock(row,col)
    boardFile = 'board.txt'
    with open(boardFile,'w+') as data.f:
        data.f.write(str(data.board))

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

def checkMouse(data):
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

def redrawAll(data):

    data.screen.fill((0,0,0))
    data.map.draw(data.screen)
    data.screen.blit(data.pointerImage, (data.mouseX, data.mouseY))
    pygame.display.flip()

def init(data):
    data.mode = 'run'
    data.map = map.map('fastest.jpg', 64, 64,scale = 1.5)
    data.map.drawGrid()
    data.cellWidth, data.cellHeight = data.map.getCellsize()
    PointerFile = 'Other/Pointer.png'
    data.pointerImage = load.load_image(PointerFile)
    pygame.mouse.set_visible(False)
    data.AutoScrollWidth = 75

    data.board = [[0] * (data.map.cols) for i in xrange(data.map.rows)]


def run():
    pygame.init()

    class Struct:pass
    data = Struct()

    data.ViewSize = ( 960, 960)
    data.MenuSize = (data.ViewSize[0], 0)
    data.screen = pygame.display.set_mode((data.ViewSize[0],data.MenuSize[1] + data.ViewSize[1]),HWSURFACE)
    pygame.display.set_caption('Test')

    data.clock = pygame.time.Clock()
    init(data)
    while 1:
        if data.mode == 'quit':
            exit()
        timerFired(data)



run()