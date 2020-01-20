# -*- coding: utf-8 -*-

import pygame
import random

pygame.init() # initialisation du module "pygame"

fenetre = pygame.display.set_mode( (600,600) ) # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Esquirol Emma 707   Space Invaders") # Définit le titre de la fenêtre


# Chargement des images:
#    On définit et affecte les variables qui contiendront les images du vaisseau ou de l'alien
image_alien = pygame.image.load("alien.png")
image_vaisseau = pygame.image.load("vaisseau.png")
image_vaisseau = pygame.transform.scale(image_vaisseau, (64, 64)) # On redimensionne l'image du vaisseau à une taille de 64x64 pixels
image_alien = pygame.transform.scale(image_alien, (33, 27))
image_bombe = pygame.image.load("bombe.png")
image_bombe = pygame.transform.scale(image_bombe, (30, 20))

# On définit les variables qui contiendront les positions des différents éléments (vaisseau, alien, projectile)
# Chaque position est un couple de valeur '(x,y)'
position_vaisseau = (300,525)
position_alien = (300,10)
projectiles = []
rectangle_alien = pygame.Rect(position_alien[0],position_alien[1], 33, 27)
rectangle_vaisseau = pygame.Rect(position_vaisseau[0], position_vaisseau[1], 64, 64)

score = 0
nombre_projectiles = 100

se_dirige_vers_la_droite = True
liste_etoiles = []
for _ in range (100):
    liste_etoiles.append ( (random.randrange(601), random.randrange(601)) ) #on ajoute à liste_etoiles des coordonnées au hasard qui représentent les étoiles

vies_alien = 3
vies_vaisseau = 3

bombes = []

# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner():
    global image_alien, image_vaisseau, fenetre, projectiles, liste_etoiles, position_alien, jeu_termine
    # On remplit complètement notre fenêtre avec la couleur noire: (0,0,0)
    # Ceci permet de 'nettoyer' notre fenêtre avant de la dessiner
    fenetre.fill( (0,0,0) )
    fenetre.blit(image_vaisseau, position_vaisseau) # On dessine l'image du vaisseau à sa position
    fenetre.blit(image_alien, (position_alien[0] + 16, position_alien[1]))  # On dessine l'image de l'alien à sa position
    for projectile in projectiles:
        if projectile != (-1, -1):
            pygame.draw.circle(fenetre, (255,0,0), projectile, 5) # On dessine le projectile (un simple petit cercle)

    arial20 = pygame.font.SysFont("arial", 20) #on définit une police de caractère
    surface_score = arial20.render("Score =" +str(score), True, pygame.Color(211,200,51)) #on définit l'affichage du score
    fenetre.blit(surface_score, (10,10)) # on définit l'emplacement de la surface d'écriture pour le score
    surface_nombre_projectiles = arial20.render("Projectiles =" + str(nombre_projectiles), True, pygame.Color(211,200,51)) #on définit l'affichage du nombre de projectiles restants
    fenetre.blit(surface_nombre_projectiles, (10,30)) #emplacement de la surface d'écriture pour le nb de projectiles restants
    surface_vies_alien = arial20.render("Vies de l'alien = " + str(vies_alien), True, pygame.Color(211, 200, 51)) #on définit l'affichage du nombre de vies de l'alien
    fenetre.blit(surface_vies_alien, (10,50)) #emplacement de la surface d'écriture du nombre de vies restantes pour l'alien
    surface_vies_vaisseau = arial20.render("Vies du vaisseau =" + str(vies_vaisseau), True, pygame.Color(211, 200, 51))
    fenetre. blit(surface_vies_vaisseau, (400, 10))
    for etoile in liste_etoiles:
        pygame.draw.circle(fenetre, (255, 255, 255), etoile, 2) # on dessine les étoiles
    arial50 = pygame.font.SysFont("arial", 50) #on initialise une nouvelle police de caractère
    if vies_alien == 0: #on affiche un message si on gagne (ou si on perd)
        surface_zone_victoire = arial50.render("TU AS GAGNÉ! Bravo!", True, pygame.Color(211, 200, 51))
        jeu_termine = True
        fenetre.blit(surface_zone_victoire, (50, 275))
    arial40 = pygame.font.SysFont("arial", 40)
    if position_alien[1] + 27 >= 600 or vies_vaisseau == 0:
        position_alien = (900, 900)
        surface_zone_defaite = arial40.render("DOMMAGE, TU AS PERDU...", True, pygame.Color(211, 200, 51))
        jeu_termine = True
        fenetre.blit(surface_zone_defaite, (50, 275))
    for bombe in bombes:
        fenetre.blit(image_bombe, bombe)
    pygame.display.flip() # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin


