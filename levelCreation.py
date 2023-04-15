import pygame as pg
import tkinter as tk
from neededCode import Level, tileList, load

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

level = Level('Testing Level', 16, 16)

selectedTile = 0

def save():

    import serverClass

    levelServer = serverClass.Server('levelDB.db')

    levelServer.deleteTable('levels')

    levelServer.createTable('levels', ['ID','Name','xLength','yLength','BlockList'],['integer','text','integer','integer','text'],['primary key autoincrement','','','',''])

    saveList = []

    for x in range(len(level.tileList)):
        smallList = []
        for y in range(len(level.tileList[x])):
            smallList.append(level.tileList[x][y].object)
        saveList.append(smallList)

    print(saveList)

    levelServer.createRow('levels',['Name','BlockList'],[level.name,saveList])

import serverClass

levelServer = serverClass.Server('levelDB.db')

maxLevels = levelServer.getTable('levels')

loadSelect = 1

while play == True:

    screen.fill([0,0,0])

    if selectedTile > 0:
        leftBlockButton = pg.draw.rect(screen, [255, 255, 255], [width / 8 * 3, yPadding / 8, width / 16, yPadding / 4], 0, 5)
    
    pg.draw.rect(screen, tileList[selectedTile].color, [width / 8 * 4, yPadding / 8, width / 16, yPadding / 4], 5, 5)
    
    screen.blit(font.render(tileList[selectedTile].name, True, [255,255,255]), [width / 8 * 4, yPadding / 2])

    if selectedTile < len(tileList) - 1:
        rightBlockButton = pg.draw.rect(screen, [255, 255, 255], [width / 8 * 5, yPadding / 8, width / 16, yPadding / 4], 0, 5)
    
    saveButton = pg.draw.rect(screen, [0,255,0], [width / 8 * 3, height - yPadding / 2, width / 16, yPadding / 4], 0, 5)
    loadButton = pg.draw.rect(screen, [0,0,255], [width / 8 * 5, height - yPadding / 2, width / 16, yPadding / 4], 0, 5)

    blockList = []
    
    for xNum in range(len(level.tileList)):
        smallList = []
        for yNum in range(len(level.tileList[0])):

            smallList.append(pg.draw.rect(screen, tileList[level.tileList[xNum][yNum].object].color, [xPadding + (xNum * ((width - xPadding * 2)) / len(level.tileList)), yPadding + (yNum * ((height - yPadding * 2)) / len(level.tileList[0])), (width - xPadding * 2) / len(level.tileList), (height - yPadding * 2) / len(level.tileList[0])], 5))
        blockList.append(smallList)

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

            if saveButton.collidepoint(event.pos):
                save()

            elif loadButton.collidepoint(event.pos):
                load(loadSelect, level)

            for x in range(len(blockList)):
                for y in range(len(blockList[0])): 
                    if blockList[x][y].collidepoint(event.pos):

                        level.tileList[x][y].object = selectedTile

    pg.display.flip()

pg.quit()