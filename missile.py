import math


class Missile:

    def __init__(self, sx, sy, kx, ky, ss, wait):
        self.start_x = sx
        self.start_y = sy
        self.end_x = kx
        self.end_y = ky
        self.current_x = self.start_x
        self.current_y = self.start_y
        self.speed = ss
        self.wait = wait

    def move(self):
        if self.wait == 0:
            dx = self.current_x - self.end_x
            dy = self.current_y - self.end_y
            pit = math.sqrt(dx*dx + dy*dy)
            self.current_x -= self.speed * dx / pit
            self.current_y -= self.speed * dy / pit
        else:
            self.wait = self.wait - 1

