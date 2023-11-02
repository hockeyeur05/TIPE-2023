### Bibliothèques
import pygame as py
from pygame.locals import *
from pygame import display

from random import randint,random

import time as tm
from time import monotonic

import numpy as np

# Pour les tracés
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
### Fonctions

def direction(x,y):
    d=(((sortiex-x)**2+(sortiey - y)**2)**(1/2)) #distance avec la sortie
    dx, dy = (sortiex- x)/d, (sortiey - y)/d+(y-bord2/2)/700
    return(dx,dy)

def direction_fond(x,y):
    d=(((bord1-x)**2+(sortiey - y)**2)**(1/2)) #distance avec la sortie
    dx, dy = (bord1- x)/d, (sortiey - y)/d+(y-bord2/2)/700
    return(dx,dy)

def dist(xa,xb,ya,yb):
    """ distance entre deux points """
    return ((xb-xa)**2 + (yb-ya)**2)**(1/2)

### Paramètres
py.init()

start=monotonic() #début du chrono
vert= (150, 200, 0)
violet = (46,26,71)
orange= (255, 120, 50)
bord1,bord2=1000,700 #taille de la fenêtre

fenetre = py.display.set_mode((bord1,bord2))
fenetre.fill((255,255,255))

depart=50 #population de départ
time=30 #temps maximal de la simulation
rayon=10 #demi largeur d'un humain (dans  la modélisation)
V = 1.5 #en m.s

#localisation de la sortie
sortiex1=bord1*80/100
sortiex2=bord1*80/100
sortiey1=0
sortiey2=bord1*70/100
sortiex=abs(sortiex1+sortiex2)/2
sortiey=abs(sortiey1+sortiey2)/2

#initialisation des listes
humains=[]
lx=[]
ly=[]
lvx=[]
lvy=[]

#on tire un humain au hasard pour le tracé
n = randint(0,depart-1)

#obstacles
porte_haut = [(bord1,0), (bord1*80/100, 0), (bord1*80/100, bord2*40/100),(bord1,bord2*40/100)]
porte_bas = [(bord1,bord2), (bord1*80/100,bord2), (bord1*80/100, bord2*60/100),(bord1,bord2*60/100)]
poteau1 = (sortiex-150,sortiey)
poteau2 = (sortiex-150,sortiey+150)
poteau3 = (sortiex-150,sortiey-150)
rayon_poteau1 = 20
rayon_poteau2 = 20
rayon_poteau3 = 20
panneau = [ (sortiex1*60/100,sortiey*130/100), (sortiex1*70/100,sortiey*130/100), (sortiex1*70/100,sortiey*60/100), (sortiex1*60/100,sortiey*60/100) ]

### Classe
class humain:
    def __init__(self,x,y,vx,vy,color):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.color=color

	def draw(self):
		py.draw.circle(fenetre, self.color, (round(self.x), round(self.y)), rayon)

#réaction aux différents obstacles (on peut les choisir en les prenant en compte dans la fonction move et en les affichant ou non)

    def react_poteau1(self):
        distx = poteau1[0] - self.x
        disty = poteau1[1] - self.y
        distp = (distx**2+disty**2)**(1/2)
        if (distp < rayon_poteau1 + rayon + 10):
            dx,dy=direction(self.x,self.y)
            self.x -= dx
            self.x += 0.6*1.5

            if self.y >= poteau1[1]:
                c = 0.6
            else:
                c = -0.6

            self.y -= dy
            self.y += c*1.5

    def react_poteau2(self):
        distx = poteau2[0] - self.x
        disty = poteau2[1] - self.y
        distp = (distx**2+disty**2)**(1/2)
        if (distp < rayon_poteau2 + rayon + 10):
            dx,dy=direction(self.x,self.y)
            self.x -= dx
            self.x += 0.6*1.5

            if self.y >= poteau2[1]:
                c = 0.6
            else:
                c = -0.6

            self.y -= dy
            self.y += c*1.5

    def react_poteau3(self):
        distx = poteau3[0] - self.x
        disty = poteau3[1] - self.y
        distp = (distx**2+disty**2)**(1/2)
        if (distp < rayon_poteau3 + rayon + 10):
            dx,dy=direction(self.x,self.y)
            self.x -= dx
            self.x += 0.6*1.5

            if self.y >= poteau3[1]:
                c = 0.6
            else:
                c = -0.6

            self.y -= dy
            self.y += c*1.5

    def react_panneau(self):
        xg = panneau[0][0]
        xd = panneau[1][0]
        yh = panneau[0][1]
        yb = panneau[2][1]
        milieuy = (yh + yb)/2
        milieux = (xg + xd)/2
        distx = milieux - self.x
        disty = milieuy - self.y
        distp = (distx**2+disty**2)**(1/2)
        if (distp <= dist(xg,milieux,yh,milieuy)+ rayon + 10 ):
            dx,dy=direction(self.x,self.y)
            if self.y <= yh + rayon + 10 and self.y >= yb - rayon - 10 :
                if self.y >= milieuy :
                    c = 0.6
                else:
                    c = -0.6

                self.y -= dy
                self.y += c*1.5

    def collision(self,population):
        for other in population:
            if self!=other:
                d=dist(self.x,other.x,self.y,other.y)

                if d <= 2*rayon:
                    tm.sleep(0.00005)
                    self.color= violet
                    other.color= violet
                    dx=min(self.x,other.x)
                    if dx== self.x:
                        self.vx-=-d/100
                        self.x-=self.x/100
                    else:
                        other.vx-=d/100
                        other.x-=other.x/100

                elif d<= 3*rayon:
                    tm.sleep(0.00005)
                    self.color=orange
                    other.color=orange
                    dx=min(self.x,other.x)
                    if dx== self.x:
                        self.vx-=-d/100
                        self.x-=self.x/100
                    else:
                        other.vx-=d/100
                        other.x-=other.x/100

    def goal(self):
        dx,dy=direction(self.x,self.y)
        if self.x <sortiex*98/100:
            self.x += dx
            self.y += dy
        else:
            self.x+=self.vx
            self.y+=self.vy

    def entree(self):
		if self.x >= bord1*78/100 and self.y >= bord2*43/100 and self.y < bord2*57/100:
		    self.vy=0
		    self.vx = V

    def move(self,population):
        """ définit le comportement d'un humain selon sa position """
        self.react_poteau1()
        self.react_poteau2()
        self.react_poteau3()
        #self.react_panneau()
        self.collision(population)
        self.goal()
        self.entree()


