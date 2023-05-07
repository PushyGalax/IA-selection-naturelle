# import
import csv
from math import sqrt
from random import *
from timeit import default_timer
import pygame as pg


class IA(pg.sprite.Sprite):
    def __init__(self, vitesse, taille, champvision, pv, image, typeia, stamina) -> None:
        # var pygame
        pg.sprite.Sprite.__init__(self)

        if image == None:
            if typeia == 1:
                image = "assets/ia/type1.png"
            elif typeia == 2:
                image = "assets/ia/type2.png"
            else:
                image = "assets/ia/type3.png"

        self.image = pg.image.load(image)
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(self.image, (taille, taille))
        self.rect = self.image.get_rect()

        self.x = randint(0, 1280-taille)
        self.y = randint(0, 720-taille)

        self.rect.center = [self.x, self.y]
        # var ia
        self.VITESSE = vitesse # la max
        self.vitesse = vitesse
        self.vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
        self.vector = self.vector.normalize()

        self.hit_cooldown = 3
        self.imortality_frames = default_timer()

        self.TAILLE = taille
        self.champvision = champvision
        self.typeia = typeia

        self.STAMINA = stamina # le max
        self.stamina = stamina

        self.pv = pv
        self.pvmax = pv
        self.pv_text = police.render(str(self.pv)+" PV", 1, (255,)*3)

        self.change_direction_timer = default_timer()
        self.timer = default_timer()

    def __str__(self):
        statact = [self.VITESSE, self.TAILLE,
                   self.champvision, self.pv, self.pvmax, self.timer, self.STAMINA]
        return statact

    def draw_hp(self):
        screen.blit(self.pv_text, (self.rect.x-8, self.rect.centery-self.TAILLE))

    def draw_stamina(self):
        stamina_rect = pg.Rect(self.x-self.TAILLE/2,self.y+self.TAILLE/2+2,self.stamina/self.STAMINA*self.TAILLE+2,2)
        rect_fond = pg.Rect(self.x-self.TAILLE/2,self.y+self.TAILLE/2+2,self.TAILLE+2,2)
        pg.draw.rect(screen, (0,0,200), rect_fond)
        pg.draw.rect(screen, (0,255,255), stamina_rect)

    def degat(self, monstres):
        for elt in monstres.sprites():
            if default_timer()-self.imortality_frames >= self.hit_cooldown and self.collision(elt):
                self.pv -= 1
                self.pv_text = police.render(str(self.pv)+" PV", 1, (255,)*3)
                self.imortality_frames = default_timer()

    def fin(self):
        time = default_timer()
        self.timer = time - self.timer
        return [self.VITESSE, self.TAILLE, self.champvision, self.pvmax, self.timer, self.typeia, self.STAMINA]

    def get_speed(self):
        return sqrt(self.vector.x**2 + self.vector.y**2)

    def update_speed(self):
        if default_timer() - self.change_direction_timer > uniform(0.2, 1.0) and self.stamina > 0:
            new_vector = pg.Vector2(choice((-random(), random())), choice((-random(), random())))
            new_vector = new_vector.normalize() / 2
            self.vector += new_vector
            current_speed = self.get_speed()
            if current_speed > self.VITESSE:
                self.vector = self.vector.normalize() * self.VITESSE
            self.change_direction_timer = default_timer()
            self.stamina -= current_speed

    def move(self, monstres, fruits, ia):
        if self.stamina <= 0:
            self.pv = 0
            return
        self.degat(monstres)
        self.miam(fruits)
        if self.typeia == 1:
            self.recherche_plus_proche_monstre(monstres)
        elif self.typeia == 2:
            self.recherche_plus_proche_monstre(monstres)
            self.recherche_plus_proche_fruit(fruits)
        self.update_speed()
        self.repousse_autres_ia(ia)
        distance = self.vector
        self.x += distance.x
        self.y += distance.y
        self.rect.center = (self.x, self.y)
        if self.x+self.TAILLE//2 >= 1280:
            self.x = 1280-self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        elif self.x-self.TAILLE//2 <= 0:
            self.x = self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        if self.y+self.TAILLE//2 >= 720:
            self.y = 720-self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1
        elif self.y-self.TAILLE//2 <= 0:
            self.y = self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1

    def collision(self, element):
        return self.rect.colliderect(element.rect)

    def distance(self, point):  # point = classe avec un rect
        return sqrt((self.x-point.rect.centerx)**2 + (self.y-point.rect.centery)**2)

    def repousse_autres_ia(self, ia):
        for elt in ia.sprites():
            if elt != self and self.collision(elt):
                self.vector = pg.Vector2(self.x-elt.x, self.y-elt.y)
                if self.vector != pg.Vector2(0, 0):
                    self.vector = self.vector.normalize()

    def recherche_plus_proche_monstre(self, monstres):
        min_dist = float("+inf")
        self.monstre_proche = None
        for elt in monstres.sprites():
            dist_monstre = self.distance(elt)
            if dist_monstre <= self.champvision and dist_monstre < min_dist:
                min_dist = dist_monstre
                self.monstre_proche = elt
        if self.monstre_proche is not None:
            self.vector += pg.Vector2(self.x-self.monstre_proche.x, self.y-self.monstre_proche.y)*2
            if self.vector != pg.Vector2(0, 0):
                self.vector = self.vector.normalize()

    def recherche_plus_proche_fruit(self, fruits):
        min_dist = float("+inf")
        fruit_proche = None
        for elt in fruits.sprites():
            dist_fruit = self.distance(elt)
            # changer la distance de detection des fruits, 3* plus grande que pour detecte monstres
            if dist_fruit <= self.champvision*5 and dist_fruit < min_dist:
                min_dist = dist_fruit
                fruit_proche = elt
        if fruit_proche is not None and self.monstre_proche is None:
            self.vector += pg.Vector2(fruit_proche.rect.centerx-self.x, fruit_proche.rect.centery-self.y)*2
            if self.vector != pg.Vector2(0, 0):
                self.vector = self.vector.normalize()

    def miam(self, fruits):
        for elt in fruits.sprites():
            if self.collision(elt):
                group_fruits.remove(elt)
                self.pv += 1
                self.stamina += self.STAMINA * 0.2
                if self.pv < self.pvmax:
                    self.pvmax = self.pv
                if self.stamina>self.STAMINA:
                    self.stamina = self.STAMINA
                self.pv_text = police.render(str(self.pv)+" PV", 1, (255,)*3)


