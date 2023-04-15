import pygame
pg = pygame 
from pygame.locals import *

window = pg.display.set_mode((600, 600))
Player_image = pg.image.load(r'Player_image.png')

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.frame = 0
        self.health = 10
        self.isjummping = False
        self.falling = False

    def jump(self):
        if self.isjummping is False:
            self.isjummping = True

    def gravity(self, object):  
        self.falling = object.playerInteraction()
        if self.falling == True and self.isjummping == False:
            player.y -= 1
        elif self.falling == False:
            pass


player = Player()


velocity = .5

run = True
while run :
    
    for event in pg.event.get():
        if event.type ==pg.QUIT:
            run = False
            quit()

    window.fill([0,0,0])
    #window.fill(225, 225, 225)
    window.blit(Player_image, (player.x, player.y))

    keysPressed = pg.key.get_pressed()

    jumpingCount = 2
    
    if keysPressed[pg.K_LEFT]:
        player.x -= velocity
    elif keysPressed[pg.K_RIGHT]:
        player.x += velocity 
    elif keysPressed[pg.K_SPACE]:
        player.jump()

    pg.display.flip()

pg.quit()




