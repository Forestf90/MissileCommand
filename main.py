import pygame
import sys
import random

from missile import Missile
from explosion import Explosion
from launcher import Launcher
import math 

width = 480
height = 480

pygame.init()

pygame.mouse.set_cursor(*pygame.cursors.diamond)

INFO = pygame.display.Info()


width = int(INFO.current_h * 0.4)
height = int(INFO.current_h * 0.4)

s = pygame.display.set_mode((width, height))
pygame.display.set_caption('Missile Command')
clock = pygame.time.Clock()

level = 0
shelter_positions = [35, 90, 140, 190, 240, 290, 340, 390, 445]
enemy_missiles = []
points = 0
player_missiles = []
explosion_list = []
shelter = [True, True, True, True, True, True]
launcher_list = [Launcher(0), Launcher(1), Launcher(2)]
launcher_positions = [30, width / 2, width - 30]
colors_list = [pygame.Color(0, 255, 0), pygame.Color(255, 0, 0), pygame.Color(255, 255, 0),
               pygame.Color(0, 255, 255), pygame.Color(255, 0, 255), pygame.Color(255, 255, 255),
               pygame.Color(0, 0, 255)]


def draw():
    s.fill((0, 0, 0))
    w = height - 50
    pygame.draw.rect(s, pygame.Color(255, 255, 0), (0, height-30, width, 30))
    for ss in range(len(launcher_list)):
        pygame.draw.polygon(s, pygame.Color(255, 255, 0),
                            [(ss*width/2-20 + 30 - (30*ss), w), (ss*width/2+20 + 30-(30*ss), w),
                             (ss*width/2+40+30 - (30*ss), height), (ss*width/2-40+30-(30*ss), height)])
        counter = launcher_list[ss].ammo
        number = 1
        while counter > 0:
            for j in range(number):
                pygame.draw.ellipse(s, (0, 0, 255), (launcher_positions[ss] + 8 - ((number - 2 * j) * 8), height - 55 + (number * 10), 5, 5))
                counter = counter-1
                if counter == 0:
                    break
            number = number+1
    launcher_pos = 1
    for i in range(len(shelter)):
        if shelter[i]:
            pygame.draw.rect(s, pygame.Color(0, 0, 255), ((i+launcher_pos)*50 + 30, height-40, 20, 20))
        if (i + 1) % 3 == 0:
            launcher_pos = launcher_pos+1
        
    for p in player_missiles:
        pygame.draw.line(s, pygame.Color(0, 255, 0), (p.start_x, p.start_y), (p.current_x, p.current_y), 1)
        pygame.draw.ellipse(s, random.choice(colors_list),
                            (p.current_x-1.5, p.current_y-1.5, 4, 4), 0)
        col = random.choice(colors_list)
        pygame.draw.line(s, col, (p.end_x-5, p.end_y-5),
                         (p.end_x+5, p.end_y+5), 1)
        pygame.draw.line(s, col, (p.end_x+5, p.end_y-5),
                         (p.end_x-5, p.end_y+5), 1)
        p.move()
        
    for p in enemy_missiles:
        pygame.draw.line(s, pygame.Color(255, 0, 0), (p.start_x, p.start_y), (p.current_x, p.current_y), 1)
        pygame.draw.ellipse(s, random.choice(colors_list),
                            (p.current_x-1.5, p.current_y-1.5, 4, 4), 0)

        p.move()
        
    for w in explosion_list:
        if w.wygasa:
            w.klatka -= 2
            if w.klatka == 0:
                explosion_list.remove(w)
                del w
                continue
        elif w.klatka == 1500:
            w.wygasa = True
        else:
            w.klatka += 1
        pygame.draw.ellipse(s, random.choice(colors_list),
                            (w.poz_x-w.klatka/60, w.poz_y-w.klatka/60, w.klatka/30, w.klatka/30), 0)
        
    pygame.display.update()


