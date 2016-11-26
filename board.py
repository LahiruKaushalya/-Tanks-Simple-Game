import pygame
from groundcell import GroundCell
from brickcell import BrickCell
from watercell import WaterCell
from stonecell import StoneCell

#these are the size of a cell in pixels
CELL_WIDTH = 60
CELL_HEIGHT = 60
NUM_ROWS = 10
NUM_COLS = 10

class Board():
    def __init__(self): 
        self.grid = [[0]*NUM_COLS for a in range(NUM_ROWS)]
        self.cells = pygame.sprite.Group()
        
    def set_terrain(self,coords,ttype):
        for cord in coords:
            self.grid[cord[0]][cord[1]] = ttype
    
    def draw_board(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if self.grid[i][j] == 0:
                    cell = GroundCell()
                elif self.grid[i][j] == -1:
                    cell = BrickCell()
                elif self.grid[i][j] == -2:
                    cell = StoneCell()
                elif self.grid[i][j] == -3:
                    cell = WaterCell()
                
                x = j*CELL_WIDTH
                y = i*CELL_HEIGHT
                
                cell.rect = pygame.Rect(x,y,CELL_WIDTH,CELL_HEIGHT)
                self.cells.add(cell)

    def move_tank(self,dire,i,j):
        if dire == 0 :
            if self.grid[i-1][j] == 0 and i != 0 :
                i -= 1
        elif dire == 1:
            if j != NUM_ROWS - 1 and self.grid[i][j+1] == 0:
                j += 1
        elif dire == 2:
            if i != NUM_COLS - 1 and self.grid[i+1][j] == 0:
                i += 1
        elif dire == 3:
            if self.grid[i][j-1] == 0 and j != 0:
                j -= 1
                
        x = j*CELL_WIDTH
        y = i*CELL_HEIGHT
                
        return [i,j,x,y]       

    
            
