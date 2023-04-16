import pygame
pg = pygame
from mainscreen import mainMenu, createButton
from neededCode import *

window = pg.display.set_mode()
Player_image = pg.image.load(r'Player_image.png')

red = [255,0,0]

class Laser:
    def __init__(self, x, y, direction):

        self.direction = direction
        self.x = x
        self.y = y

        middlePoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]
        topPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))]
        rightPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))+ blockLength / 2]
        downPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList))))+ blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength]
        leftPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))),(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]

        if direction == 0 and self.checkWalls() == True: # Up
            self.y -= 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, topPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)
        elif direction == 1 and self.checkWalls() == True: # Right
            self.x += 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, rightPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)
        elif direction == 2 and self.checkWalls() == True: # Down
            self.y += 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, downPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)
        elif direction == 3 and self.checkWalls() == True: # Left
            self.x -= 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, leftPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

    def checkWalls(self):
        if self.direction == 0 and self.y == -1:
            return False

        elif self.direction == 2 and self.y == len(level.tileList[0]) - 1:
            return False

        elif self.direction == 1 and self.x == len(level.tileList) - 1:
            return False

        elif self.direction == 3 and self.x == -1:
            return False
        
        else:
            return True

    def move(self):

        topPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))]
        rightPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))+ blockLength / 2]
        downPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList))))+ blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength]
        leftPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))),(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]

        if self.direction == 0 and self.checkWalls() == True: # Up
            self.y -= 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, downPoint, topPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)
        elif self.direction == 1 and self.checkWalls() == True: # Right
            self.x += 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, leftPoint, rightPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)
        elif self.direction == 2 and self.checkWalls() == True: # Down
            self.y += 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, topPoint, downPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)
        elif self.direction == 3 and self.checkWalls() == True: # Left
            self.x -= 1
            level.laserList.append(pg.draw.line(level.laserSurface, red, rightPoint, leftPoint, 5))
            tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

    def singleMirror(self):

        middlePoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]
        topPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))]
        rightPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))+ blockLength / 2]
        downPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList))))+ blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength]
        leftPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))),(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]

        direction = level.singleMir[(self.x,self.y)].direction

        if direction == 0:
            if self.direction == 1:
                self.direction = 0

                self.y -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, leftPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, topPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 2:
                self.direction = 3

                self.x -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, topPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, leftPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

        elif direction == 1:
            if self.direction == 2:
                self.direction = 1

                self.x += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, topPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, rightPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 3:
                self.direction = 0

                self.y -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, rightPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, topPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

        elif direction == 2:
            if self.direction == 0:
                self.direction = 1
                
                self.x += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, downPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, rightPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 3:
                self.direction = 2

                self.y += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, rightPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, downPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

        elif direction == 3:
            if self.direction == 0:
                self.direction = 3

                self.x -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, downPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, leftPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 1:
                self.direction = 2

                self.y += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, leftPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, downPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

    def doubleMirror(self):

        middlePoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]
        topPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))]
        rightPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))) + blockLength,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList))))+ blockLength / 2]
        downPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList))))+ blockLength / 2,(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength]
        leftPoint = [(levelWidthPadding + (self.x * (levelWidth / len(level.tileList)))),(levelHeightPadding + (self.y * (levelWidth / len(level.tileList)))) + blockLength / 2]

        direction = level.doubleMir[(self.x,self.y)].direction

        if direction == 0:
            if self.direction == 0:
                self.direction = 1

                self.x += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, downPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, rightPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 1:
                self.direction = 0

                self.y -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, leftPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, topPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 2:
                self.direction = 3

                self.x -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, topPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, leftPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 3:
                self.direction = 2

                self.y += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, rightPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, downPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

        if direction == 1: 
            if self.direction == 0:
                self.direction = 3

                self.x -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, downPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, leftPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 3:
                self.direction = 0

                self.y -= 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, rightPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, topPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 2:
                self.direction = 1

                self.x += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, topPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, rightPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

            elif self.direction == 1:
                self.direction = 2

                self.y += 1
                level.laserList.append(pg.draw.line(level.laserSurface, red, leftPoint, middlePoint, 5))
                level.laserList.append(pg.draw.line(level.laserSurface, red, middlePoint, downPoint, 5))
                tileList[level.tileList[self.x][self.y].object].laserInteraction(self)

    def portal(self):

        portal = level.portalConnections[(self.x, self.y)]

        self.x = portal[0]
        self.y = portal[1]

        self.move()

    def stop(self):
        pass

    def hitTarget(self):
        level.targets[(self.x,self.y)].active = True

