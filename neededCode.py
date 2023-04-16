def load(number, level):
    import serverClass

    levelServer = serverClass.Server('levelDB.db')

    levelServer.executeQuery(f'SELECT BlockList, PortalConnections FROM levels where ID = {number};')
    results = levelServer.cursor.fetchall()[0]

    blockList = results[0]

    portalConnections = results[1]

    blockList = blockList[2:-2].split('], [')

    for listnum in range(len(blockList)):
        blockList[listnum] = blockList[listnum].split(', ')

        for num in range(len(blockList[listnum])):
            blockList[listnum][num] = Tile(object = int(blockList[listnum][num]))

    level.tileList = blockList

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

class Level:

    def __init__(self, name, xTiles, yTiles):

        self.name = name

        self.tileList = [[Tile() for _ in range(yTiles)] for _ in range(xTiles)]

        self.portalConnections = {}

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

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser can move through the block
        pass

class Block: # A block tile

    name = 'Block'

    color = [128,128,128]

    tileNum = 1

    def playerInteraction(level): # The player cant move thorugh the block
        return False

    def laserInteraction(self, laser): # The laser cant move through the block
        pass
    
class Glass: # A tile where light can go through but players cant

    name = 'Glass'

    color = [200,200,200]

    tileNum = 2

    def playerInteraction(level): # The player cant move thorugh the block
        return False

    def laserInteraction(self, laser): # The laser can move through the block
        pass

class Smoke: # A tile where players can go through but light cant

    name = 'Smoke'

    color = [75,75,75]

    tileNum = 3

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser stops
        pass

class DoubleSidedMirror: # A tile that reflects lasers

    name = 'DoubleSidedMirror'

    color = [0,0,255]

    tileNum = 4

    def __init__(self):
        self.direction = 0

    def playerInteraction(level): # The player cant move thorugh the block
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

    def playerInteraction(level): # The player cant move thorugh the block
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

    def __init__(self, level):
        self.active = False

        level.targetList.append(self)

    def playerInteraction(level): # The player can move thorugh the block
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

    def playerInteraction(level): # The player can move thorugh the block
        return True

    def laserInteraction(self, laser): # The laser can move through the block
        pass

    def flipLever(self, level):
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

    def changeTargetBlock(self, level, block, startPos, endPos):
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

    def playerInteraction(level): # The player cant move through a laser beam block
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

    def playerInteraction(level): # The player can move through an entry way
        return True

    def laserInteraciton(self, laser): # The laser wont go through the entry
        pass

class Exit:

    name = 'Exit'

    color = [0,255,0]

    tileNum = 10

    def playerInteraction(level): # The player can only interact with an exit after all the target blocks have been activated
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

    def playerInteraction(level): # teleports player to the paired portal 
        return True

    def laserInteraction(self,laser): # teleports laser to the paired portal
        pass

tileList = [Air, Block, Glass, Smoke, DoubleSidedMirror, OneSidedMirror, Target, Lever, LaserBeam, Entry, Exit, Portal]
