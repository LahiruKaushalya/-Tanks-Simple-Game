import pygame

CELL_WIDTH = 60
CELL_HEIGHT = 60

class GroundCell(pygame.sprite.Sprite):
    def __init__(self):
        super(GroundCell, self).__init__()
        self.image = pygame.image.load("ground.jpg").convert()
        self.image = pygame.transform.scale(self.image,(CELL_WIDTH,CELL_HEIGHT))
