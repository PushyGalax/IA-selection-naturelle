#import
import pygame as pg
from random import *

#prg
class IA:
    def __init__(self, vitesse, taille, champvision, pv) -> None:             #je pense an stat il faut taille, vitesse, pv, champ de vision
        self.vitesse = vitesse
        self.taille = taille
        self.champvision = champvision
        self.pv = pv

    def __str__(self) -> str:               #print des stat de l'objet
        return f"{self.vitesse} {self.taille} {self.champvision}"
    
    def move(self):
        pass

class monstre:
    def __init__(self) -> None:             #les monstres n'évolue pas ils font 1 de dégats et ils ont vitesse const et champ de vision const
        self.VITESSE = 20                   #val à changer
        self.CHAMPVISION = 35

    def __str__(self) -> str:
        pass

class fruit:
    def __init__(self) -> None:             #les fruits n'évolue pas, plus 1 pv quand IA sur fruit
        pass

    def __str__(self) -> str:
        pass


#main