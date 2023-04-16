import pygame as pg
from levelCreation import createLevel
import tkinter as tk

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

xPadding = 50
yPadding = 100

root.quit()

pg.init()

font = pg.font.Font('freesansbold.ttf',32)
titlefont = pg.font.Font('freesansbold.ttf',32)

color = (255, 255, 255)
color_lighter = (170, 170, 170)
color_darker = (100, 100, 100)

def createButton(screen,name,xpos,ypos,xLength,yLength,mouse):
    buttonRect = pg.rect.Rect([xpos,ypos,xLength,yLength]) 

    if buttonRect.collidepoint(mouse): 
        button = pg.draw.rect(screen,color_lighter,[xpos,ypos,xLength,yLength]) 
          
    else: 
        button = pg.draw.rect(screen,color_darker,[xpos,ypos,xLength,yLength]) 

    screen.blit(font.render(name, True, color_lighter), (xpos,ypos)) 
    return button

creatingLevel = False

def mainMenu(screen):
    
    run = True
    creatingLevel = False

    if creatingLevel == True:
        pass

    elif creatingLevel == False:
        while run == True:
            screen.fill([0,0,0])

            mouse = pg.mouse.get_pos()

            screen.blit(font.render("Title", True, color_lighter), (width/2- len('Tittle') * 10,height/16)) 
            quitbutton = createButton(screen,'Quit',width/8*7,height/16*14,140,40,mouse)
            newLevelButton = createButton(screen,'Create Level',width/8*5,height/16*14,140,40,mouse)
            b1 = createButton(screen,'1',width/8,height/4,140,40,mouse)
            b2 = createButton(screen,'2',width/4,height/4,140,40,mouse)
            b3 = createButton(screen,'3',width/8*3,height/4,140,40,mouse)
            b4 = createButton(screen,'4',width/8*4,height/4,140,40,mouse)
            b5 = createButton(screen,'5',width/8*5,height/4,140,40,mouse)
            b6 = createButton(screen,'6',width/8*6,height/4,140,40,mouse)
            b7 = createButton(screen,'7',width/8,height/2,140,40,mouse)
            b8 = createButton(screen,'8',width/4,height/2,140,40,mouse)
            b9 = createButton(screen,'9',width/8*3,height/2,140,40,mouse)
            b10 = createButton(screen,'10',width/8*4,height/2,140,40,mouse)
            b11 = createButton(screen,'11',width/8*5,height/2,140,40,mouse)
            b12 = createButton(screen,'12',width/8*6,height/2,140,40,mouse)
            b13 = createButton(screen,'13',width/8,height/4*3,140,40,mouse)
            b14 = createButton(screen,'14',width/4,height/4*3,140,40,mouse)
            b15 = createButton(screen,'15',width/8*3,height/4*3,140,40,mouse)
            b16 = createButton(screen,'16',width/8*4,height/4*3,140,40,mouse)
            
            buttonList = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16]
            pg.display.flip()

            for en in pg.event.get():

                if en.type == pg.QUIT:
                    pg.quit()

                elif en.type == pg.MOUSEBUTTONUP:
                    if quitbutton.collidepoint(en.pos):
                        pg.quit()

                    elif newLevelButton.collidepoint(en.pos):
                        creatingLevel = True
                        createLevel(screen)

                    for buttonNum in range(len(buttonList)):
                        if buttonList[buttonNum].collidepoint(en.pos):
                            return buttonNum + 1
                        
                if en.type == pg.KEYUP:
                    if en.key == pg.K_ESCAPE:
                        pg.quit()