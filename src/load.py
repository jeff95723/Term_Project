import pygame, os
from pygame.locals import *

def load_image(file):
    '''Loads an image with transparency'''
    file = os.path.join('..','data', 'images', file)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Image, "%s" not found' %(file)
    return image.convert_alpha()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_images(file))
    return imgs




#def load_images_alpha(*files):
#    imgs = []
#    for file in files:
#        imgs.append(load_images())