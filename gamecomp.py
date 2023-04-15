import pygame
pg = pygame 
from pygame.locals import *

from neededCode import load, Level, tileList

import tkinter as tk
root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.quit()

xPadding = 50
yPadding = 100

gameWidth = width - xPadding * 2
gameHeight = height - yPadding * 2

window = pg.display.set_mode()
Player_image = pg.image.load(r'Player_image.png')

class Player:
    def __init__(self, x = 100, y = 100):
        self.x = x
        self.y = y
        self.frame = 0
        self.health = 10
        self.isjummping = False
        self.falling = False

    def jump(self):
        if self.isjummping is False:
            self.isjummping = True

    def gravity(self): 
        playerBottomLeft = [playerRect.bottomleft[0] - levelWidthPadding,playerRect.bottomleft[1] + 1]
        playerBottomRight = [playerRect.bottomright[0] - levelWidthPadding,playerRect.bottomright[1] + 1]
    
        leftBlockCoords = [int(playerBottomLeft[0] / blockLength), int(playerBottomLeft[1] / blockLength)]
        rightBlockCoords = [int(playerBottomRight[0] / blockLength), int(playerBottomRight[1] / blockLength)] 

        self.falling = tileList[level.tileList[leftBlockCoords[0]][leftBlockCoords[1]].object].playerInteraction() or tileList[level.tileList[rightBlockCoords[0]][rightBlockCoords[1]].object].playerInteraction()

        if self.falling == True and self.isjummping == False:
            player.y += 1
        elif self.falling == False:
            pass

velocity = .5

run = True

level = Level('First Level',16,16)

load(1, level)

blockLength = min(height / len(level.tileList[0]), width / len(level.tileList))

levelWidth = blockLength * len(level.tileList)
levelHeight = blockLength * len(level.tileList[0])

levelWidthPadding = (gameWidth - levelWidth) / 2
levelHeightPadding = (gameHeight - levelHeight) / 2

done = False

for xNum in range(len(level.tileList)):
    if done == True:
        break

    for yNum in range(len(level.tileList[xNum])):
        if level.tileList[xNum][yNum].object == 9:
            done = True
            x = xNum
            y = yNum
            break

player = Player(xPadding + levelWidthPadding + (x * (levelWidth / len(level.tileList))), yPadding + levelHeightPadding + (y * (levelHeight / len(level.tileList[0]))))

while run == True:
    
    for event in pg.event.get():
        if event.type ==pg.QUIT:
            run = False
            quit()

    window.fill([0,0,0])
    #window.fill(225, 225, 225)

    keysPressed = pg.key.get_pressed()

    jumpingCount = 2

    for xNum in range(len(level.tileList)):
        for yNum in range(len(level.tileList[0])):
            pg.draw.rect(window, tileList[level.tileList[xNum][yNum].object].color, [xPadding + levelWidthPadding + (xNum * (levelWidth / len(level.tileList))), yPadding + levelHeightPadding + (yNum * (levelHeight / len(level.tileList[0]))), blockLength, blockLength])
    
    playerSurface = pg.Surface([blockLength,blockLength])

    playerSurface.blit(pg.transform.scale(Player_image, [blockLength, blockLength]),[0,0])
    playerRect = window.blit(playerSurface, (player.x, player.y))

    player.gravity()

    if keysPressed[pg.K_LEFT]:
        player.x -= velocity
    elif keysPressed[pg.K_RIGHT]:
        player.x += velocity 
    elif keysPressed[pg.K_SPACE]:
        player.jump()

    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                run = False

    pg.display.flip()

pg.quit()




