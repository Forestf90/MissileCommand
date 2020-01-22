import pygame
import sys
import random

from missile import Missile
from explosion import Explosion
from launcher import Launcher
import math 

# width = 480
# height = 480

pygame.init()

pygame.mouse.set_cursor(*pygame.cursors.diamond)

INFO = pygame.display.Info()


WIDTH = int(INFO.current_h * 0.5)
HEIGHT = int(INFO.current_h * 0.5)

GROUND_HEIGHT = int(HEIGHT / 15)
SHELTER_HEIGHT = int(HEIGHT / 10)

s = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Missile Command')
clock = pygame.time.Clock()

level = 0

half = WIDTH/18
shelter_positions = [WIDTH/9 - half, 2*WIDTH/9 - half, 3*WIDTH/9 - half, 4*WIDTH/9 - half, 5*WIDTH/9 - half,
                     6*WIDTH/9 - half, 7*WIDTH/9 - half, 8*WIDTH/9 - half, 9*WIDTH/9 - half]

enemy_missiles = []
points = 0
player_missiles = []
explosion_list = []
shelter = [True, True, True, True, True, True]
launcher_list = [Launcher(0), Launcher(1), Launcher(2)]
launcher_positions = [30, WIDTH / 2, WIDTH - 30]
colors_list = [pygame.Color(0, 255, 0), pygame.Color(255, 0, 0), pygame.Color(255, 255, 0),
               pygame.Color(0, 255, 255), pygame.Color(255, 0, 255), pygame.Color(255, 255, 255),
               pygame.Color(0, 0, 255)]


def draw():
    s.fill((0, 0, 0))
    w = HEIGHT - SHELTER_HEIGHT
    pygame.draw.rect(s, pygame.Color(255, 255, 0), (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    for ss in range(len(launcher_list)):
        pygame.draw.polygon(s, pygame.Color(255, 255, 0),
                            [(ss * WIDTH / 2 - 20 + GROUND_HEIGHT - (GROUND_HEIGHT * ss), w), (ss * WIDTH / 2 + 20 + GROUND_HEIGHT - (GROUND_HEIGHT * ss), w),
                             (ss * WIDTH / 2 + 40 + GROUND_HEIGHT - (GROUND_HEIGHT * ss), HEIGHT), (ss * WIDTH / 2 - 40 + GROUND_HEIGHT - (GROUND_HEIGHT * ss), HEIGHT)])
        counter = launcher_list[ss].ammo
        number = 1
        while counter > 0:
            for j in range(number):
                pygame.draw.ellipse(s, (0, 0, 255), (launcher_positions[ss] + GROUND_HEIGHT/8 - ((number - 2 * j) * 6), HEIGHT - SHELTER_HEIGHT + ((number-1) * 8), 5, 5))
                counter = counter-1
                if counter == 0:
                    break
            number = number+1
    launcher_pos = 1
    for i in range(len(shelter)):
        if shelter[i]:
            pygame.draw.rect(s, pygame.Color(0, 0, 255), ((i+launcher_pos) * WIDTH/9 + SHELTER_HEIGHT/4, HEIGHT - GROUND_HEIGHT*1.2, SHELTER_HEIGHT/2, SHELTER_HEIGHT/3))
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
        if w.expires:
            w.frame -= 2
            if w.frame == 0:
                explosion_list.remove(w)
                del w
                continue
        elif w.frame == 1500:
            w.expires = True
        else:
            w.frame += 1
        pygame.draw.ellipse(s, random.choice(colors_list),
                            (w.poz_x-w.frame/60, w.poz_y-w.frame/60, w.frame/30, w.frame/30), 0)
        
    pygame.display.update()


def designate_launcher(x, y):
    minimum_x = 10
    y1 = HEIGHT - 50
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
        x1 = WIDTH / 2
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    if launcher_list[2].ammo > 0:
        x1 = WIDTH - 30
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    return minimum_x


def launch_rocket(x, y):
    if y > HEIGHT-SHELTER_HEIGHT*1.4:
        return
    
    launcher_position = designate_launcher(x, y)
    if launcher_position == 30:
        launcher_list[0].ammo -= 1
    elif launcher_position == WIDTH/2:
        launcher_list[1].ammo -= 1
    elif launcher_position == WIDTH-30:
        launcher_list[2].ammo -= 1
    else:
        return
    player_missiles.append(Missile(launcher_position, HEIGHT - 50, x, y, 0.2, 0))


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
            if middle_point(p.current_x, p.current_y, w.poz_x, w.poz_y, w.frame / 60) < 1:
                temp = Explosion(p.current_x, p.current_y)
                explosion_list.append(temp)
                player_missiles.remove(p)
                del p
                break
    for p in enemy_missiles:
        if p.current_y-p.end_y > -0.1:
            temp = Explosion(p.current_x, p.current_y)
            explosion_list.append(temp)
            if p.end_x == shelter_positions[0]:
                launcher_list[0].ammo = 0
            elif p.end_x == shelter_positions[1]:
                shelter[0] = False
            elif p.end_x == shelter_positions[2]:
                shelter[1] = False
            elif p.end_x == shelter_positions[3]:
                shelter[2] = False
            elif p.end_x == shelter_positions[4]:
                launcher_list[1].ammo = 0
            elif p.end_x == shelter_positions[5]:
                shelter[3] = False
            elif p.end_x == shelter_positions[6]:
                shelter[4] = False
            elif p.end_x == shelter_positions[7]:
                shelter[5] = False
            elif p.end_x == shelter_positions[8]:
                launcher_list[2].ammo = 0
            lose()
            enemy_missiles.remove(p)
            del p
            continue
        
        for w in explosion_list:
            if middle_point(p.current_x, p.current_y, w.poz_x, w.poz_y, w.frame / 60) < 1:
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
        explosion_list.clear()
        global points
        points += 1
        for i in range(10):
            temp = Missile(random.randrange(WIDTH), 0,
                           random.choice(shelter_positions), HEIGHT - 30, 0.04, random.randrange(4000))
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
    large_text = pygame.font.SysFont("consolas", int(HEIGHT * 0.035))
    text_surface = large_text.render("Survived waves : " + str(points) +
                                     " Press space to start again", True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = ((WIDTH / 2), (HEIGHT / 2))
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
        #clock.tick(100)


main()

