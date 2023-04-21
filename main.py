#import
import pygame as pg
from random import *
from math import cos, sin, sqrt
from timeit import default_timer
import tkinter as tk


class IA(pg.sprite.Sprite):
    def __init__(self, vitesse, taille, champvision, pv) -> None:
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('ia.png')
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(self.image, (taille, taille))
        self.rect = self.image.get_rect()

        self.target = None

        self.rect.center = [randint(0,1280),randint(0,720)]
        #var ia
        self.vitessenum = vitesse
        self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
        self.vector = self.vector.normalize()

        self.TAILLE = taille
        self.champvision = champvision
        self.pv = pv
        self.pvmax = pv
        self.change_direction_timer = default_timer()
        self.timer = default_timer()
    
    def __str__(self):
        statact = [self.vitessenum, self.TAILLE, self.champvision, self.pv, self.pvmax, self.timer]
        return statact
    
    def degat(self):
        self.pv-=1
    
    def fin(self):
        time = default_timer()
        self.timer = time - self.timer
        return [self.vitessenum, self.TAILLE, self.champvision, self.pvmax, self.timer]

    def move(self, monstres):
        self.recherche_plus_proches(monstres)
        if default_timer() - self.change_direction_timer > 1:
            self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
            self.vector = self.vector.normalize()
            self.change_direction_timer = default_timer()
        self.rect = self.rect.move(self.vector * self.vitessenum)
        centrex = self.rect.centerx
        if centrex+self.TAILLE//2>=1280:
            self.rect.centerx = 1280-self.TAILLE//2
            self.vector.x *= -1
        elif centrex-self.TAILLE//2<=0:
            self.rect.centerx = self.TAILLE//2
            self.vector.x *= -1
        centrey = self.rect.centery
        if centrey+self.TAILLE//2>=720:
            self.rect.centery = 720-self.TAILLE//2
            self.vector.y *= -1
        elif centrey-self.TAILLE//2<=0:
            self.rect.centery = self.TAILLE//2
            self.vector.y *= -1

    def collision(self, monstre):
        if self.rect.colliderect(monstre.rect):
            self.degat()

    def distance(self, point): # point = classe avec un rect
        return sqrt((self.rect.centerx-point.rect.x)**2 + (self.rect.centery-point.rect.y)**2)

    def recherche_plus_proches(self, monstres):
        min_dist = float("+inf")
        monstre_proche = None
        for elt in monstres.sprites():
            dist_monstre = self.distance(elt)
            if dist_monstre<=self.champvision and dist_monstre<min_dist:
                min_dist = dist_monstre
                monstre_proche = elt
        if monstre_proche is not None:
            self.collision(monstre_proche)
            self.vector = pg.Vector2(self.rect.centerx-monstre_proche.rect.centerx, self.rect.centery-monstre_proche.rect.centery)
            self.vector = self.vector.normalize()


class Monstre(pg.sprite.Sprite):
    def __init__(self) -> None:             #les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
        super().__init__()                  #val à changer
        self.VITESSE = 3
        self.TAILLE = 50
        self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
        self.vector = self.vector.normalize()
        self.image = pg.image.load('monstre.png')
        self.image = pg.transform.scale(self.image, (self.TAILLE, self.TAILLE))
        self.rect = self.image.get_rect()
        self.rect.center = [randint(0,1280),randint(0,720)]
        # print(self.vector)

    def move(self):
        self.rect = self.rect.move(self.vector * self.VITESSE)
        centrex = self.rect.centerx
        if centrex+self.TAILLE//2>=1280:
            self.rect.centerx = 1280-self.TAILLE//2
            self.vector.x *= -1
        elif centrex-self.TAILLE//2<=0:
            self.rect.centerx = self.TAILLE//2
            self.vector.x *= -1
        centrey = self.rect.centery
        if centrey+self.TAILLE//2>=720:
            self.rect.centery = 720-self.TAILLE//2
            self.vector.y *= -1
        elif centrey-self.TAILLE//2<=0:
            self.rect.centery = self.TAILLE//2
            self.vector.y *= -1


class fruit(pg.sprite.Sprite):
    def __init__(self) -> None:             #les fruits n'évolue pas, plus 1 pv quand IA sur fruit
        super().__init__()

    def __str__(self) -> str:
        pass


#main

pg.init()
screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()
running = True

# texte
police = pg.font.SysFont("monospace" ,15)
l_pv = []

# fruit
group_fruit = pg.sprite.Group()
group_fruit.add(fruit())

# monstre
group_monstre = pg.sprite.Group()
for i in range(10):
    new_monstre = Monstre()
    group_monstre.add(new_monstre)

ia_group = pg.sprite.Group()

# ia
for joueur in range(5):
    new_player = IA(2, 30, 200, 3)
    ia_group.add(new_player)
    l_pv.append(pg.font.render("3", 1, (255,)*3))

statia=[]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")

    for elt in group_monstre.sprites():
        elt.move()

    for i,elt in enumerate(ia_group.sprites()):
        elt.move(group_monstre)
        screen.blit(l_pv[i], (elt.rect.x, elt.rect.centery-elt.taille))

    ia_list = ia_group.sprites()
    if len(ia_list) != 0:
        for elem in ia_list:
            stat = elem.__str__()
            pv = stat[3]
            if pv == 0:
                mort=elem.fin()
                statia.append(mort)
                ia_group.remove(elem)
    else:
        statia.sort(key=lambda M : M[4], reverse=True)
        best=statia[0]
        statia.remove(best)
        for elem in statia:
            vitesse = (best[0]+elem[0])//2
            taille = (best[1]+elem[1])//2
            champ = (best[2]+elem[2])//2
            pv = (best[3]+elem[3])//2
            ia_group.add(IA(vitesse,taille,champ,pv))
        ia_group.add(IA(best[0],best[1],best[2],best[3]))
        statia = []

    ia_group.draw(screen)
    group_monstre.draw(screen)

    pg.display.flip()

    clock.tick(60)

pg.quit()