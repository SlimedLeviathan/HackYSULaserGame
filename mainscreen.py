import pygame as pg
import sys 
import tkinter as tk

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

xPadding = 50
yPadding = 100

root.quit()

pg.init()

screen = pg.display.set_mode()
font = pg.font.Font('freesansbold.ttf',32)
titlefont = pg.font.Font('freesansbold.ttf',32)

color = (255, 255, 255)
color_lighter = (170, 170, 170)
color_darker = (100, 100, 100)


def createButton(name,xpos,ypos,xLength,yLength):
    buttonRect = pg.rect.Rect([xpos,ypos,xLength,yLength]) 

    if buttonRect.collidepoint(mouse): 
        button = pg.draw.rect(screen,color_lighter,[xpos,ypos,xLength,yLength]) 
          
    else: 
        button = pg.draw.rect(screen,color_darker,[xpos,ypos,xLength,yLength]) 

    screen.blit(font.render(name, True, color_lighter), (xpos,ypos)) 
    return button
while True:
    mouse = pg.mouse.get_pos()

    screen.blit(font.render("Tittle", True, color_lighter), (width/2- len('Tittle') * 10,height/16)) 
    quitbutton = createButton('quit',width/8*7,height/16*14,140,40)
    button1 = createButton('1',width/8,height/4,140,40)
    button2 = createButton('2',width/4,height/4,140,40)
    button3 = createButton('3',width/8*3,height/4,140,40)
    button4 = createButton('4',width/8*4,height/4,140,40)
    button5 = createButton('5',width/8*5,height/4,140,40)
    button6 = createButton('6',width/8*6,height/4,140,40)
    button7 = createButton('7',width/8,height/2,140,40)
    button8 = createButton('8',width/4,height/2,140,40)
    button9 = createButton('9',width/8*3,height/2,140,40)
    button10 = createButton('10',width/8*4,height/2,140,40)
    button11 = createButton('11',width/8*5,height/2,140,40)
    button12 = createButton('12',width/8*6,height/2,140,40)
    button13 = createButton('13',width/8,height/4*3,140,40)
    button14 = createButton('14',width/4,height/4*3,140,40)
    button15 = createButton('15',width/8*3,height/4*3,140,40)
    button16 = createButton('16',width/8*4,height/4*3,140,40)
      

    for en in pg.event.get():

        if en.type == pg.QUIT:
            pg.quit()
        elif en.type == pg.MOUSEBUTTONDOWN:
            if quitbutton.collidepoint(en.pos):
                pg.quit()

      

    pg.display.update() 