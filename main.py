#import
import pygame as pg
from random import *
from math import cos, sin, sqrt

#prg
class IA(pg.sprite.Sprite):
    def __init__(self, vector, vitesse, taille, champvision, pv, timer) -> None:             #je pense an stat il faut taille, vitesse, pv, champ de vision
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('ball.png')
        self.rect = self.image.get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector

        self.rect.center = [randint(0,1280),randint(0,720)]
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
        self.vector = pg.Vector2(0,0)
        self.image = pg.image.load('ball.png')
        self.rect = self.image.get_rect()
        self.target = None
        self.state = "LURKING"

    def dist_sprites(self, sprite):
        return sqrt((self.rect.x - sprite.rect.x)**2 + (self.rect.y - sprite.rect.y)**2)

    def direction_sprites(self, sprite):
        vec = pg.Vector2(sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)
        norme_vec = self.dist_sprites(sprite)
        return pg.Vector2(vec.x/norme_vec, vec.y/norme_vec)

    def lurk(self):
        pass

    def research(self, ia):
        for spri in ia.sprites():
            if self.dist_sprites(spri)<self.CHAMPVISION:
                self.target = spri
                self.state = "CHASING"
                break

    def chase(self):
        self.vector = self.direction_sprites(self.target)
        self.update()
        if self.dist_sprites(self.target)>self.CHAMPVISION:
            self.target = None
            self.state = "LURKING"

    def manage_states(self, ia):
        if self.state == "LURKING":
            self.lurk()
            self.research(ia)
        elif self.state == "CHASING":
            self.chase()

    def calcnewpos(self, rect, vector):
        (angle,z) = vector
        (dx,dy) = (z*cos(angle),z*sin(angle))
        return rect.move(dx,dy)

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
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
    new_player = IA(None, 15, 20, 25, 3, None)
    ia_group.add(new_player)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    group_monstre.sprites()[0].manage_states(ia_group)

    screen.blit(text, textRect)
    pg.display.flip()

    group_monstre.draw(screen)
    ia_group.draw(screen)

    clock.tick(60)

pg.quit()