import pygame

CELL_WIDTH = 60
CELL_HEIGHT = 60

class BrickCell(pygame.sprite.Sprite):
    #this is how we write constructors in python
    def __init__(self):
        #IMPORTANT: that you call the super class constructor first
        super(BrickCell, self).__init__()
        #here use any texture you like for ground.png
        self.image = pygame.image.load("brick.jpg").convert()
        #once we load the image we scale is to suit the cell sie as we define
        self.image = pygame.transform.scale(self.image,(CELL_WIDTH,CELL_HEIGHT))