# Fonction en charge de gérer les évènements clavier (ou souris)
# Cette fonction sera appelée depuis notre boucle infinie
def gerer_clavier_souris():
    global continuer, position_vaisseau, projectiles, nombre_projectiles
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
        #on vérifie si la barre espace est pressée et si oui on vérifie s'il reste des projectiles
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if nombre_projectiles > 0:
                projectiles.append( (position_vaisseau[0] + 32 ,position_vaisseau[1]) )
                nombre_projectiles -= 1 
                laser = pygame.mixer.Sound("sf_laser_15.wav") #lorsque le vaisseau tire un projectile on entend un bruit de laser
                laser.play()

    # Gestion du clavier: Quelles touches sont pressées ?
    touches_pressees = pygame.key.get_pressed()
    if touches_pressees[pygame.K_RIGHT] == True and position_vaisseau[0]+64 < 600:
        position_vaisseau = ( position_vaisseau[0] + 5 , position_vaisseau[1] )

    if touches_pressees[pygame.K_LEFT] == True and position_vaisseau[0] > 0:
        position_vaisseau = (position_vaisseau[0] - 5, position_vaisseau[1])

    if touches_pressees[pygame.K_UP] == True and position_vaisseau[1] > 0:
        position_vaisseau = (position_vaisseau[0], position_vaisseau[1] - 5)

    if touches_pressees[pygame.K_DOWN] == True and position_vaisseau[1] + 64 < 600:
        position_vaisseau = (position_vaisseau[0], position_vaisseau[1] + 5)
    rectangle_vaisseau = pygame.Rect(position_vaisseau[0], position_vaisseau[1], 64, 64)

# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()

# La boucle infinie de pygame:
# On va continuellement dessiner sur la fenêtre, gérer les évènements et calculer certains déplacements
continuer = 1
jeu_termine = False
while continuer==1:
    # pygame permet de fixer la vitesse de notre boucle:
    # ici on déclare 50 tours par secondes soit une animation à 50 images par secondes
    clock.tick(50)

    dessiner()
    gerer_clavier_souris()
    if not jeu_termine:
        if position_alien != (-1, -1):
            if random.randint(0, 100) == 1: #on tire un nombre au hasard et s'il est égal à 1 il envoie une bombe
                    bombes.append((position_alien[0] + 16,position_alien[1]))
                    
    #L'alien se décale de droite à gauche ou de gauche à droite
            if se_dirige_vers_la_droite:
                position_alien = (position_alien[0] + 2,position_alien[1]) 
            if not se_dirige_vers_la_droite:
                position_alien = (position_alien[0] -2, position_alien[1])
            # Quand l'alien arrive au bord de l'écran il descend de 20 vers le vaisseau
            if position_alien[0] + 33 > 600:
                position_alien = (position_alien[0], position_alien[1] +20)
                se_dirige_vers_la_droite = False
            if position_alien[0] < 0:
                position_alien = (position_alien[0], position_alien[1] +20)
                se_dirige_vers_la_droite = True
            rectangle_alien = pygame.Rect(position_alien[0],position_alien[1], 33, 27)
            #on crée une variable projectile_2 qui va permettre de mettre les coordonnées des projectiles n'ayant 
            #pas dépassé le bas de l'écran
    #on gère la descente des bombes et la collision avec le vaisseau (il perd les vies en un seul coup...)
    bombes_2 = []
    for bombe in bombes:
        bombes_2.append((bombe[0], bombe[1] + 5))
        rectangle_bombe = pygame.Rect(bombe[0], bombe[1], 30, 20)
        if bombe[1] >= 600:
            del bombe #la bombe est supprimée si son ordonnée est supérieure au bas de la fenêtre
        if rectangle_bombe.colliderect(rectangle_vaisseau):
            del bombe
            if vies_vaisseau > 0:
                vies_vaisseau -= 1
            else:
                jeu_termine = True
    bombes = bombes_2
    
    projectiles_2 = []
    for projectile in projectiles:
        #Lorsque l'ordonnée du projectile est supérieure à 0(haut de la fenêtre) on le supprime
        if projectile[1] > 0:
            #Lorsque le projectile touche l'alien, on le supprime et on ajoute 1 au score
            if rectangle_alien.collidepoint(projectile):
                score += 1
                #on entend un bruit d'explosion quand l'alien est touché 
                explosion = pygame.mixer.Sound("sf_explosion_01.wav")
                explosion.play()
                #on gère le nombre de vies de l'alien et quand il n'en a plus on le met à une position lointaine (petite référence à Star Wars (;)
                if vies_alien > 0:
                    vies_alien -= 1 
                if vies_alien == 0:
                    position_alien = (-100, -100) #quand il n'a plus de vies il disparaît (il sort de la fenêtre)
            else:
             # On fait avancer le projectile (si il existe)
                projectiles_2.append( (projectile[0], projectile[1] - 5) ) # le projectile "monte" vers le haut de la fenêtre
    projectiles = projectiles_2 #la liste projectile prend la valeur de projectile_2 (c'est-à-dire que les projectiles supprimés ne sont plus pris en compte)

    liste_etoiles_2 = [] #elle va permettre de recréer des étoiles plaçées au hasard
    for etoile in liste_etoiles:
        if etoile[1]> 600:
            del etoile #Lorsque l'étoile arrive en bas de l'écran on la supprime
            liste_etoiles_2.append((random.randrange(601), 0))
        else:
            liste_etoiles_2.append((etoile[0], etoile[1] + 3)) #si l'étoile est encore dans l'écran, on la fait descendre de 3 (-> impression de mouvement de la part du vaisseau et de l'alien)
    liste_etoiles = liste_etoiles_2
    if jeu_termine == True:
        nombre_projectiles = 0


        
# A la fin, lorsque l'on sortira de la boucle, on demandera à Pygame de quitter proprement
pygame.quit()