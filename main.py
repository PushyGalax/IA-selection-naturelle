#import
import pygame as pg
from random import *
from math import sqrt
from timeit import default_timer
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd


class IA(pg.sprite.Sprite):
    def __init__(self, vitesse, taille, champvision, pv, image) -> None:
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(self.image, (taille, taille))
        self.rect = self.image.get_rect()

        self.target = None

        self.x = randint(0,1280-taille)
        self.y = randint(0,720-taille)

        self.rect.center = [self.x, self.y]
        #var ia
        self.VITESSE = vitesse
        self.vitesse = vitesse # bouge (game_speed)
        self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
        self.vector = self.vector.normalize()

        self.hit_cooldown = 3
        self.imortality_frames = default_timer()

        self.TAILLE = taille
        self.champvision = champvision

        self.pv = pv
        self.pvmax = pv
        self.pv_text = police.render(str(self.pv)+" PV", 1, (255,)*3)

        self.change_direction_timer = default_timer()
        self.timer = default_timer()
    
    def __str__(self):
        statact = [self.VITESSE, self.TAILLE, self.champvision, self.pv, self.pvmax, self.timer]
        return statact
    
    def degat(self):
        self.pv-=1
        self.pv_text = police.render(str(self.pv)+" PV", 1, (255,)*3)
        self.imortality_frames = default_timer()

    def bonus(self):
        self.pv+=1
        if self.pv < self.pvmax:
            self.pvmax = self.pv
        self.pv_text = police.render(str(self.pv)+" PV", 1, (255,)*3)

    def fin(self):
        time = default_timer()
        self.timer = time - self.timer
        return [self.VITESSE, self.TAILLE, self.champvision, self.pvmax, self.timer]

    def move(self, monstres, fruits, ia):
        self.recherche_plus_proche_monstre(monstres)
        self.recherche_plus_proche_fruit(fruits)
        self.repousse_autres_ia(ia)
        if default_timer() - self.change_direction_timer > randint(1,5):
            self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
            self.vector = self.vector.normalize()
            self.change_direction_timer = default_timer()
        distance = self.vector * self.vitesse
        self.x += distance.x
        self.y += distance.y
        self.rect.center = (self.x, self.y)
        if self.x+self.TAILLE//2>=1280:
            self.x = 1280-self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        elif self.x-self.TAILLE//2<=0:
            self.x = self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        if self.y+self.TAILLE//2>=720:
            self.y = 720-self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1
        elif self.y-self.TAILLE//2<=0:
            self.y = self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1

    def collision(self, element):
        return self.rect.colliderect(element.rect)

    def distance(self, point): # point = classe avec un rect
        return sqrt((self.x-point.rect.centerx)**2 + (self.y-point.rect.centery)**2)

    def repousse_autres_ia(self, ia):
        for elt in ia.sprites():
            if elt!=self and self.collision(elt):
                self.vector = pg.Vector2(self.x-elt.x, self.y-elt.y)
                if self.vector!= pg.Vector2(0,0):
                    self.vector = self.vector.normalize()

    def recherche_plus_proche_monstre(self, monstres):
        min_dist = float("+inf")
        monstre_proche = None
        for elt in monstres.sprites():
            dist_monstre = self.distance(elt)
            if dist_monstre<=self.champvision and dist_monstre<min_dist:
                min_dist = dist_monstre
                monstre_proche = elt
        if monstre_proche is not None:
            if default_timer()-self.imortality_frames>=self.hit_cooldown and self.collision(monstre_proche):
                self.degat()
            self.vector = pg.Vector2(self.x-monstre_proche.x, self.y-monstre_proche.y)
            if self.vector!= pg.Vector2(0,0):
                self.vector = self.vector.normalize()

    def recherche_plus_proche_fruit(self, fruits):
        min_dist = float("+inf")
        fruit_proche = None
        for elt in fruits.sprites():
            dist_fruit = self.distance(elt)
            if dist_fruit<=self.champvision and dist_fruit<min_dist:
                min_dist = dist_fruit
                fruit_proche = elt
        if fruit_proche is not None:
            if self.collision(fruit_proche):
                group_fruits.remove(fruit_proche)
                self.bonus()


