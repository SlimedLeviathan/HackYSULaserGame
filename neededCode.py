import pygame as pg
import tkinter as tk

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.quit()

xPadding = 0
yPadding = 50

gameWidth = width - xPadding * 2
gameHeight = height - yPadding * 2

# I need to create a system where there is a grid of tiles
# Each tile has its own actual tile that occupies its area
class Tile:

    def __init__(self, object = 0):
        
        # is an instance of a class
        self.object = object

class Level:

    def __init__(self, xTiles, yTiles):

        self.tileList = [[Tile() for _ in range(yTiles)] for _ in range(xTiles)]

        self.laserList = []
        self.laserSurface = pg.Surface([width, height], pg.SRCALPHA)

        self.portalConnections = {}
        self.leverConnections = {}

        self.targets = {}
        self.laserBeams = {}
        self.singleMir = {}
        self.doubleMir = {}

    def changeDicts(self):

        for key, value in self.targets.items():
            self.targets.update({key : False})
        for key, value in self.laserBeams.items():
            self.laserBeams.update({key : value.direction})
        for key, value in self.singleMir.items():
            self.singleMir.update({key : value.direction})
        for key, value in self.doubleMir.items():
            self.doubleMir.update({key : value.direction})

level = Level(16,16)

blockLength = min(gameHeight / len(level.tileList[0]), gameWidth / len(level.tileList))

levelWidth = blockLength * len(level.tileList)
levelHeight = blockLength * len(level.tileList[0])

levelWidthPadding = ((gameWidth - levelWidth) / 2) + xPadding
levelHeightPadding = ((gameHeight - levelHeight) / 2) + yPadding

def load(number, level):
    import serverClass

    levelServer = serverClass.Server('levelDB.db')

    print(levelServer.executeQuery(f'SELECT BlockList, PortalConnections, LeverConnections, laserBeams, targets, singleMir, doubleMir FROM levels where number = {number} order by ID asc;'))
    
    results = levelServer.cursor.fetchall()

    results = results[-1]

    blockList = results[0]

    portalConnections = results[1]

    leverConnections = results[2]
    
    laserBeams = results[3]
    targets = results[4]
    singleMir = results[5]
    doubleMir = results[6]

    blockList = blockList[2:-2].split('], [')

    for listnum in range(len(blockList)):
        blockList[listnum] = blockList[listnum].split(', ')

        for num in range(len(blockList[listnum])):
            blockList[listnum][num] = Tile(object = int(blockList[listnum][num]))

    level.tileList = blockList

    if portalConnections != '{}':
        portalConnections = portalConnections[2:-2].split('], (')

        for dictnum in range(len(portalConnections)):
            portalConnections[dictnum] = portalConnections[dictnum].split('): [')

            for valuenum in range(len(portalConnections[dictnum])):
                portalConnections[dictnum][valuenum] = portalConnections[dictnum][valuenum].split(', ')

                for numnum in range(len(portalConnections[dictnum][valuenum])):
                    portalConnections[dictnum][valuenum][numnum] = int(portalConnections[dictnum][valuenum][numnum])

        portalDict = {}
        for dictnum in range(len(portalConnections)):

            portalDict.update({(portalConnections[dictnum][0][0],portalConnections[dictnum][0][1]):portalConnections[dictnum][1]})

        level.portalConnections = portalDict

    if leverConnections != '{}':
        leverConnections = leverConnections[2:-2].split('], (')

        for dictnum in range(len(leverConnections)):
            leverConnections[dictnum] = leverConnections[dictnum].split('): [')

            leverConnections[dictnum][0] = leverConnections[dictnum][0].split(', ')
            leverConnections[dictnum][1] = leverConnections[dictnum][1][1:-1].split('], [')

            for valuenum in range(len(leverConnections[dictnum][1])):
                leverConnections[dictnum][1][valuenum] = leverConnections[dictnum][1][valuenum].split(', ')

                for numnum in range(len(leverConnections[dictnum][1][valuenum])):
                    leverConnections[dictnum][1][valuenum][numnum] = int(leverConnections[dictnum][1][valuenum][numnum])

            for numnum in range(len(leverConnections[dictnum][0])):
                leverConnections[dictnum][0][numnum] = int(leverConnections[dictnum][0][numnum])

        leverDict = {}
        for dictnum in range(len(leverConnections)):

            leverDict.update({(leverConnections[dictnum][0][0],leverConnections[dictnum][0][1]):leverConnections[dictnum][1]})
        
        level.leverConnections = leverDict

    targetDict = {}
    if targets != '{}':
        targets = targets[1:-1].split(', (')
        for num in range(len(targets)):
            targets[num] = targets[num][1:-8].split(', ')
            targetDict.update({(int(targets[num][0]),int(targets[num][1])):Target()})

    level.targets = targetDict

    laserDict = {}

    if laserBeams != '{}':
        laserBeams = laserBeams[2:-1].split(', (')
        for num in range(len(laserBeams)):
            laserBeams[num] = laserBeams[num].split('): ')

            coords = laserBeams[num][0].split(', ')

            laserDict.update({(int(coords[0]),int(coords[1])):LaserBeam(direction = int(laserBeams[num][1]))})

    level.laserBeams = laserDict


    doubleMirDict = {}
    if doubleMir != '{}':
        doubleMir = doubleMir[2:-1].split(', (')
        for num in range(len(doubleMir)):
            doubleMir[num] = doubleMir[num].split('): ')

            coords = doubleMir[num][0].split(', ')


            doubleMirDict.update({(int(coords[0]),int(coords[1])):DoubleSidedMirror(direction = int(doubleMir[num][1]))})
    level.doubleMir = doubleMirDict
    
    singleMirDict = {}
    if singleMir != '{}':
        singleMir = singleMir[2:-1].split(', (')
        for num in range(len(singleMir)):
            singleMir[num] = singleMir[num].split('): ')

            coords = singleMir[num][0].split(', ')

            singleMirDict.update({(int(coords[0]),int(coords[1])):OneSidedMirror(direction = int(singleMir[num][1]))})
    level.singleMir = singleMirDict

