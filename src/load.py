import pygame, os
from pygame.locals import *
'''Used for loading a file to pygame'''

def load_image(fileName, scale = 1):
    '''Loads an image with transparency'''
    file = os.path.join('..','data', 'images','', fileName)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        pygame.quit()
        raise SystemExit, 'Image, "%s" not found' %(fileName)

    image = pygame.transform.scale(image.convert_alpha(), ((int(scale*image.get_width())),
                                   int(scale*image.get_height())))
    return image

def load_image_smooth(fileName, scale = 1):
    '''Loads an image with smooth scaling'''
    file = os.path.join('..', 'data', 'images', fileName)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        pygame.quit()
        raise SystemExit, "Image, %s not found" %(fileName)
    image = pygame.transform.smoothscale(image.convert_alpha(),((int(scale*image.get_width())),
                                                                int(scale*image.get_height())))

    return image

def load_dumb(fileName):
    file = os.path.join('..', 'data', 'images', fileName)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        pygame.quit()
        raise SystemExit, "Image, %s not found" %(fileName)
    return image.convert()



def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_images(file))
    return imgs


def load_images_alpha(*files):
    imgs = []
    for file in files:
        imgs.append(load_images())


def load_sound(file):
    file = os.path.join('..','data', 'images', file)
    try:
        sound = pygame.mixer.Sound(file)
    except pygame.error:
        pygame.quit()
        raise SystemExit, 'Failed to load sound %s' %file
    return sound