class Monstre(pg.sprite.Sprite):
    # les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
    def __init__(self) -> None:
        super().__init__()  # val à changer
        self.VITESSE = 3
        self.vitesse = 3
        self.TAILLE = 50
        self.x = randint(0, 1280-self.TAILLE)
        self.y = randint(0, 720-self.TAILLE)
        self.vector = pg.Vector2(
            choice((-random(), random())), choice((-random(), random())))
        self.vector = self.vector.normalize()
        self.image = pg.image.load('assets/monstre.png')
        self.image = pg.transform.scale(self.image, (self.TAILLE, self.TAILLE))
        self.rect = self.image.get_rect()

    def move(self):
        distance = self.vector * self.vitesse
        self.x += distance.x
        self.y += distance.y
        self.rect.center = (self.x, self.y)
        if self.x+self.TAILLE//2 >= 1280:
            self.x = 1280-self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        elif self.x-self.TAILLE//2 <= 0:
            self.x = self.TAILLE//2
            self.rect.centerx = self.x
            self.vector.x *= -1
        if self.y+self.TAILLE//2 >= 720:
            self.y = 720-self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1
        elif self.y-self.TAILLE//2 <= 0:
            self.y = self.TAILLE//2
            self.rect.centery = self.y
            self.vector.y *= -1


class fruit(pg.sprite.Sprite):
    def __init__(self) -> None:  # les fruits n'évolue pas, plus 1 pv quand IA sur fruit
        super().__init__()
        self.image = pg.image.load("assets/fruit.png")
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = [randint(0, 1230), randint(0, 670)]


# main

pg.init()
screen = pg.display.set_mode((1780, 720))  # 1280, 720
image_fond = pg.image.load("assets/grass.png")

