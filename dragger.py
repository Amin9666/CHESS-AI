import pygame
from const import *

class Dragger: 
    
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos #(x, y)