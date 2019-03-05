import pygame
from enum import Enum
from pygame.locals import *

class GridType(Enum):
    Empty = 0
    Wall = 1
    End = 2

# Constants

FPS = 30

SCREENSIZEX = 576
SCREENSIZEY = 576

GRIDSIZEX = 12
GRIDSIZEY = 12

GRIDENDPOS = (11, 11)

BOXSIZE = 48
BOXCOLOR = (0, 0, 0)

class Mouse:
    pos = None
    mouseImg = None
    
    def __init__(self):
        self.pos = [0, 0]
        self.mouseImg = pygame.image.load("mouse.png")
        self.mouseImg = pygame.transform.scale(self.mouseImg, (BOXSIZE-4, BOXSIZE-4))
        
    def reset(self):
        self.pos = [0, 0]
        
    def getPixelPos(self):
        return (self.pos[0]*BOXSIZE+2, self.pos[1]*BOXSIZE+2)
        
    def draw(self):
        pos = self.getPixelPos()
        display.blit(self.mouseImg, pos)
    


class GameState:
    grid = None
    myMouse = None
    
    def __init__(self, walls):
        self.initializeGrid(walls)
        self.myMouse = Mouse()
            
    def initializeGrid(self, walls):
        self.grid = []
        for y in range(GRIDSIZEY):
            row = []
            for x in range(GRIDSIZEX):
                if walls[y][x] == False:
                    row.append(GridType.Empty)
                else:
                    row.append(GridType.Wall)
            self.grid.append(row)
        self.grid[GRIDENDPOS[1]][GRIDENDPOS[0]] = GridType.End
    
    def draw(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pos = (x * BOXSIZE, y * BOXSIZE)
                
                if y == 0 and x == 0:
                    pygame.draw.rect(display, (128, 128, 255), [0,0,BOXSIZE,BOXSIZE], 0)
                if self.grid[y][x] == GridType.Empty:
                    pygame.draw.rect(display, BOXCOLOR, [pos[0], pos[1], BOXSIZE, BOXSIZE], 1)
                elif self.grid[y][x] == GridType.Wall:
                    pygame.draw.rect(display, BOXCOLOR, [pos[0], pos[1], BOXSIZE, BOXSIZE], 0)
                elif self.grid[y][x] == GridType.End:
                    pygame.draw.rect(display, (128, 255, 128), [pos[0], pos[1], BOXSIZE, BOXSIZE], 0)
                    pygame.draw.rect(display, BOXCOLOR, [pos[0], pos[1], BOXSIZE, BOXSIZE], 1)
        self.myMouse.draw()

def toggleWallAtPos(pos):
    gridPos = (int(pos[0]/BOXSIZE), int(pos[1]/BOXSIZE))
    if game.grid[gridPos[1]][gridPos[0]] == GridType.Empty:
        game.grid[gridPos[1]][gridPos[0]] = GridType.Wall
    elif game.grid[gridPos[1]][gridPos[0]] == GridType.Wall:
        game.grid[gridPos[1]][gridPos[0]] = GridType.Empty

# Returns array of True/False based on string
def getWalls(wallString):
    currentX = 0
    currentY = 0
    grid = []
    
    for y in range(GRIDSIZEY):
        row = []
        for x in range(GRIDSIZEX):
            row.append(False)
        grid.append(row)
        
    while len(wallString) > 0:
        char = wallString[0]
        wallString = wallString[1:len(wallString)]
        if char != "|":
            if char == "0":
                grid[currentY][currentX] = False
            else:
                grid[currentY][currentX] = True
            currentX += 1
            currentX %= GRIDSIZEX
            if currentX == 0:
                currentY += 1
    return grid

def printWalls():
    line = ""
    for y in range(len(game.grid)):
        line += "|"
        for x in range(len(game.grid[y])):
            if game.grid[y][x] == GridType.Empty:
                line += "0"
            elif game.grid[y][x] == GridType.Wall:
                line += "1"
            else:
                line += "2"
    print(line)


fpsClock = pygame.time.Clock()
display = pygame.display.set_mode((SCREENSIZEX, SCREENSIZEY))
wallStr = "001000101000|001000100000|001000101000|000000101111|111110100000|000000101110|000010101000|001010101010|001000000010|011111110010|001000000010|000000000012"
game = GameState(getWalls(wallStr))


while True:
    display.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        '''elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            toggleWallAtPos(pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                printWalls()'''
    
    
    
    game.draw()
    
    pygame.display.update()
    fpsClock.tick(FPS)