clock = pg.time.Clock()
running = True

# texte
police = pg.font.SysFont("monospace", 15)
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

group_ia = pg.sprite.Group()

# ia
for joueur in range(12):
    chance = randint(1, 2)
    if chance == 1:
        vitesse = round(3-random())
        taille = 30-randint(0, 4)
        champ = 80
        pv = round(3-random())
        stamina = 50 - randint(0,10)
    else:
        vitesse = round(3+random())
        taille = 30+randint(0, 4)
        champ = 80
        pv = round(3+random())
        stamina = 50 + randint(0,10)
    group_ia.add(IA(vitesse, taille, champ, pv,
                 None, randint(1, 3), stamina))


# les stats
bordure = pg.image.load("assets/bordure.png")
bordure = pg.transform.scale(bordure, (16, 720))
texte_stats = pg.image.load("assets/texte_stats.png")
texte_stats = pg.transform.scale(texte_stats, (256, 64))
aff_type_1 = pg.image.load("assets/ia/type1.png")
aff_type_2 = pg.image.load("assets/ia/type2.png")
aff_type_3 = pg.image.load("assets/ia/type3.png")
aff_type_1 = pg.transform.scale(aff_type_1, (40, 40))
aff_type_2 = pg.transform.scale(aff_type_2, (40, 40))
aff_type_3 = pg.transform.scale(aff_type_3, (40, 40))
aff_type_1_shiny = pg.image.load("assets/ia/type1_shiny.png")
aff_type_2_shiny = pg.image.load("assets/ia/type2_shiny.png")
aff_type_3_shiny = pg.image.load("assets/ia/type3_shiny.png")
aff_type_1_shiny = pg.transform.scale(aff_type_1_shiny, (40, 40))
aff_type_2_shiny = pg.transform.scale(aff_type_2_shiny, (40, 40))
aff_type_3_shiny = pg.transform.scale(aff_type_3_shiny, (40, 40))

def cote_stat():
    screen.fill("#A0A0A0", (1280, 0, 1780, 720))
    screen.blit(texte_stats, (1410, 50))
    screen.blit(police_stat.render(
        f"Génération : {generation}", 1, (0,)*3), (1420, 300))
    screen.blit(police_stat.render(
        f"Nombre d'IA restantes : {len(ia_list)}", 1, (0,)*3), (1320, 350))
    screen.blit(aff_type_1, (1400, 400))
    screen.blit(aff_type_2, (1400, 450))
    screen.blit(aff_type_3, (1400, 500))
    screen.blit(aff_type_1_shiny, (1350, 400))
    screen.blit(aff_type_2_shiny, (1350, 450))
    screen.blit(aff_type_3_shiny, (1350, 500))
    screen.blit(police_stat.render("IA peureuse", 1, (0,)*3), (1450, 400))
    screen.blit(police_stat.render("IA courrageuse", 1, (0,)*3), (1450, 450))
    screen.blit(police_stat.render("IA idiote", 1, (0,)*3), (1450, 500))


statia = []
var_vitesse = 0
temps = []

# csv part

def moyenne(stat):
    moy = 0
    incr = 0
    for elem in group_ia.sprites():
        act = elem.__str__()
        incr += 1
        moy += act[stat]
    moy = moy/incr
    return moy

def csv_ecrit():
    with open('dataia.csv', 'a') as csvfile:
        csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames)
        info = {"generation": generation,
                "vitesse": moyenne(0),
                "taille": moyenne(1),
                "pv": moyenne(4),
                "stamina": moyenne(6)}
        csvwrite.writerow(info)

    with open('tempsia.csv', 'a') as csvfile:
        csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames2)
        info = {"generation": generation,
                "tempsmin": statia[-1][4],
                "tempsmax": statia[0][4],
                "tempsmoy": moytemps}
        csvwrite.writerow(info)

    with open('type.csv', 'a') as csvfile:
        csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames3)
        info = {"generation": generation,
                "type1": cpttype1,
                "type2": cpttype2,
                "type3": cpttype3}
        csvwrite.writerow(info)