class Monstre(pg.sprite.Sprite):
    def __init__(self) -> None:             #les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
        super().__init__()                  #val à changer
        self.VITESSE = 3
        self.vitesse = 3
        self.TAILLE = 50
        self.x = randint(0,1280-self.TAILLE)
        self.y = randint(0,720-self.TAILLE)
        self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
        self.vector = self.vector.normalize()
        self.image = pg.image.load('monstre.png')
        self.image = pg.transform.scale(self.image, (self.TAILLE, self.TAILLE))
        self.rect = self.image.get_rect()

    def move(self):
        distance = self.vector * self.vitesse
        self.x += distance.x
        self.y += distance.y
        self.rect.center = (self.x, self.y)
        if self.x+self.TAILLE//2>=1280:
            self.x = 1280-self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        elif self.x-self.TAILLE//2<=0:
            self.x = self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        if self.y+self.TAILLE//2>=720:
            self.y = 720-self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1
        elif self.y-self.TAILLE//2<=0:
            self.y = self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1


class fruit(pg.sprite.Sprite):
    def __init__(self) -> None:             #les fruits n'évolue pas, plus 1 pv quand IA sur fruit
        super().__init__()
        self.image = pg.image.load("fruit.png")
        self.image = pg.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.center = [randint(0,1230), randint(0,670)]


class Bouton:
    def __init__(self, image, pos):
        self.rect = pg.rect.Rect(0,0,64,64)
        self.rect.center = (pos[0]+32,pos[1]+32)
        self.image = pg.image.load(image)

    def clicked(self, image):
        mouse = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = pg.image.load(image)
            self.draw()
            return True
        return False

    def draw(self):
        self.image = pg.transform.scale(self.image, (64,64))
        screen.blit(self.image, (self.rect.x, self.rect.y))

#main

pg.init()
screen = pg.display.set_mode((1780, 720)) # 1280, 720
image_fond = pg.image.load("grass.png")

clock = pg.time.Clock()
running = True

# texte
police = pg.font.SysFont("monospace" ,15)
police_stat = pg.font.SysFont("monospace", 29)


# fruit
group_fruits = pg.sprite.Group()
for i in range(5):
    group_fruits.add(fruit())

# monstre
group_monstre = pg.sprite.Group()
for i in range(20):
    new_monstre = Monstre()
    group_monstre.add(new_monstre)

ia_group = pg.sprite.Group()

# ia
for joueur in range(12):
    chance=randint(1,2)
    if chance == 1:
        vitesse = round(2-random())
        taille = round(30-randint(0,4))
        champ =  round(50)
        pv = round(3-random())
    else:
        vitesse = round(2+random())
        taille = round(30+randint(0,4))
        champ = round(50)
        pv = round(3+random())
    ia_group.add(IA(vitesse,taille,champ,pv,"ia.png"))


# les stats
bordure = pg.image.load("bordure.png")
bordure = pg.transform.scale(bordure, (16,720))
texte_stats = pg.image.load("texte_stats.png")
texte_stats = pg.transform.scale(texte_stats, (256,64))
bouton_pause = Bouton("pause_unpressed.png", (1498,600))
bouton_ralentir = Bouton("ralentir_unpressed.png", (1418,600))
bouton_accelerer = Bouton("accelerer_unpressed.png", (1578,600))

def cote_stat():
    screen.fill("#A0A0A0", (1280,0,1780,720))
    screen.blit(texte_stats, (1410,50))
    screen.blit(police_stat.render(f"Génération : {generation}", 1, (0,)*3), (1420,300))
    screen.blit(police_stat.render(f"Nombre d'IA restantes : {len(ia_list)}", 1, (0,)*3), (1320,350))
    bouton_pause.draw()
    bouton_accelerer.draw()
    bouton_ralentir.draw()

def modifier_vitesse_jeu(increment):
    monstres = group_monstre.sprites()
    ia = ia_group.sprites()
    if min(ia, key=lambda x: x.vitesse).vitesse>0.5 and min(monstres, key=lambda x: x.vitesse).vitesse>0.5:
        for elt in monstres:
            elt.vitesse += increment
        for elt in ia:
            elt.vitesse += increment

