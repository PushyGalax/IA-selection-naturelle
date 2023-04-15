#import
import pygame as pg
from random import *
from math import cos, sin

#prg
class IA(pg.sprite.Sprite):
    def __init__(self, vector, vitesse, taille, champvision, pv, timer) -> None:             #je pense an stat il faut taille, vitesse, pv, champ de vision
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = pg.load_png('ball.png')
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        
        #var ia
        self.vitesse = vitesse
        self.taille = taille
        self.champvision = champvision
        self.pv = pv
        self.timer = timer

    def __str__(self) -> str:               #print des stat de l'objet
        return f"{self.vitesse} {self.taille} {self.champvision}"
    
    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def move(self):
        pass

class monstre(pg.sprite.Sprite):
    def __init__(self) -> None:             #les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
        self.VITESSE = 20                   #val à changer
        self.CHAMPVISION = 35

    def __str__(self) -> str:
        pass

class fruit(pg.sprite.Sprite):
    def __init__(self) -> None:             #les fruits n'évolue pas, plus 1 pv quand IA sur fruit
        pass

    def __str__(self) -> str:
        pass


#main

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

screen.fill("black")
font = pg.font.Font('freesansbold.ttf', 16)
text = font.render('Show stat', True, (255,255,255), (0,0,0))

textRect = text.get_rect()
textRect.center = (1200, 25)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.blit(text, textRect)
    pg.display.flip()
    clock.tick(60)

pg.quit()