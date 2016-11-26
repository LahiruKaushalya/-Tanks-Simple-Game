import pygame

CELL_WIDTH = 60
CELL_HEIGHT = 60

class WaterCell(pygame.sprite.Sprite):
    def __init__(self):
        super(WaterCell, self).__init__()
        self.image = pygame.image.load("water.jpg").convert()
        self.image = pygame.transform.scale(self.image,(CELL_WIDTH,CELL_HEIGHT))
