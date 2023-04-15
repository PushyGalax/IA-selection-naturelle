#import
import pygame as pg
from random import *
from math import cos, sin

#prg
class IA(pg.sprite.Sprite):
    def __init__(self, vector, vitesse, taille, champvision, pv, timer) -> None:             #je pense an stat il faut taille, vitesse, pv, champ de vision
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('victime.png')
        self.screen = pg.display.get_surface()
        self.size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (self.size[0]/taille, self.size[1]/taille))
        self.rect = self.image.get_rect()
        self.area = self.screen.get_rect()
        self.vector = vector
        self.rect.center = [randint(0,1280),randint(0,720)]
        
        #var ia
        self.vitesse = vitesse
        self.taille = taille
        self.champvision = champvision
        self.pv = pv
        self.timer = timer

    def __str__(self) -> str:               #print des stat de l'objet
        return f"{self.vitesse} {self.taille} {self.champvision} {self.pv} {self.timer}"
    
    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*cos(angle),z*sin(angle))
        return rect.move(dx,dy)

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def move(self):
        pass

class Monstre(pg.sprite.Sprite):
    def __init__(self) -> None:             #les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
        super().__init__()                  #val à changer
        self.VITESSE = 20
        self.CHAMPVISION = 35
        self.image = pg.image.load('ball.png')
        self.rect = self.image.get_rect()

    def calcnewpos(self, rect, vector):
        (angle,z) = vector
        (dx,dy) = (z*cos(angle),z*sin(angle))
        return rect.move(dx,dy)

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos


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

group_monstre = pg.sprite.Group()
for i in range(1):
    new_monstre = Monstre()
    group_monstre.add(new_monstre)

ia_group = pg.sprite.Group()
for joueur in range(20):
    new_player = IA(None, 15, 3, 25, 3, None)
    ia_group.add(new_player)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.blit(text, textRect)
    pg.display.flip()
    group_monstre.draw(screen)
    ia_group.draw(screen)
    clock.tick(60)

pg.quit()