generation = 1
vie = moyenne(0)
tai = moyenne(1)
hp = moyenne(4)


fieldnames = ['generation', "vitesse", "taille", "pv", "stamina"]
fieldnames2 = ["generation", "tempsmin", "tempsmax", "tempsmoy"]
fieldnames3 = ["generation", "type1", "type2", "type3"]

with open('dataia.csv', 'w') as csvfile:
    csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwrite.writeheader()
    info = {"generation": generation,
            "vitesse": vie,
            "taille": tai,
            "pv": hp}
    csvwrite.writerow(info)

with open('tempsia.csv', 'w') as csvfile:
    csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames2)
    csvwrite.writeheader()


with open('type.csv', 'w') as csvfile:
    csvwrite = csv.DictWriter(csvfile, fieldnames=fieldnames3)
    csvwrite.writeheader()




## BOUCLE DU JEU ##
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    ia_list = group_ia.sprites()
    # screen.blit(image_fond, (0,0))
    screen.fill("#317d50")
    cote_stat()

    for elt in group_monstre.sprites():
        elt.move()

    for elt in group_ia.sprites():
        elt.move(group_monstre, group_fruits, group_ia)
        elt.draw_hp()
        elt.draw_stamina()

    if len(ia_list) != 0:
        for elem in ia_list:
            if elem.pv <= 0:
                mort = elem.fin()
                statia.append(mort)
                group_ia.remove(elem)
    else:
        cpttype1 = 0
        cpttype2 = 0
        cpttype3 = 0
        statia.sort(key=lambda M: M[4], reverse=True)
        moytemps = 0
        for elem in statia:
            moytemps += elem[4]
            if elem[5] == 1:
                cpttype1 += 1
            elif elem[5] == 2:
                cpttype2 += 1
            elif elem[5] == 3:
                cpttype3 += 1
        moytemps /= len(statia)
        best = statia[0]
        statia.remove(best)
        # [self.VITESSE, self.TAILLE, self.champvision, self.pvmax, self.timer]
        for elem in statia:
            vitesse = ((best[0]+elem[0])/2)
            taille = (best[1]+elem[1])/2
            pv = (best[3]+elem[3])/2
            stamina = (best[6]+elem[6])/2
            chance = randint(0, 1)
            if chance == 0:
                vitesse = max(1, round(vitesse+random()))
            else:
                vitesse = max(1, round(vitesse-random()))
            chance = randint(0, 1)
            if chance == 0:
                taille = max(20, round(taille + random()))
            else:
                taille = max(20, round(taille - random()))
            chance = randint(0, 1)
            if chance == 0:
                pv = max(1, round(pv + random()))
            else:
                pv = max(1, round(pv - random()))
            chance = randint(0,1)
            if chance == 0:
                stamina = max(20, round(stamina + randint(0,7)))
            else:
                stamina = max(20, round(stamina - randint(0,7)))
            if elem[5] == best[5]:
                typeia = best[5]
            else:
                chance = randint(1, 10)
                if chance == 1:
                    typeia = best[5]
                else:
                    typeia = elem[5]
            group_ia.add(IA(vitesse, taille, 60, pv, None, typeia, stamina))
        if best[5]==1:
            group_ia.add(IA(best[0], best[1], best[2], best[3], "assets/ia/type1_shiny.png", best[5], best[6]))
        elif best[5]==2:
            group_ia.add(IA(best[0], best[1], best[2], best[3], "assets/ia/type2_shiny.png", best[5], best[6]))
        elif best[5]==3:
            group_ia.add(IA(best[0], best[1], best[2], best[3], "assets/ia/type3_shiny.png", best[5], best[6]))

        for elem in group_fruits.sprites():
            group_fruits.remove(elem)
        for i in range(5):
            group_fruits.add(fruit())
        generation += 1

        csv_ecrit()

        statia = []

    group_fruits.draw(screen)
    group_ia.draw(screen)
    group_monstre.draw(screen)
    screen.blit(bordure, (1280, 0))

    pg.display.flip()

    clock.tick(60)

pg.quit()
