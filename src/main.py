import pygame
from pygame.locals import *
from sys import exit


import load

pygame.init()

screen = pygame.display.set_mode((1000,1000), 0 ,32)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,250,250))
pygame.display.set_caption("Hello World")
fileName = 'Archon.gif'
mouseCursor= pygame.image.load(fileName).convert()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    #screen.blit(fill = 'black')
    x,y = pygame.mouse.get_pos()
    #x -= mouseCursor.get_width()/2
    #y -= mouseCursor.get_width()/2

    #screen.blit(mouseCursor, (x,y))

    pygame.display.update()