### Initialisation
x=2*rayon
y=2*rayon

#départ organisé
for i in range(depart):
    if y <= bord2*90/100:
        y+=4*rayon
    else:
        y-=y-4*rayon
        x+=4*rayon

    vx=randint(0, 150)/100
    vy=(V**2 - vx**2)**0.5
    nv_humain=humain(x, y, vx, vy,vert) #création d'un nouvel humain avec les caractéristiques précédentes
    humains.append(nv_humain) #on l'ajoute à la liste des humains

### Boucle principale
continuer= True
while continuer == True:

    #affichage de la fenêtre
    fenetre.fill((255, 255, 255))

    #affichage des obstacles
    py.draw.polygon(fenetre, (0, 0, 0), porte_bas)
    py.draw.polygon(fenetre, (0, 0, 0), porte_haut)
    py.draw.circle(fenetre,(0,0,0),poteau1,rayon_poteau1)
    py.draw.circle(fenetre,(0,0,0),poteau2,rayon_poteau2)
    py.draw.circle(fenetre,(0,0,0),poteau3,rayon_poteau3)
    #py.draw.polygon(fenetre, (0, 0, 0), panneau)

    #arrêt de la simulation si on le souhaite
    for event in py.event.get():
        if event.type == QUIT:
            continuer = False

    keys = py.key.get_pressed()
    #on affiche le temps lors de la pression sur le bouton "entrer"
    if keys[py.K_RETURN]:
        fin=monotonic()-start
        tm.sleep(1)
        print(fin)

    #on peut figer les humains
    elif keys[py.K_SPACE]:
        for humain in humains:
            (dx,dy)=direction(humain.x,humain.y)
            humain.x-=dx
            humain.y-=dy

    # affichage des humains
    for humain in humains:
        humain.move(humains)
        humain.draw()
    py.display.flip()

#Pour le tracé
    h=humains[n] #choix d'un point pour le futur tracé
    #on ajoute ses caractéristiques dans des listes au fil du temps
    (dx,dy)=direction(h.x,h.y)
    lx.append(h.x)
    ly.append(h.y)
    lvx.append(h.vx)
    lvy.append(h.vy)

    #si on dépasse le temps maximal on arrête la simulation
    if monotonic()-start >= time:
        continuer = False
py.quit()

### trace de la vitesse en fonction des positions
# Tableau pour les 3 axes
LVX,LVY = np.meshgrid(lvx,lvy)
V = dist(0,LVX,0,LVY)
X,Y=np.meshgrid(lx,ly)

# Tracé du résultat en 3D
fig = plt.figure(figsize = (10,7))
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, V, cmap=cm.coolwarm, linewidth=0)
ax.set_title("Vitesse en fonction des positions", fontsize = 13)
ax.set_xlabel('X', fontsize = 11)
ax.set_ylabel('Y', fontsize = 11)
ax.set_zlabel('vitesse', fontsize = 11)
plt.show()