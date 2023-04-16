import pygame as pg
import tkinter as tk
from neededCode import *

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.quit()

xPadding = 50
yPadding = 100

gameWidth = width - xPadding * 2
gameHeight = height - yPadding * 2

pg.init()

font = pg.font.Font('freesansbold.ttf',32)

play = True

screen = pg.display.set_mode()

level = Level(16, 16)

selectedTile = 0

def save():

    import serverClass

    levelServer = serverClass.Server('levelDB.db')

    levelServer.createTable('levels', ['ID','Number','BlockList','PortalConnections','LeverConnections','laserBeams','targets','singleMir','doubleMir'],['integer','integer','text','text','text','text','text','text','text'],['primary key autoincrement','','','','','','','',''])

    saveList = []

    for x in range(len(level.tileList)):
        smallList = []
        for y in range(len(level.tileList[x])):
            smallList.append(level.tileList[x][y].object)
        saveList.append(smallList)

    level.changeDicts()

    levelServer.createRow('levels',['Number','BlockList','PortalConnections','LeverConnections','laserBeams','targets','singleMir','doubleMir'],[loadSelect,saveList,level.portalConnections,level.leverConnections,level.laserBeams,level.targets,level.singleMir,level.doubleMir])

import serverClass

levelServer = serverClass.Server('levelDB.db')

levelServer.executeQuery('Select number from levels group by number')

maxLevels = len(levelServer.cursor.fetchall())

loadSelect = 1

placeTile = True
connectTile = False
connectingTile = False

