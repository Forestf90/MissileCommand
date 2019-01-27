# -*- coding: utf-8 -*-
import math

class rakieta:
    speed =0.2
    def __init__(self ,sx , sy ,kx ,ky):
        self.startx=sx
        self.starty=sy
        self.koniecx= kx
        self.koniecy=ky
        self.aktualnyx=self.startx
        self.aktualnyy=self.starty
        
    def ruch(self):
        dx = self.aktualnyx- self.koniecx
        dy = self.aktualnyy -self.koniecy
        pitg = math.sqrt(dx*dx + dy*dy)
        self.aktualnyx -= self.speed *dx/pitg
        self.aktualnyy -= self.speed * dy/pitg