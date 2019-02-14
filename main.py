# -*- coding: utf-8 -*-
import pygame ,sys ,random

from rakieta import rakieta
from wybuch import wybuch
from stanowisko import stanowisko
import math 

width = 480
height = 480

pociski=[]
wybuchy=[]
stanowiska =[stanowisko(0), stanowisko(1), stanowisko(2)]
stanowiska_poz = [30 , width/2 , width-30]
kolory =[pygame.Color(0,255,0),pygame.Color(255,0,0), pygame.Color(255,255,0),
         pygame.Color(0,255,255), pygame.Color(255,0,255), pygame.Color(255,255,255),
         pygame.Color(0,0,255)]

pygame.init();
s=pygame.display.set_mode((height, width));
pygame.display.set_caption('Missile Command');
clock = pygame.time.Clock()

rakieta_img =pygame.Surface((3,4))
pygame.mouse.set_cursor(*pygame.cursors.diamond)
def rysuj_rakieta():
    kol = pygame.Color(0,0,255)
    rakieta_img.fill((255,255,0))
    rakieta_img.set_at((1, 0), kol)
    rakieta_img.set_at((1, 1), kol)
    rakieta_img.set_at((1, 2), kol)
    rakieta_img.set_at((1, 3), kol)
    rakieta_img.set_at((0, 3), kol)
    rakieta_img.set_at((2, 3), kol)
    rakieta_img.set_at((0, 4), kol)
    rakieta_img.set_at((2, 4), kol)
def rysuj_mape():
    s.fill((0,0,0))
    w =height -50;
    pygame.draw.rect(s ,pygame.Color(255,255,0),( 0 ,height-30 ,width ,30))
    for ss in range(len(stanowiska)):
        pygame.draw.polygon(s, pygame.Color(255,255,0),
                        [(ss*width/2-20 +30 -(30*ss),w),(ss*width/2+20 +30-(30*ss),w),
                         (ss*width/2+40+30 -(30*ss),height),(ss*width/2-40+30-(30*ss),height)])
        counter = stanowiska[ss].amunicja
        poziom =1
        while counter>0:
            for j in range(poziom):
                #s.blit(rakieta_img ,(stanowiska_poz[ss] +(poziom-j *3),height-50+(poziom*8 )))
                pygame.draw.ellipse(s ,(0,0,255) ,(stanowiska_poz[ss]+8 -((poziom-2*j) *8),height-55+(poziom*10 ),5,5))
                counter= counter-1
                if counter==0:
                    break
            poziom= poziom+1


    for p in pociski:
        pygame.draw.line(s, pygame.Color(0,255,0) ,(p.startx ,p.starty ),(p.aktualnyx ,p.aktualnyy),1)
        pygame.draw.ellipse(s ,random.choice(kolory),
                        (p.aktualnyx-1.5 , p.aktualnyy-1.5 ,4 ,4), 0)
        col =random.choice(kolory)
        pygame.draw.line(s,col ,(p.koniecx-5 ,p.koniecy-5) ,
                         (p.koniecx+5 ,p.koniecy+5) ,1)
        pygame.draw.line(s,col ,(p.koniecx+5 ,p.koniecy-5) ,
                         (p.koniecx-5 ,p.koniecy+5) ,1)
        p.ruch()
        
    for w in wybuchy:
        if w.wygasa:
            w.klatka-=2
            if w.klatka==0:
                wybuchy.remove(w)
                del w
                continue
        elif w.klatka ==1500:
            w.wygasa=True
        else:
            w.klatka+=1
        pygame.draw.ellipse(s ,random.choice(kolory),
                        (w.pozx-w.klatka/60 ,w.pozy-w.klatka/60 ,w.klatka/30 ,w.klatka/30), 0)
        
    pygame.display.update()
def z_ktorego(x ,y):
    minimum_x =10
    y1= height-50
    dy =y-y1
    minimum =100000
    if stanowiska[0].amunicja >0:
        x1=30
        dx=x1-x
        temp =  math.sqrt(dx*dx + dy*dy)
        if temp <minimum:
            minimum=temp
            minimum_x=x1
    if stanowiska[1].amunicja >0:
        x1=width/2
        dx=x1-x
        temp =  math.sqrt(dx*dx + dy*dy)
        if temp <minimum:
            minimum=temp
            minimum_x=x1
    if stanowiska[2].amunicja >0:
        x1=width-30
        dx=x1-x
        temp =  math.sqrt(dx*dx + dy*dy)
        if temp <minimum:
            minimum=temp
            minimum_x=x1
    return minimum_x
    
def strzal(x,y):
    if y>height-81:
        return
    
    ktore = z_ktorego(x,y)
    if ktore==30:
        stanowiska[0].amunicja -=1
    elif ktore==width/2:
        stanowiska[1].amunicja -=1
    elif ktore==width-30:
        stanowiska[2].amunicja -=1
    else:
        return
    pocisk = rakieta(ktore ,height-50 , x,y)
    pociski.append(pocisk)

def srodek(x , y ,wx ,wy ,r):
    
    p = ((math.pow((x - wx), 2) // math.pow(r+1, 2)) + 
         (math.pow((y - wy), 2) // math.pow(r+1, 2))) 
  
    return p
    

def kolizje():
    for p in pociski:
        if p.aktualnyy-p.koniecy<0.1:
            temp = wybuch(p.aktualnyx, p.aktualnyy)
            wybuchy.append(temp)
            pociski.remove(p)
            del p
            continue
        
        for w in wybuchy:
            if srodek(p.aktualnyx, p.aktualnyy ,w.pozx ,w.pozy ,w.klatka/60)<1:
                temp = wybuch(p.aktualnyx, p.aktualnyy)
                wybuchy.append(temp)
                pociski.remove(p)
                del p
                break
            
    
def main():
     while True:
        kolizje()
        rysuj_mape()
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    x ,y = pygame.mouse.get_pos()
                    strzal(x,y)
     clock.tick(60)

rysuj_rakieta()
main()