while play == True:

    screen.fill([0,0,0])

    if selectedTile > 0:
        leftBlockButton = pg.draw.rect(screen, [255, 255, 255], [width / 8 * 3, yPadding / 8, width / 16, yPadding / 4], 0, 5)
    
    if placeTile == True:
        tileButton = pg.draw.rect(screen, tileList[selectedTile].color, [width / 8 * 4, yPadding / 8, width / 16, yPadding / 4], 0, 5)
    elif placeTile == False:
        tileButton = pg.draw.rect(screen, tileList[selectedTile].color, [width / 8 * 4, yPadding / 8, width / 16, yPadding / 4], 5, 5)
    
    screen.blit(font.render(tileList[selectedTile].name, True, [255,255,255]), [width / 8 * 4, yPadding / 2])

    if selectedTile < len(tileList) - 1:
        rightBlockButton = pg.draw.rect(screen, [255, 255, 255], [width / 8 * 5, yPadding / 8, width / 16, yPadding / 4], 0, 5)
    
    if connectTile == True:
        connectionButton = pg.draw.rect(screen, [0,255,0], [width / 8, yPadding / 8, width / 8, yPadding / 4], 0, 5)
    elif connectTile == False:
        connectionButton = pg.draw.rect(screen, [0,255,0], [width / 8, yPadding / 8, width / 8, yPadding / 4], 5, 5)
    
    screen.blit(font.render('Connect Tiles', True, [255,255,255]), [width / 8 - len('Connect Tiles') * 3, yPadding / 8 - 2])
    
    saveButton = pg.draw.rect(screen, [0,255,0], [width / 8 * 3, height - yPadding / 2, width / 16, yPadding / 4], 0, 5)
    
    if loadSelect > 1:
        loadLeftButton = pg.draw.rect(screen, [0,0,255], [width / 8 * 4, height - yPadding / 2, width / 16, yPadding / 4], 0, 5)
    
    loadButton = pg.draw.rect(screen, [0,0,255], [width / 8 * 5, height - yPadding / 2, width / 16, yPadding / 4], 0, 5)
    screen.blit(font.render(f'{loadSelect}', True, [255,255,255]), [width / 8 * 5 + width / 40, height - yPadding / 2 - 2])
    
    loadRightButton = pg.draw.rect(screen, [0,0,255], [width / 8 * 6, height - yPadding / 2, width / 16, yPadding / 4], 0, 5)

    blockList = []
    
    for xNum in range(len(level.tileList)):
        smallList = []
        for yNum in range(len(level.tileList[0])):

            smallList.append(pg.draw.rect(screen, tileList[level.tileList[xNum][yNum].object].color, [xPadding + (xNum * ((width - xPadding * 2)) / len(level.tileList)), yPadding + (yNum * ((height - yPadding * 2)) / len(level.tileList[0])), (width - xPadding * 2) / len(level.tileList), (height - yPadding * 2) / len(level.tileList[0])], 5))
        blockList.append(smallList)

    for key, value in level.portalConnections.items():
        pg.draw.line(screen,[255,0,255],[xPadding + (key[0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (key[1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2],[xPadding + (value[0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (value[1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2])

    for key, value in level.leverConnections.items():

        pg.draw.line(screen,[255,255,255],[xPadding + (key[0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (key[1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2],[xPadding + (value[0][0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (value[0][1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2])
        
        if connectingTile == False:
            pg.draw.line(screen,[0,255,0],[xPadding + (value[0][0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (value[0][1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2],[xPadding + (value[1][0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (value[1][1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2])

    if connectingTile == True:
        pg.draw.line(screen,[0,255,0],[xPadding + (startConnectPos[0] * ((width - xPadding * 2)) / len(level.tileList)) + ((width - xPadding * 2) / len(level.tileList)) / 2, yPadding + (startConnectPos[1] * ((height - yPadding * 2)) / len(level.tileList[0])) + ((height - yPadding * 2) / len(level.tileList[0])) / 2],pg.mouse.get_pos())

    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                play = False

        if event.type == pg.MOUSEBUTTONUP:
            if selectedTile > 0:
                if leftBlockButton.collidepoint(event.pos):
                    selectedTile -= 1
            
            if selectedTile < len(tileList) - 1:
                if rightBlockButton.collidepoint(event.pos):
                    selectedTile += 1
            
            if loadSelect > 1:
                if loadLeftButton.collidepoint(event.pos):
                    loadSelect -= 1
            
            if loadRightButton.collidepoint(event.pos):
                loadSelect += 1

            if saveButton.collidepoint(event.pos):
                save()

            elif loadButton.collidepoint(event.pos):
                load(loadSelect, level)

            elif connectionButton.collidepoint(event.pos):
                connectTile = True
                placeTile = False

            elif tileButton.collidepoint(event.pos):
                connectTile = False
                placeTile = True

            for x in range(len(blockList)):
                for y in range(len(blockList[0])): 
                    if blockList[x][y].collidepoint(event.pos):
                        if placeTile == True:
                            if selectedTile == level.tileList[x][y].object:
                                if tileList[selectedTile] == LaserBeam:
                                    level.laserBeams[(x,y)].changeDirection()
                                elif tileList[selectedTile] == DoubleSidedMirror:
                                    level.doubleMir[(x,y)].changeDirection()
                                elif tileList[selectedTile] == OneSidedMirror:
                                    level.singleMir[(x,y)].changeDirection()

                            else:
                                level.tileList[x][y].object = selectedTile

                                if tileList[selectedTile] == LaserBeam:
                                    level.laserBeams.update({(x,y):LaserBeam()})
                                elif tileList[selectedTile] == DoubleSidedMirror:
                                    level.doubleMir.update({(x,y):DoubleSidedMirror()})
                                elif tileList[selectedTile] == OneSidedMirror:
                                    level.singleMir.update({(x,y):OneSidedMirror()})
                                elif tileList[selectedTile] == Target:
                                    level.targets.update({(x,y):Target()})

                        if connectTile == True:
                            if connectingTile == False:
                                startingTile = tileList[level.tileList[x][y].object]
                                
                                if startingTile != Entry or startingTile != Exit:
                                    startConnectPos = [x,y]
                                    connectingTile = True

                            elif connectingTile == True:
                                startingTile = tileList[level.tileList[startConnectPos[0]][startConnectPos[1]].object]
                                clickedTile = tileList[level.tileList[x][y].object]

                                if startingTile == Portal:
                                    if clickedTile == Portal:

                                        level.portalConnections.update({(startConnectPos[0],startConnectPos[1]):[x,y]})
                                        
                                        connectingTile = False

                                elif startingTile == Lever:
                                    if clickedTile != Portal and clickedTile != Lever and clickedTile != Entry and clickedTile != Exit and clickedTile != Target:
                                        level.leverConnections.update({(startConnectPos[0],startConnectPos[1]):[[x,y],[None,None,None]]})

                                        firstStartConnectPos = startConnectPos
                                        startConnectPos = [x,y]


                                elif clickedTile != Portal and clickedTile != Lever and clickedTile != Entry and clickedTile != Exit and clickedTile != Target:
                                    
                                    startingTileMove = level.leverConnections[(firstStartConnectPos[0],firstStartConnectPos[1])][0]
                                    
                                    level.leverConnections.update({(firstStartConnectPos[0],firstStartConnectPos[1]):[startingTileMove,[x,y,level.tileList[x][y].object]]})

                                    connectingTile = False
    pg.display.flip()

pg.quit()