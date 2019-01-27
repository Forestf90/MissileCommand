# -*- coding: utf-8 -*-
import pygame ,sys ,random

from rakieta import rakieta
from wybuch import wybuch

width = 480
height = 480

pociski=[]
wybuchy=[]

kolory =[pygame.Color(0,255,0),pygame.Color(255,0,0), pygame.Color(255,255,0),
         pygame.Color(0,255,255), pygame.Color(255,0,255), pygame.Color(255,255,255),
         pygame.Color(0,0,255)]

pygame.init();
s=pygame.display.set_mode((height, width));
pygame.display.set_caption('Missile Command');
clock = pygame.time.Clock()

def rysuj_mape():
    s.fill((0,0,0))
    w =height -50;
    pygame.draw.rect(s ,pygame.Color(255,255,0),( 0 ,height-30 ,width ,30))
    pygame.draw.polygon(s, pygame.Color(255,255,0),
                        [(width/2-20 ,w),(width/2+20 ,w),(width/2+40,height),(width/2-40,height)])

    for p in pociski:
        if p.aktualnyy-p.koniecy<0.1:
            temp = wybuch(p.aktualnyx, p.aktualnyy)
            wybuchy.append(temp)
            pociski.remove(p)
            del p
            continue
        pygame.draw.line(s, pygame.Color(0,255,0) ,(p.startx ,p.starty ),(p.aktualnyx ,p.aktualnyy),1)
        pygame.draw.ellipse(s ,random.choice(kolory),
                        (p.aktualnyx-1.5 , p.aktualnyy-1.5 ,4 ,4), 0)
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
    
def strzal(x,y):
    if x>height-31:
        return
    pocisk = rakieta(width/2 ,height-50 , x,y)
    pociski.append(pocisk)
    
    
def main():
     while True:
        rysuj_mape()
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    x ,y = pygame.mouse.get_pos()
                    strzal(x,y)
     clock.tick(60)


main()