class Player:
    def __init__(self, x = 100, y = 100):
        self.x = x
        self.y = y
        self.frame = 0
        self.health = 10
        self.isjummping = False
        self.falling = False
        self.jumpStart = None
        self.maxJump = 2
        self.teleporting = False
        self.flippingLever = False

    def jump(self):
        if self.isjummping == False and self.falling == False:
            self.isjummping = True

            self.jumpStart = int((playerRect.bottom - levelHeightPadding) / blockLength)

    def gravity(self): 
        playerBottomLeft = [playerRect.bottomleft[0] - levelWidthPadding,playerRect.bottomleft[1] - levelHeightPadding]            
        playerBottomRight = [playerRect.bottomright[0] - levelWidthPadding,playerRect.bottomright[1] - levelHeightPadding]            
    
        leftBlockCoords = [int(playerBottomLeft[0] / blockLength), int(playerBottomLeft[1] / blockLength)]
        rightBlockCoords = [int(playerBottomRight[0] / blockLength), int(playerBottomRight[1] / blockLength)] 

        self.falling = tileList[level.tileList[leftBlockCoords[0]][leftBlockCoords[1]].object].playerInteraction(level) and tileList[level.tileList[rightBlockCoords[0]][rightBlockCoords[1]].object].playerInteraction(level)

        if self.falling == True and self.isjummping == False:
            player.y += velocity
             
        elif self.isjummping == True:
            player.y -= velocity

            currentHeight = int((playerRect.bottom - levelHeightPadding) / blockLength)
            
            if currentHeight <= 0:
                self.y = levelHeightPadding

            elif self.jumpStart - self.maxJump > currentHeight or keysPressed[pg.K_SPACE] == False or not tileList[level.tileList[int((playerRect.left - levelWidthPadding) / blockLength)][currentHeight - 1].object].playerInteraction(level) or not tileList[level.tileList[int((playerRect.right - levelWidthPadding) / blockLength)][currentHeight - 1].object].playerInteraction(level):
                self.isjummping = False 

        playerCenter = [playerRect.center[0] - levelWidthPadding,playerRect.center[1] - levelHeightPadding]
        centerCoords = [int(playerCenter[0] / blockLength), int(playerCenter[1] / blockLength)]

        if tileList[level.tileList[centerCoords[0]][centerCoords[1]].object] == Portal:
            if self.teleporting == False:
                newCoords = level.portalConnections[centerCoords[0], centerCoords[1]]

                self.x = levelWidthPadding + (newCoords[0] * (levelWidth / len(level.tileList)))
                self.y = levelHeightPadding + (newCoords[1] * (levelHeight / len(level.tileList[0])))

                self.teleporting = True

        else:
            if self.teleporting == True:
                self.teleporting = False

velocity = 5

run = True

level = Level(16,16)

levelNumber = None

done = False

for xNum in range(len(level.tileList)):
        if done == True:
            break

        for yNum in range(len(level.tileList[xNum])):
            if tileList[level.tileList[xNum][yNum].object] == Entry:
                done = True
                x = xNum
                y = yNum
                break

def Reset():

    done = False
    
    load(levelNumber, level)
    
    for xNum in range(len(level.tileList)):
        for yNum in range(len(level.tileList[xNum])):
            if tileList[level.tileList[xNum][yNum].object] == Entry:
                x = xNum
                y = yNum
                global player
                player = Player(levelWidthPadding + (x * (levelWidth / len(level.tileList))), levelHeightPadding + (y * (levelHeight / len(level.tileList[0]))))

startMenu = True

