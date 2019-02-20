# -*- coding: utf-8 -*-
import pygame ,sys ,random

from rakieta import rakieta
from wybuch import wybuch
from stanowisko import stanowisko
import math 

width = 480
height = 480
level=0
pozycje = [35 ,90, 140,190 ,240,290,340,390, 445]
pociski_wroga=[]
punkty=0
pociski=[]
wybuchy=[]
domy =[True , True, True, True , True , True]
#domy=[False,False,False,False,False,False]
stanowiska =[stanowisko(0), stanowisko(1), stanowisko(2)]
stanowiska_poz = [30 , width/2 , width-30]
kolory =[pygame.Color(0,255,0),pygame.Color(255,0,0), pygame.Color(255,255,0),
         pygame.Color(0,255,255), pygame.Color(255,0,255), pygame.Color(255,255,255),
         pygame.Color(0,0,255)]

pygame.init();
s=pygame.display.set_mode((height, width));
pygame.display.set_caption('Missile Command');
clock = pygame.time.Clock()


pygame.mouse.set_cursor(*pygame.cursors.diamond)

def rysuj_mape():
    s.fill((0,0,0))
    w =height -50
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
    trzy=1
    for i in range(len(domy)):
        if(domy[i]==True):pygame.draw.rect(s,pygame.Color(0,0,255),((i+trzy)*50 +30,height-40,20,20))
        if((i+1)%3==0):
            trzy=trzy+1
        
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
        
    for p in pociski_wroga:
        pygame.draw.line(s, pygame.Color(255,0,0) ,(p.startx ,p.starty ),(p.aktualnyx ,p.aktualnyy),1)
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
    pocisk = rakieta(ktore ,height-50 , x,y ,0.2 ,0)
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
    for p in pociski_wroga:
        if p.aktualnyy-p.koniecy>-0.1:
            temp = wybuch(p.aktualnyx, p.aktualnyy)
            wybuchy.append(temp)
            if p.koniecx==35:
                stanowiska[0].amunicja=0
            elif p.koniecx==90:
                domy[0]=False
            elif p.koniecx==140:
                domy[1]=False
            elif p.koniecx==190:
                domy[2]=False
            elif p.koniecx==240:
                stanowiska[1].amunicja=0
            elif p.koniecx==290:
                domy[3]=False
            elif p.koniecx==340:
                domy[4]=False
            elif p.koniecx==390:
                domy[5]=False
            elif p.koniecx==445:
                stanowiska[2].amunicja=0
            przegrana()
            pociski_wroga.remove(p)
            del p
            continue
        
        for w in wybuchy:
            if srodek(p.aktualnyx, p.aktualnyy ,w.pozx ,w.pozy ,w.klatka/60)<1:
                temp = wybuch(p.aktualnyx, p.aktualnyy)
                wybuchy.append(temp)
                pociski_wroga.remove(p)
                del p
                break
def level():
    if not pociski_wroga:
        stanowiska[0].amunicja=10
        stanowiska[1].amunicja=10
        stanowiska[2].amunicja=10
        for i in range(10):
            temp = rakieta(random.randrange(width) ,0
            , random.choice(pozycje) ,height-30 , 0.04, random.randrange(4000))
            pociski_wroga.append(temp)
def przegrana():
    for i in domy:
        if i==True:
            return
    del wybuchy[:]
    del pociski[:]
    del pociski_wroga[:]
    rysuj_mape()
    largeText = pygame.font.SysFont("consolas",12)
    textSurface = largeText.render("Uzyskane punkty : "+str(punkty)+
                                   " Wciśnij spacje aby zacząć od nowa", True, (255,0,0))
    TextRect= textSurface.get_rect()
    TextRect.center = ((width/2),(height/2))
    s.blit(textSurface, TextRect)
    
    pygame.display.update()
    global punkty
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                        stanowiska[0].amunicja=10
                        stanowiska[1].amunicja=10
                        stanowiska[2].amunicja=10
                        domy[0]=True
                        domy[1]=True
                        domy[2]=True
                        domy[3]=True
                        domy[4]=True
                        domy[5]=True
                        punkty=0
                        main()
                        
def main():
     while True:
        kolizje()
        rysuj_mape()
        level()
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    x ,y = pygame.mouse.get_pos()
                    strzal(x,y)
     clock.tick(60)

main()