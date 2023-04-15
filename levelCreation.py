import pygame as pg
import tkinter as tk

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

xPadding = 50
yPadding = 100

root.quit()

pg.init()

font = pg.font.Font('freesansbold.ttf',32)

play = True

screen = pg.display.set_mode()

# Each level has its own list of tiles
# All of the specific objects in a level will be set in a list in the level so that they can all be ran easily
class Level:

    def __init__(self, name, xTiles, yTiles):

        self.name = name

        self.tileList = [[Tile() for _ in range(yTiles)] for _ in range(xTiles)]

        self.targetList = []

# I need to create a system where there is a grid of tiles
# Each tile has its own actual tile that occupies its area
class Tile:

    def __init__(self, object = 0):
        
        # is an instance of a class
        self.object = object

class Air: # A empty tile

    name = 'Air'

    color = [255,255,255]

    tileNum = 0

    def playerInteraction(self): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser can move through the block
        pass

class Block: # A block tile

    name = 'Block'

    color = [128,128,128]

    tileNum = 1

    def playerInteraction(self): # The player cant move thorugh the block
        return False

    def laserInteraction(self, laser): # The laser cant move through the block
        pass
    
class Glass: # A tile where light can go through but players cant

    name = 'Glass'

    color = [200,200,200]

    tileNum = 2

    def playerInteraction(self): # The player cant move thorugh the block
        return False

    def laserInteraction(self, laser): # The laser can move through the block
        pass

class Smoke: # A tile where players can go through but light cant

    name = 'Smoke'

    color = [75,75,75]

    tileNum = 3

    def playerInteraction(self): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser stops
        pass

class DoubleSidedMirror: # A tile that reflects lasers

    name = 'DoubleSidedMirror'

    color = [0,0,255]

    tileNum = 4

    def __init__(self):
        self.direction = 0

    def playerInteraction(self): # The player cant move thorugh the block
        return False

    def laserInteraction(self, laser): # The laser changes direction by 90 degrees when interacting with this block
        pass

    def changeDirection(self):

        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 0
        
class OneSidedMirror: # A tile that reflects lasers

    name = 'OneSidedMirror'

    color = [0,0,128]

    tileNum = 5

    def __init__(self):
        self.direction = 0

    def playerInteraction(self): # The player cant move thorugh the block
        return False

    def laserInteraction(self, laser): # The laser changes direction by 90 degrees when interacting with this block on the right side, ptherwise it gets stopped
        pass

    def changeDirection(self):

        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 2
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 3:
            self.direction = 0

class Target: # A tile that unlocks the door

    name = 'Target'

    color = [255,0,0]

    tileNum = 6

    def __init__(self):
        self.active = False

        level.targetList.append(self)

    def playerInteraction(self): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser cant move thorugh the block, but it activates the target
        pass

class Lever: # A empty tile

    name = 'Lever'

    color = [165,42,42]

    tileNum = 7

    def __init__(self):

        self.active = False

        self.targetBlocks = []

    def playerInteraction(self): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser can move through the block
        pass

    def flipLever(self):
        if self.active == True:
            self.active = False

            for num in range(len(self.targetBlocks)):
                level.tileList[self.targetBlocks[num][1][0]][self.targetBlocks[num][1][1]].object = self.targetBlocks[num][0]
                level.tileList[self.targetBlocks[num][3][0]][self.targetBlocks[num][3][1]].object = Air()

        elif self.active == False:
            self.active = True

            for num in range(len(self.targetBlocks)):
                level.tileList[self.targetBlocks[num][3][0]][self.targetBlocks[num][3][1]].object = self.targetBlocks[num][0]
                level.tileList[self.targetBlocks[num][1][0]][self.targetBlocks[num][1][1]].object = self.targetBlocks[num][2]

    def changeTargetBlock(self, block, startPos, endPos):
        self.targetBlocks.append([block, startPos, level.tileList[endPos[0]][endPos[1]].object, endPos])

    def deleteTargetBlock(self, block):
        for num in range(len(self.targetBlocks)):
            if self.targetBlocks[num][0] == block:
                del self.targetBlocks[num]

class LaserBeam:

    name = 'LaserBeam'

    color = [255,255,0]

    tileNum = 8

    def __init__(self):
        self.direction = 0

    def playerInteraction(self): # The player cant move through a laser beam block
        return False

    def laserInteraciton(self, laser): # The laser wont go through the laser beam block
        pass

    def shootLaser(self): # shoots a laser in the direction it is facing
        pass

    def changeDirection(self):

        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 2
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 3:
            self.direction = 0

class Entry:

    name = 'Entry'

    color = [0,128,0]

    tileNum = 9

    def playerInteraction(self): # The player cant move through an entry way
        return True

    def laserInteraciton(self, laser): # The laser wont go through the entry
        pass

class Exit:

    name = 'Exit'

    color = [0,255,0]

    tileNum = 10

    def playerInteraction(self): # The player can only interact with an exit after all the target blocks have been activated
        done = False

        targetDone = 0

        for target in level.targetList:
            if target.active == True:
                targetDone += 1

        if targetDone == len(level.targetList):
            return True
        
        else:
            return False

    def laserInteraciton(self, laser): # The laser wont go through the exit
        pass

class Portal:

    name = 'Portal'

    color = [255,0,255]

    tileNum = 11

    def __init___(self):

        self.pairedPortal = None
        self.pairedPortalPos = None

        self.direction = 0

    def playerInteraction(self): # teleports player to the paired portal 
        return True

    def laserInteraction(self,laser): # teleports laser to the paired portal
        pass

    def pairPortal(self, portal, portalPos):
        
        self.pairedPortal = portal
        self.pairedPortalPos = portalPos

    def changeDirection(self):

        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 2
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 3:
            self.direction = 0

tileList = [Air, Block, Glass, Smoke, DoubleSidedMirror, OneSidedMirror, Target, Lever, LaserBeam, Entry, Exit, Portal]

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

def load(number):
    import serverClass

    levelServer = serverClass.Server('levelDB.db')

    levelServer.executeQuery(f'SELECT BlockList FROM levels where ID = {number};')

    blockList = levelServer.cursor.fetchall()[0][0]

    blockList = blockList[2:-2].split('], [')

    for listnum in range(len(blockList)):
        blockList[listnum] = blockList[listnum].split(', ')

        for num in range(len(blockList[listnum])):
            blockList[listnum][num] = Tile(object = int(blockList[listnum][num]))

    level.tileList = blockList


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
                load(loadSelect)

            for x in range(len(blockList)):
                for y in range(len(blockList[0])): 
                    if blockList[x][y].collidepoint(event.pos):

                        level.tileList[x][y].object = selectedTile

    pg.display.flip()

pg.quit()