def reset_vitesse_jeu():
    monstres = group_monstre.sprites()
    ia = ia_group.sprites()
    for elt in monstres:
        elt.vitesse = elt.VITESSE
    for elt in ia:
        elt.vitesse = elt.VITESSE

statia=[]
pause = False
var_vitesse = 0

#csv part

def moyenne(stat):
    moy=0
    incr=0
    for elem in ia_group.sprites():
        act=elem.__str__()
        incr+=1
        moy+=act[stat]
    moy=moy/incr
    return moy

generation = 1
vit=moyenne(0)
tai=moyenne(1)
hp=moyenne(4)

fieldnames = ['generation', "vitesse", "taille", "pv"]

with open('dataia.csv', 'w') as csvfile:
    csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwrite.writeheader()
    info = {"generation": generation,
        "vitesse": vit,
        "taille": tai,
        "pv": hp}
    csvwrite.writerow(info)

fieldnames2=["generation", "tempsmin", "tempsmax", "tempsmoy"]

with open('tempsia.csv', 'w') as csvfile:
    csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames2)
    csvwrite.writeheader()

temps=[]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if bouton_pause.clicked("pause_pressed.png" if not pause else "pause_unpressed.png"):
                pause = not pause
            if bouton_ralentir.clicked("ralentir_pressed.png") and not pause and len(ia_group.sprites())!=0:
                modifier_vitesse_jeu(-0.1)
                var_vitesse -= 0.1
            elif bouton_accelerer.clicked("accelerer_pressed.png") and not pause and len(ia_group.sprites())!=0:
                modifier_vitesse_jeu(0.1)
                var_vitesse +=  0.1
        else:
            bouton_ralentir.image = pg.image.load("ralentir_unpressed.png")
            bouton_ralentir.draw()
            bouton_accelerer.image = pg.image.load("accelerer_unpressed.png")
            bouton_accelerer.draw()

    if not pause:
        ia_list = ia_group.sprites()
        screen.blit(image_fond, (0,0))
        cote_stat()

        for elt in group_monstre.sprites():
            elt.move()

        for elt in ia_group.sprites():
            elt.move(group_monstre, group_fruits, ia_group)
            screen.blit(elt.pv_text, (elt.rect.x-8, elt.rect.centery-elt.TAILLE))

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
            moytemps=0
            for elem in statia:
                moytemps+=elem[4]
            moytemps/=len(statia)
            best=statia[0]
            statia.remove(best)
            for elem in statia:
                vitesse = ((best[0]+elem[0])//2)
                taille = (best[1]+elem[1])//2
                pv = (best[3]+elem[3])//2
                chance=randint(0,1)
                if chance == 0:
                    vitesse = round(vitesse-random())
                    taille = round(taille + random())
                    pv=round(pv-random())
                else:
                    vitesse = round(vitesse+random())
                    taille = round(taille - random())
                    pv=round(pv+random())
                if taille < 20:
                    taille=20
                ia_group.add(IA(vitesse,taille,40,pv,"ia.png"))
            ia_group.add(IA(best[0],best[1],best[2],best[3], "ia_shiny.png"))
            reset_vitesse_jeu()
            for i in range(int(var_vitesse*10)):
                modifier_vitesse_jeu(0.1 if var_vitesse>0 else -0.1)
            generation+=1

            with open('dataia.csv', 'a') as csvfile:
                csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames)
                info = {"generation": generation,
                        "vitesse": moyenne(0),
                        "taille": moyenne(1),
                        "pv": moyenne(4)}
                csvwrite.writerow(info)

            with open('tempsia.csv', 'a') as csvfile:
                csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames2)
                info = {"generation": generation,
                        "tempsmin": statia[-1][4],
                        "tempsmax": statia[0][4],
                        "tempsmoy": moytemps}
                csvwrite.writerow(info)

            statia = []

        group_fruits.draw(screen)
        ia_group.draw(screen)
        group_monstre.draw(screen)
        screen.blit(bordure, (1280,0))

    pg.display.flip()

    clock.tick(60)

pg.quit()