def designate_launcher(x, y):
    minimum_x = 10
    y1 = height-50
    dy = y-y1
    minimum = 100000
    if launcher_list[0].ammo > 0:
        x1 = 30
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    if launcher_list[1].ammo > 0:
        x1 = width/2
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    if launcher_list[2].ammo > 0:
        x1 = width-30
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    return minimum_x


def launch_rocket(x, y):
    if y > height-81:
        return
    
    launcher_position = designate_launcher(x, y)
    if launcher_position == 30:
        launcher_list[0].ammo -= 1
    elif launcher_position == width/2:
        launcher_list[1].ammo -= 1
    elif launcher_position == width-30:
        launcher_list[2].ammo -= 1
    else:
        return
    player_missiles.append(Missile(launcher_position, height - 50, x, y, 0.2, 0))


def middle_point(x, y, wx, wy, r):
    p = ((math.pow((x - wx), 2) // math.pow(r+1, 2)) + 
         (math.pow((y - wy), 2) // math.pow(r+1, 2))) 
  
    return p


def collision():
    for p in player_missiles:
        if p.current_y-p.end_y < 0.1:
            temp = Explosion(p.current_x, p.current_y)
            explosion_list.append(temp)
            player_missiles.remove(p)
            del p
            continue
        
        for w in explosion_list:
            if middle_point(p.current_x, p.current_y, w.poz_x, w.poz_y, w.klatka / 60) < 1:
                temp = Explosion(p.current_x, p.current_y)
                explosion_list.append(temp)
                player_missiles.remove(p)
                del p
                break
    for p in enemy_missiles:
        if p.current_y-p.end_y > -0.1:
            temp = Explosion(p.current_x, p.current_y)
            explosion_list.append(temp)
            if p.koniecx == shelter_positions[0]:
                launcher_list[0].ammo = 0
            elif p.koniecx == shelter_positions[1]:
                shelter[0] = False
            elif p.koniecx == shelter_positions[2]:
                shelter[1] = False
            elif p.koniecx == shelter_positions[3]:
                shelter[2] = False
            elif p.koniecx == shelter_positions[4]:
                launcher_list[1].ammo = 0
            elif p.koniecx == shelter_positions[5]:
                shelter[3] = False
            elif p.koniecx == shelter_positions[6]:
                shelter[4] = False
            elif p.koniecx == shelter_positions[7]:
                shelter[5] = False
            elif p.koniecx == shelter_positions[8]:
                launcher_list[2].ammo = 0
            lose()
            enemy_missiles.remove(p)
            del p
            continue
        
        for w in explosion_list:
            if middle_point(p.current_x, p.current_y, w.poz_x, w.poz_y, w.klatka / 60) < 1:
                temp = Explosion(p.current_x, p.current_y)
                explosion_list.append(temp)
                enemy_missiles.remove(p)
                del p
                break


def new_level():
    if not enemy_missiles:
        launcher_list[0].ammo = 10
        launcher_list[1].ammo = 10
        launcher_list[2].ammo = 10
        for i in range(10):
            temp = Missile(random.randrange(width), 0,
                           random.choice(shelter_positions), height - 30, 0.04, random.randrange(4000))
            enemy_missiles.append(temp)


def lose():
    for i in shelter:
        if i:
            return
    del explosion_list[:]
    del player_missiles[:]
    del enemy_missiles[:]
    global points
    draw()
    large_text = pygame.font.SysFont("consolas", int(height * 0.05))
    text_surface = large_text.render("Scored points : " + str(points) +
                                     " Press space to start again", True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = ((width/2), (height/2))
    s.blit(text_surface, text_rect)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    launcher_list[0].ammo = 10
                    launcher_list[1].ammo = 10
                    launcher_list[2].ammo = 10
                    shelter[0] = True
                    shelter[1] = True
                    shelter[2] = True
                    shelter[3] = True
                    shelter[4] = True
                    shelter[5] = True
                    points = 0
                    main()


def main():

    while True:
        collision()
        draw()
        new_level()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                launch_rocket(x, y)
#        clock.tick(120)


main()

