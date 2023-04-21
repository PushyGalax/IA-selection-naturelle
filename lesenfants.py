import pygame as pg
from random import randint, random
from timeit import default_timer

class IA(pg.sprite.Sprite):
    def __init__(self, vitesse, taille, champvision, pv) -> None:
        #var pygame
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('ia.png')
        self.image.set_colorkey((247, 247, 247))
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(self.image, (taille, taille))
        self.rect = self.image.get_rect()
        self.area = self.screen.get_rect()
        self.vector = pg.Vector2(0,0)

        self.target = None

        self.rect.center = [randint(0,1280),randint(0,720)]
        #var ia
        self.vitessenum = vitesse
        self.vitesse = pg.Vector2(0,0)

        self.taille = taille
        self.champvision = champvision
        self.pv = pv
        self.pvmax = pv
        self.timer = default_timer()
    
    def __str__(self):               #print des stat de l'objet
        statact = [self.vitesse, self.taille, self.champvision, self.pv, self.pvmax, self.timer]
        return statact
    
    def degat(self):
        self.pv-=1
    
    def fin(self):
        time = default_timer()
        self.timer = time - self.timer
        return [self.vitesse, self.taille, self.champvision, self.pvmax, self.timer]


pg.init()
screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()
running = True


font = pg.font.Font('freesansbold.ttf', 16)
text = font.render('Show stat', True, (255,255,255), (0,0,0))

textRect = text.get_rect()
textRect.center = (1200, 25)

statia=[]

ia_group = pg.sprite.Group()
for joueur in range(20):
    new_player = IA(5 ,50, 30, 3)
    ia_group.add(new_player)

while running:
    screen.fill("black")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    ia_list = ia_group.sprites()
    if len(ia_list) != 0:
        for elem in ia_list:
            stat = elem.__str__()
            pv = stat[3]
            if pv == 0:
                mort=elem.fin()
                statia.append(mort)
                ia_group.remove(elem)

        for elem in ia_list:
            alea = randint(1,5)
            if alea == 1:
                elem.degat()
    else:
        statia.sort(key=lambda M : M[3], reverse=True)
        best=statia[0]
        statia.remove(best)
        for elem in statia:
            vitesse = (best[0]+elem[0])//2
            taille = (best[1]+elem[1])//2
            champ = (best[2]+elem[2])//2
            pv = (best[3]+elem[3])//2
            ia_group.add(IA(vitesse,taille,champ,pv))
        ia_group.add(IA(best[0],best[1],best[2],best[3]))
        statia=[]

    screen.blit(text, textRect)
    

    ia_group.draw(screen)
    pg.display.flip()
    clock.tick(60)

pg.quit()