class Air: # A empty tile

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\air.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])


    name = 'Air'

    color = [255,255,255]

    tileNum = 0

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(laser): # The laser can move through the block
        laser.move()

class Block: # A block tile

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\block.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'Block'

    color = [128,128,128]

    tileNum = 1

    def playerInteraction(level): # The player cant move thorugh the block
        return False

    def laserInteraction(laser): # The laser cant move through the block
        laser.stop()
    
class Glass: # A tile where light can go through but players cant

    name = 'Glass'

    color = [200,200,200]

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\glass.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])


    tileNum = 2

    def playerInteraction(level): # The player cant move thorugh the block
        return False

    def laserInteraction(laser): # The laser can move through the block
        laser.move()

class Smoke: # A tile where players can go through but light cant

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\smoke.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'Smoke'

    color = [75,75,75]

    tileNum = 3

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(laser): # The laser stops
        laser.stop()

class DoubleSidedMirror: # A tile that reflects lasers

    image0 = pg.Surface([blockLength, blockLength])
    image1 = pg.Surface([blockLength, blockLength])
    image0.blit(pg.transform.scale(pg.image.load('Images\\doubleMir0.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image1.blit(pg.transform.scale(pg.image.load('Images\\doubleMir1.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'DoubleSidedMirror'

    color = [0,0,255]

    tileNum = 4

    def __init__(self, direction = 0):
        self.direction = direction

    def playerInteraction(level): # The player cant move thorugh the block
        return False

    def laserInteraction(laser): # The laser changes direction by 90 degrees when interacting with this block
        laser.doubleMirror()

    def changeDirection(self):

        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 0
        
class OneSidedMirror: # A tile that reflects lasers

    image0 = pg.Surface([blockLength, blockLength])
    image1 = pg.Surface([blockLength, blockLength])
    image2 = pg.Surface([blockLength, blockLength])
    image3 = pg.Surface([blockLength, blockLength])
    image0.blit(pg.transform.scale(pg.image.load('Images\\singleMir0.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image1.blit(pg.transform.scale(pg.image.load('Images\\singleMir1.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image2.blit(pg.transform.scale(pg.image.load('Images\\singleMir2.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image3.blit(pg.transform.scale(pg.image.load('Images\\singleMir3.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'OneSidedMirror'

    color = [0,0,128]

    tileNum = 5

    def __init__(self, direction = 0):
        self.direction = direction

    def playerInteraction(level): # The player cant move thorugh the block
        return False

    def laserInteraction(laser): # The laser changes direction by 90 degrees when interacting with this block on the right side, ptherwise it gets stopped
        laser.singleMirror()

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

    image = pg.Surface([blockLength, blockLength])
    activatedImage = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\target.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    activatedImage.blit(pg.transform.scale(pg.image.load('Images\\targetActivated.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'Target'

    color = [255,0,0]

    tileNum = 6

    def __init__(self):
        self.active = False

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(laser): # The laser cant move thorugh the block, but it activates the target
        laser.hitTarget()

        image = pg.Surface([blockLength, blockLength])
        image.blit(pg.transform.scale(pg.image.load('Images\\targetActivated.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

class Lever: # A empty tile

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\lever.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'Lever'

    color = [165,42,42]

    tileNum = 7

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(laser): # The laser can move through the block
        laser.move()

    def flipLever(level, movingTilePos, endTilePos, defaultTile):
        if level.tileList[movingTilePos[0]][movingTilePos[1]].object == 0 and level.tileList[endTilePos[0]][endTilePos[1]].object != defaultTile:
            if tileList[level.tileList[endTilePos[0]][endTilePos[1]].object] == DoubleSidedMirror:
                level.doubleMir.update({(movingTilePos[0],movingTilePos[1]) : DoubleSidedMirror(direction = level.doubleMir[(endTilePos[0],endTilePos[1])].direction)})
                del level.doubleMir[(endTilePos[0],endTilePos[1])]


            elif tileList[level.tileList[endTilePos[0]][endTilePos[1]].object] == OneSidedMirror:
                level.singleMir.update({(movingTilePos[0],movingTilePos[1]) : OneSidedMirror(direction = level.singleMir[(endTilePos[0], endTilePos[1])].direction)})
                del level.singleMir[(endTilePos[0],endTilePos[1])]

            elif tileList[level.tileList[endTilePos[0]][endTilePos[1]].object] == LaserBeam:
                level.laserBeams.update({(movingTilePos[0],movingTilePos[1]) : LaserBeam(direction = level.laserBeams[(endTilePos[0], endTilePos[1])].direction)})
                del level.laserBeams[(endTilePos[0],endTilePos[1])]
            
            level.tileList[movingTilePos[0]][movingTilePos[1]].object = level.tileList[endTilePos[0]][endTilePos[1]].object
            level.tileList[endTilePos[0]][endTilePos[1]].object = defaultTile

        else:
            if tileList[level.tileList[movingTilePos[0]][movingTilePos[1]].object] == DoubleSidedMirror:
                level.doubleMir.update({(endTilePos[0],endTilePos[1]) : DoubleSidedMirror(direction = level.doubleMir[(movingTilePos[0],movingTilePos[1])].direction)})
                del level.doubleMir[(movingTilePos[0],movingTilePos[1])]

            elif tileList[level.tileList[movingTilePos[0]][movingTilePos[1]].object] == OneSidedMirror:
                level.singleMir.update({(endTilePos[0],endTilePos[1]) : OneSidedMirror(direction = level.singleMir[(movingTilePos[0],movingTilePos[1])].direction)})
                del level.singleMir[(movingTilePos[0],movingTilePos[1])]

            elif tileList[level.tileList[movingTilePos[0]][movingTilePos[1]].object] == LaserBeam:
                level.laserBeams.update({(endTilePos[0],endTilePos[1]) : LaserBeam(direction = level.laserBeams[(movingTilePos[0],movingTilePos[1])].direction)})
                del level.laserBeams[(movingTilePos[0],movingTilePos[1])]

            level.tileList[endTilePos[0]][endTilePos[1]].object = level.tileList[movingTilePos[0]][movingTilePos[1]].object
            level.tileList[movingTilePos[0]][movingTilePos[1]].object = 0

class LaserBeam:

    image0 = pg.Surface([blockLength, blockLength])
    image1 = pg.Surface([blockLength, blockLength])
    image2 = pg.Surface([blockLength, blockLength])
    image3 = pg.Surface([blockLength, blockLength])
    image0.blit(pg.transform.scale(pg.image.load('Images\\laserBeam0.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image1.blit(pg.transform.scale(pg.image.load('Images\\laserBeam1.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image2.blit(pg.transform.scale(pg.image.load('Images\\laserBeam2.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])
    image3.blit(pg.transform.scale(pg.image.load('Images\\laserBeam3.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'LaserBeam'

    color = [255,255,0]

    tileNum = 8

    def __init__(self, direction = 0):
        self.direction = direction

    def playerInteraction(level): # The player cant move through a laser beam block
        return False

    def laserInteraction(laser): # The laser wont go through the laser beam block
        laser.stop()

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

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\entry.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])


    tileNum = 9

    def playerInteraction(level): # The player can move through an entry way
        return True

    def laserInteraction(laser): # The laser wont go through the entry
        laser.stop()

class Exit:

    name = 'Exit'

    color = [0,255,0]

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\exit.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])


    tileNum = 10

    def playerInteraction(level): # The player can only interact with an exit after all the target blocks have been activated
        targetDone = 0

        for target in level.targets:
            if level.targets[target].active == True:
                targetDone += 1

        if targetDone == len(level.targets):
            return True
        
        else:
            return False

    def laserInteraciton(laser): # The laser wont go through the exit
        laser.stop()

class Portal:

    image = pg.Surface([blockLength, blockLength])
    image.blit(pg.transform.scale(pg.image.load('Images\\portal.png'),[blockLength,blockLength]),[0,0,blockLength,blockLength])

    name = 'Portal'

    color = [255,0,255]

    tileNum = 11

    def playerInteraction(level): # teleports player to the paired portal 
        return True

    def laserInteraction(laser): # teleports laser to the paired portal
        laser.portal()

tileList = [Air, Block, Glass, Smoke, DoubleSidedMirror, OneSidedMirror, Target, Lever, LaserBeam, Entry, Exit, Portal]
