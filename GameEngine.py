import pygame
from pygame.locals import *
from pygame.time import get_ticks
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
            #print updateData
            hasUpdate = True
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
key = comps[0]

if key == "PLAYERS_FULL":
    print "Server Full.wait....."
    sys.exit()
elif key == "GAME_ALREADY_STARTED":
    print "Game Started.Wait....."
    pygame.quit()
    sys.exit()
elif key == "ALREADY_ADDED":
    print "You Alredy Join."
    
board = Board()
board.init_board(comps)
board.draw_board()
board.cells.draw(screen)

WIDTH,HEIGHT = 60,60
tank = pygame.image.load("tank.png").convert_alpha()
tank = pygame.transform.scale(tank,(WIDTH,HEIGHT))
coin = pygame.image.load("coin.png").convert_alpha()
coin = pygame.transform.scale(coin,(WIDTH,HEIGHT))
life = pygame.image.load("life.jpg").convert_alpha()
life = pygame.transform.scale(life,(WIDTH,HEIGHT))
ground = pygame.image.load("ground.jpg").convert()
ground = pygame.transform.scale(ground,(WIDTH,HEIGHT))

x,y,start_d = 0,0,0
cur_d = start_d
newcor,times = [],{}
cur_time = pygame.time

while True:
    #clock.tick(FPS)
    angle = 0
    comps = updateData[:-1].split(":")
    key = comps[0]
    
    if key == "S":
        comps = comps[1].split(";")
        x,y,start_d= int(comps[1][0]),int(comps[1][2]),int(comps[2])
        X,Y = x*WIDTH,y*HEIGHT
        tank = pygame.transform.rotate(tank, start_d*-90)
        screen.blit(tank,(X,Y))
        pygame.display.update()
        
    elif key == "C":
        cx,cy,time,val = int(comps[1][0]),int(comps[1][2]),int(comps[2]),int(comps[3])
        screen.blit(coin,(cx*WIDTH,cy*WIDTH))
        times[time+cur_time.get_ticks()] = (cx*WIDTH,cy*WIDTH)
        pygame.display.update()
        
    elif key == "L":
        lx,ly,time = int(comps[1][0]),int(comps[1][2]),int(comps[2])
        screen.blit(life,(lx*WIDTH,ly*HEIGHT))
        times[time+cur_time.get_ticks()] = (lx*WIDTH,ly*WIDTH)
        pygame.display.update()
        
    for t in times.keys():
        if t <= cur_time.get_ticks():
            cor = times[t]
            screen.blit(ground,(cor[0],cor[1]))
            pygame.display.update()
            times.pop(t)
            
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                sc.send_message("UP#")
                new_d = 0
            elif event.key == pygame.K_RIGHT:
                sc.send_message("P0;RIGHT#")
                new_d = 1
            elif event.key == pygame.K_DOWN :
                sc.send_message("DOWN#")
                new_d = 2
            elif event.key == pygame.K_LEFT :
                sc.send_message("LEFT#")
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
    