while run == True:
    play = True
    if startMenu == True:

        levelNumber = mainMenu(window)
        
        if levelNumber != None:
            startMenu = False

            Reset()

    elif startMenu == False:

        soundtrack = pg.mixer.Sound('music.wav')
        
        soundtrack.play()
        
        while play == True:


            for target in level.targets:
                level.targets[target].active = False

            level.laserSurface = pg.Surface([width,height],pg.SRCALPHA)

            level.laserList = []

            window.fill([0,0,0])

            for key,value in level.laserBeams.items():
                Laser(key[0],key[1], value.direction)

            for xNum in range(len(level.tileList)):
                for yNum in range(len(level.tileList[0])):
                    if tileList[level.tileList[xNum][yNum].object] == OneSidedMirror or tileList[level.tileList[xNum][yNum].object] == DoubleSidedMirror or tileList[level.tileList[xNum][yNum].object] == LaserBeam:
                        if tileList[level.tileList[xNum][yNum].object] == OneSidedMirror:
                            direction = level.singleMir[(xNum,yNum)].direction

                        elif tileList[level.tileList[xNum][yNum].object] == DoubleSidedMirror:
                            direction = level.doubleMir[(xNum,yNum)].direction
                            
                        elif tileList[level.tileList[xNum][yNum].object] == LaserBeam:
                            direction = level.laserBeams[(xNum,yNum)].direction
                        
                        if direction == 0:
                            image = tileList[level.tileList[xNum][yNum].object].image0
                        elif direction == 1:
                            image = tileList[level.tileList[xNum][yNum].object].image1
                        elif direction == 2:
                            image = tileList[level.tileList[xNum][yNum].object].image2
                        elif direction == 3:
                            image = tileList[level.tileList[xNum][yNum].object].image3

                    elif tileList[level.tileList[xNum][yNum].object] == Target:
                        targetActive = level.targets[xNum,yNum].active

                        if targetActive == True:
                            image = tileList[level.tileList[xNum][yNum].object].activatedImage

                        else:
                            image = tileList[level.tileList[xNum][yNum].object].image
                        
                    else:
                        image = tileList[level.tileList[xNum][yNum].object].image

                    pg.rect.Rect([levelWidthPadding + (xNum * (levelWidth / len(level.tileList))), levelHeightPadding + (yNum * (levelHeight / len(level.tileList[0]))), blockLength, blockLength])
                    window.blit(image, [levelWidthPadding + (xNum * (levelWidth / len(level.tileList))), levelHeightPadding + (yNum * (levelHeight / len(level.tileList[0]))), blockLength, blockLength])

            playerRect = window.blit(pg.transform.scale(Player_image, [blockLength, blockLength]), (player.x, player.y))

            playerCenter = [playerRect.center[0] - levelWidthPadding,playerRect.center[1] - levelHeightPadding]
            centerCoords = [int(playerCenter[0] / blockLength), int(playerCenter[1] / blockLength)]
            
            player.gravity()

            keysPressed = pg.key.get_pressed()

            if tileList[level.tileList[int((playerRect.left - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object] == Exit:
                if keysPressed[pg.K_LEFT] and not tileList[level.tileList[int((playerRect.left - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object].playerInteraction(level) and int((playerRect.right - levelWidthPadding) / blockLength) > 0:
                    player.x -= velocity

                if keysPressed[pg.K_RIGHT] and tileList[level.tileList[int((playerRect.right - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object].playerInteraction(level) and int((playerRect.right - levelWidthPadding + 2) / blockLength) <= len(level.tileList) - 1:
                    player.x += velocity

            if tileList[level.tileList[int((playerRect.right - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object] == Exit:
                if keysPressed[pg.K_LEFT] and tileList[level.tileList[int((playerRect.left - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object].playerInteraction(level) and int((playerRect.right - levelWidthPadding) / blockLength) > 0:
                    player.x -= velocity
                
                if keysPressed[pg.K_RIGHT] and tileList[level.tileList[int((playerRect.right - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object].playerInteraction(level) and int((playerRect.right - levelWidthPadding + 2) / blockLength) <= len(level.tileList) - 1:
                    player.x += velocity

            else:
                if keysPressed[pg.K_LEFT] and tileList[level.tileList[int((playerRect.left - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object].playerInteraction(level) and int((playerRect.right - levelWidthPadding) / blockLength) > 0:
                    player.x -= velocity

                if keysPressed[pg.K_RIGHT] and tileList[level.tileList[int((playerRect.right - levelWidthPadding) / blockLength)][int((playerRect.bottom - levelHeightPadding) / blockLength) - 1].object].playerInteraction(level) and int((playerRect.right - levelWidthPadding + 2) / blockLength) <= len(level.tileList) - 1:
                    player.x += velocity

            if keysPressed[pg.K_SPACE]:
                player.jump()

            for laser in level.laserList:
                window.blit(level.laserSurface,[0,0,width,height])
            
            if keysPressed[pg.K_e] and tileList[level.tileList[centerCoords[0]][centerCoords[1]].object] == Lever:
                value = level.leverConnections[(centerCoords[0],centerCoords[1])]

                if player.flippingLever == False:
                    Lever.flipLever(level, value[0],value[1],value[1][2])
                    player.flippingLever = True

            else:
                player.flippingLever = False

            if tileList[level.tileList[centerCoords[0]][centerCoords[1]].object] == Exit:
                levelNumber += 1
                Reset()

            for laser in level.laserList:
                if playerRect.clipline((laser.bottomleft, laser.topright)):
                    Reset()

            mainMenuButton = createButton(window, 'Main Menu', width/16*14,height/16*15,140,40,pg.mouse.get_pos())

            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        play = False

                if event.type == pg.QUIT:
                    run = False
                    quit()

                if event.type == pg.MOUSEBUTTONUP:
                    if mainMenuButton.collidepoint(event.pos):
                        startMenu = True
                        play = False

            pg.display.flip()

pg.quit()

