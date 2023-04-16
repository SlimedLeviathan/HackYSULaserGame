import pygame
from neededCode import *
import tkinter as tk
pg = pygame
root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

class Laser:
    def __init__(self, direction):
        self.direction = direction 
        self.speed = 3
        