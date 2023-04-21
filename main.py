#import
import pygame as pg
from random import *
from math import cos, sin, sqrt

#prg
class IA(pg.sprite.Sprite):
    def __init__(self, vitesse, taille, champvision, pv, timer, cible, chasseur) -> None:
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('ia.png')
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(self.image, (taille, taille))
        self.rect = self.image.get_rect()
        self.area = self.screen.get_rect()
        self.vector = pg.Vector2(0,0)
        self.cible = cible
        self.chasseur = chasseur
        self.target = None

        self.rect.center = [randint(0,1280),randint(0,720)]
        #var ia
        self.vitesse = vitesse
        self.taille = taille
        self.champvision = champvision
        self.pv = pv
        self.timer = timer

    def __str__(self) -> str:               #print des stat de l'objet
        return f"{self.vitesse} {self.taille} {self.champvision} {self.pv} {self.timer}"
    
    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def dist_sprites(self, sprite):
        return sqrt((self.rect.x - sprite.rect.x)**2 + (self.rect.y - sprite.rect.y)**2)

    def direction_sprites(self, sprite):
        vec = pg.Vector2(sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)
        norme_vec = self.dist_sprites(sprite)
        return pg.Vector2(vec.x/norme_vec, vec.y/norme_vec)

    def research(self, fruit_):
        for spri in fruit_.sprites():
            if self.dist_sprites(spri)<self.CHAMPVISION:
                self.target = spri
                return True
        self.target = None
        return False
    
    def servie(self, chasseur_):
        for spri in chasseur_.sprites():
            if self.dist_sprites(spri)<self.CHAMPVISION:
                self.target = spri
                return True
        self.target = None
        return False
    
    def move(self):
        self.vector = self.direction_sprites(self.target)
        self.update()
        if self.dist_sprites(self.target)>self.CHAMPVISION:
            pass

    def calcnewpos(self, rect, vector):
        (angle,z) = vector
        (dx,dy) = (z*cos(angle),z*sin(angle))
        return rect.move(dx,dy)

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos




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
        self.rect = self.rect.move(self.vector.x*self.VITESSE, self.vector.y*self.VITESSE)
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

# monstre
group_monstre = pg.sprite.Group()
for i in range(2):
    new_monstre = Monstre()
    group_monstre.add(new_monstre)

ia_group = pg.sprite.Group()

# ia
for joueur in range(1):
    new_player = IA(None, 15, 3, 25, 3, None, group_monstre)

for joueur in range(20):
    new_player = IA(pg.Vector2(0,0), 30, 30, 3, None, group_fruit, group_monstre)
    ia_group.add(new_player)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")

    for elt in group_monstre.sprites():
        elt.move()

    screen.blit(text, textRect)

    ia_group.draw(screen)
    group_monstre.draw(screen)

    pg.display.flip()

    clock.tick(60)

pg.quit()