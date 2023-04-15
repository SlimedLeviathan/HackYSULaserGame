import pygame
pg = pygame 
from pygame.locals import *

from neededCode import load, Level, tileList

import tkinter as tk
root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.quit()

xPadding = 0
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
        self.jumpStart = None
        self.jumpAmount = 0
        self.maxJump = 2

    def jump(self):
        if self.isjummping == False and self.falling == False:
            self.isjummping = True

            self.jumpStart = int((playerRect.bottom - levelHeightPadding) / blockLength)

    def gravity(self): 
        playerBottomLeft = [playerRect.bottomleft[0] - levelWidthPadding,playerRect.bottomleft[1] - levelHeightPadding]
        playerBottomRight = [playerRect.bottomright[0] - levelWidthPadding,playerRect.bottomright[1] - levelHeightPadding]
    
        leftBlockCoords = [int(playerBottomLeft[0] / blockLength), int(playerBottomLeft[1] / blockLength)]
        rightBlockCoords = [int(playerBottomRight[0] / blockLength), int(playerBottomRight[1] / blockLength)] 

        self.falling = tileList[level.tileList[leftBlockCoords[0]][leftBlockCoords[1]].object].playerInteraction() and tileList[level.tileList[rightBlockCoords[0]][rightBlockCoords[1]].object].playerInteraction()

        if self.falling == True and self.isjummping == False:
            player.y += 1
             
        elif self.isjummping == True:
            player.y -= 1

            print(int((playerRect.bottom - levelHeightPadding) / blockLength))

            if int((playerRect.bottom - levelHeightPadding) / blockLength) - self.jumpStart < self.jumpAmount:
                self.isjummping = False 

velocity = .5

run = True

level = Level('First Level',16,16)

load(1, level)

blockLength = min(gameHeight / len(level.tileList[0]), gameWidth / len(level.tileList))

levelWidth = blockLength * len(level.tileList)
levelHeight = blockLength * len(level.tileList[0])

levelWidthPadding = ((gameWidth - levelWidth) / 2) + xPadding
levelHeightPadding = ((gameHeight - levelHeight) / 2) + yPadding

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

player = Player(`levelWidthPadding + (x * (levelWidth / len(level.tileList))), yPadding + levelHeightPadding + (y * (levelHeight / len(level.tileList[0]))))

while run == True:

    window.fill([0,0,0])
    #window.fill(225, 225, 225)

    keysPressed = pg.key.get_pressed()

    jumpingCount = 2

    for xNum in range(len(level.tileList)):
        for yNum in range(len(level.tileList[0])):
            pg.draw.rect(window, tileList[level.tileList[xNum][yNum].object].color, [`levelWidthPadding + (xNum * (levelWidth / len(level.tileList))), yPadding + levelHeightPadding + (yNum * (levelHeight / len(level.tileList[0]))), blockLength, blockLength])
    
    playerSurface = pg.Surface([blockLength,blockLength])

    playerSurface.blit(pg.transform.scale(Player_image, [blockLength, blockLength]),[0,0])
    playerRect = window.blit(playerSurface, (player.x, player.y))

    player.gravity()

    if keysPressed[pg.K_LEFT]:
        player.x -= velocity
    if keysPressed[pg.K_RIGHT]:
        player.x += velocity 
    if keysPressed[pg.K_SPACE]:
        player.jump()

    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                run = False

        if event.type ==pg.QUIT:
            run = False
            quit()

    pg.display.flip()

pg.quit()




