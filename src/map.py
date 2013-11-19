import pygame
from pygame.locals import *

import load

class map(object):

   def __init__(self, file, rows, cols, scale):
       self.image = load.load_image_smooth(fileName = 'maps/%s' %file, scale = scale)
       self.rows = rows
       self.cols = cols
       self.x = 0
       self.y = 0
       self.rect = pygame.Surface.get_rect(self.image)
       self.width,self.height = pygame.Surface.get_size(self.image)
       self.scale = scale
       self.display = pygame.display.get_surface()
       self.displayWidth, self.displayHeight = pygame.Surface.get_size(self.display)

   def draw(self, mainScreen):
       mainScreen.blit(self.image,(self.x,self.y))

   def move(self,(dx,dy)):
       self.x += dx
       self.y += dy
       if self.x > 0:
           self.x = 0
       elif self.x < -self.width + self.displayWidth:
           self.x = -self.width + self.displayWidth
       if self.y > 0:
           self.y = 0
       if self.y < -self.height + self.displayHeight:
           self.y = -self.height + self.displayHeight

   def getCellsize(self):
       return (self.width/self.cols, self.height/self.rows)

   def drawGrid(self):
       rows, cols = self.rows, self.cols
       cW, cH = self.getCellsize()
       for row in xrange(rows):
           pygame.draw.lines(self.image, (0,0,0),False, [(0,row * cH),(self.width,row * cH)])
       for col in xrange(cols):
           pygame.draw.lines(self.image, (0,0,0),False, [(col * cW, 0),(col * cW, self.height)])



################################################################################
# test
################################################################################
