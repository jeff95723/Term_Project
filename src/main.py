import pygame
from pygame.locals import *
from sys import exit


import load


pygame.init()

screen = pygame.display.set_mode((1000,1000), 0 ,32)
background = pygame.Surface(screen.get_size())
background = background.convert()
pygame.display.set_caption("Hello World")
fileName = 'Units/Protoss/Archon.gif'
mouseCursor= load.load_image(fileName, 3)

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    background.fill((0,0,0))
    x,y = pygame.mouse.get_pos()
    x -= mouseCursor.get_width()/2
    y -= mouseCursor.get_width()/2

    screen.blit(background,(0,0))
    screen.blit(mouseCursor, (x,y))

    pygame.display.update()