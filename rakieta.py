import math


class rakieta:

    def __init__(self, sx, sy, kx, ky, ss, czekaj):
        self.startx = sx
        self.starty = sy
        self.koniecx = kx
        self.koniecy = ky
        self.aktualnyx = self.startx
        self.aktualnyy = self.starty
        self.speed = ss
        self.czas = czekaj

    def ruch(self):
        if self.czas == 0:
            dx = self.aktualnyx - self.koniecx
            dy = self.aktualnyy - self.koniecy
            pitg = math.sqrt(dx*dx + dy*dy)
            self.aktualnyx -= self.speed * dx/pitg
            self.aktualnyy -= self.speed * dy/pitg
        else:
            self.czas = self.czas - 1

