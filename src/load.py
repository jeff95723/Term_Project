import pygame, os
from pygame.locals import *
'''Used for loading a file to pygame'''
pygame.mixer.init()

def load_image(fileName, scale = 1):
    '''Loads an image with transparency'''
    file = os.path.join('..','data', 'images', fileName)
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

def load_button(filename):
    '''Loads a button, returns a surface'''
    imagefile = 'Other/Buttons/' + filename
    image = load_image(imagefile,1)
    w,h = image.get_size()
    scale = 50.0/max(w,h)
    return load_image_smooth(imagefile,scale)

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

def load_avatar(fileName):
    imageName = 'Avatars/' + fileName
    return  load_image(imageName,1.2)


def load_sound(file):
    file = os.path.join('..','data', 'sound', file)
    try:
        if file[-8] != 'DS_Store':
            sound = pygame.mixer.Sound(file)
    except pygame.error:
        pygame.quit()
        raise SystemExit, 'Failed to load sound %s' %file
    return sound

def load_sounds(*files):
    snds = []
    for file in files:
        snds.append(load_sound(file))
    return snds

def load_sound_path(localPath):
    path = os.path.join('..','data','sound',localPath)
    files = os.listdir(path)
    result = []
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    for fileName in files:
        fileName = str(localPath) + (fileName)
        result.append(fileName)
    return result

def load_sounds_in_Folder(localPath):
    soundFileNames = load_sound_path(localPath)
    sounds = load_sounds(*soundFileNames)
    return sounds

def load_map_data(fileName):
    file = os.path.join('..', 'data', 'mapData',fileName)
    with open(file, 'r') as f:
        content = f.read()
    return eval(content)

