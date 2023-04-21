#import
import pygame as pg
from random import *
from math import cos, sin, sqrt
from timeit import default_timer


class IA(pg.sprite.Sprite):
    def __init__(self, vitesse, taille, champvision, pv) -> None:
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('ia.png')
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(self.image, (taille, taille))
        self.rect = self.image.get_rect()
        self.area = self.screen.get_rect()

        self.target = None

        self.rect.center = [randint(0,1280),randint(0,720)]
        #var ia
        self.vitessenum = vitesse
        self.vector = pg.Vector2(random(),random())
        self.vector = self.vector.normalize()

        self.taille = taille
        self.champvision = champvision
        self.pv = pv
        self.pvmax = pv
        self.change_direction_timer = default_timer()
        self.timer = default_timer()
    
    def __str__(self):               #print des stat de l'objet
        statact = [self.vector, self.taille, self.champvision, self.pv, self.pvmax, self.timer]
        return statact
    
    def degat(self):
        self.pv-=1
    
    def fin(self):
        time = default_timer()
        self.timer = time - self.timer
        return [self.vector, self.taille, self.champvision, self.pv, self.timer]

    def move(self, monstres):
        self.recherche_plus_proches(monstres)
        if default_timer() - self.change_direction_timer > 1:
            self.vector = pg.Vector2(random(),random())
            self.vector = self.vector.normalize()
            self.change_direction_timer = default_timer()
        self.rect = self.rect.move(self.vector * self.vitessenum)
        centrex = self.rect.centerx
        if centrex+self.taille//2>=1280:
            self.rect.centerx = 1280-self.taille//2
            self.vector.x *= -1
        elif centrex-self.taille//2<=0:
            self.rect.centerx = self.taille//2
            self.vector.x *= -1
        centrey = self.rect.centery
        if centrey+self.taille//2>=720:
            self.rect.centery = 720-self.taille//2
            self.vector.y *= -1
        elif centrey-self.taille//2<=0:
            self.rect.centery = self.taille//2
            self.vector.y *= -1

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
            self.vector = pg.Vector2(self.rect.centerx-monstre_proche.rect.centerx, self.rect.centery-monstre_proche.rect.centery)
            self.vector = self.vector.normalize()


class Monstre(pg.sprite.Sprite):
    def __init__(self) -> None:             #les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
        super().__init__()                  #val à changer
        self.VITESSE = 3
        self.vector = pg.Vector2(random(), random())
        self.vector = self.vector.normalize()
        self.image = pg.image.load('monstre.png')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [randint(0,1280),randint(0,720)]
        print(self.vector)

    def move(self):
        self.rect = self.rect.move(self.vector * self.VITESSE)
        centrex = self.rect.centerx
        if centrex+25>=1280 or centrex-25<=0:
            self.vector.x *= -1
        centrey = self.rect.centery
        if centrey+25>=720 or centrey<=0:
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

font = pg.font.Font('freesansbold.ttf', 16)
text = font.render('Show stat', True, (255,255,255), (0,0,0))

textRect = text.get_rect()
textRect.center = (1200, 25)

# fruit
group_fruit = pg.sprite.Group()
group_fruit.add(fruit())

d = 0
# monstre
group_monstre = pg.sprite.Group()
for i in range(2):
    new_monstre = Monstre()
    group_monstre.add(new_monstre)

ia_group = pg.sprite.Group()

# ia
for joueur in range(1):
    new_player = IA(5, 3, 25, 3)

for joueur in range(2):
    new_player = IA(2, 30, 200, 3)
    ia_group.add(new_player)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")

    for elt in group_monstre.sprites():
        elt.move()

    for elt in ia_group.sprites():
        elt.move(group_monstre)

    screen.blit(text, textRect)

    ia_group.draw(screen)
    group_monstre.draw(screen)

    pg.display.flip()

    clock.tick(180)

pg.quit()