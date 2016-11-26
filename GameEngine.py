import pygame
from pygame.locals import *
import sys
from board import Board
from socketclient import ServerClient
import SocketServer


pygame.init()
WIDTH,HEIGHT = 601,601
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
FPS = 24


hasUpdate = False
updateData = None

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global hasUpdate
        global updateData
        try:
            data = self.request.recv(1024)
            updateData = data
            hasUpdate = True
            print data
        except:
            print "Exception at server"
            

hasUpdate = False
updateData = None

     	
sc = ServerClient(ThreadedTCPRequestHandler)

sc.start_server()
sc.connect_client("127.0.0.1", 6000)
sc.send_message("JOIN#")

while not hasUpdate:
    pass

hasUpdate = False

comps = updateData[:-1].split(":")
print comps
playerNum = int(comps[1][1])


brickList = list()
for c in comps[2].split(";"):
    tmp = c.split(",")
    brickList.append((int(tmp[1]), int(tmp[0])))
    
stoneList=list()
for stone in comps[3].split(";"):
    tempo = stone.split(",")
    stoneList.append((int(tempo[1]),int(tempo[0])))
    
waterList=list()
for w in comps[4].split(";"):
    tempo = w.split(",")
    waterList.append((int(tempo[1]),int(tempo[0])))

board = Board()

board.set_terrain(brickList,-1)
board.set_terrain(stoneList,-2)
board.set_terrain(waterList,-3)
board.draw_board()

board.cells.draw(screen)
tank = pygame.image.load("tank.png").convert_alpha()
tank = pygame.transform.scale(tank,(60,60))
ground = pygame.image.load("ground.jpg").convert()
ground = pygame.transform.scale(ground,(60,60))

start_d = 2 #start direction.(server) 

tank = pygame.transform.rotate(tank, start_d*-90)
x,y= 5,5
X,Y = x*60,y*60
screen.blit(tank,(X,Y))

cur_d = start_d
newcor = []

while True:
    clock.tick(FPS)
    angle = 0
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == pygame.K_UP:  
                new_d = 0
            elif event.key == pygame.K_RIGHT:
                new_d = 1
            elif event.key == pygame.K_DOWN :
                new_d = 2
            elif event.key == pygame.K_LEFT :
                new_d = 3

            if new_d == cur_d:
                newcor = board.move_tank(cur_d,x,y)
                if x != newcor[0] or y != newcor[1]:
                    screen.blit(ground,(X,Y))
                    x,y,X,Y = newcor[0],newcor[1],newcor[2],newcor[3]
                    screen.blit(tank,(X,Y))
            else:
                screen.blit(ground,(X,Y))
                tank = pygame.transform.rotate(tank, (new_d - cur_d)*(-90))
                
            screen.blit(tank,(X,Y))
            
            cur_d = new_d
            
                
        pygame.display.update()
    
