import time
from pynput.keyboard import *

from world_generation import *

level = 1

taille_jeu = 16

compteur = 0

map_complete = read_csv(level)
hauteur = len(map_complete)
longeur = len(map_complete[0])

map_matrice = [ligne[:taille_jeu] for ligne in map_complete]

joueur_x = 0
joueur_y = 0

saute = False
saut_restant = 0

vitesse = 1


def render_console(level):
    global map_matrice, hauteur, longeur

    apparition_joueur()

    compteur,niveau_fini = avancement()

    while not niveau_fini:
        physique()
        for x in range(hauteur):
            for y in range(taille_jeu):
                if x == joueur_x and y == joueur_y:
                    print('b', end='  ')
                else:
                    print(map_matrice[x][y], end='  ')
            print()

        compteur, niveau_fini = avancement()
        time.sleep(vitesse)

def apparition_joueur():
    global joueur_x, joueur_y

    flag_first_bloc = False
    i = hauteur - 1

    while (not flag_first_bloc) and i > 0:
        flag_first_bloc = map_matrice[i][0] == '1'
        if not flag_first_bloc:
            i -= 1

    joueur_x = i
    joueur_y = 0


def avancement():
    global joueur_x, joueur_y, compteur, map_matrice

    niveau_fini = compteur == longeur - 1

    if compteur <= 3:
        joueur_y += 1
        compteur += 1
    else:
        for col in range(taille_jeu - 1):
            for lig in range(hauteur):
                map_matrice[lig][col] = map_matrice[lig][col + 1]

        prochaine_colonne = compteur + 1

        for lig in range(hauteur):
            if prochaine_colonne < longeur:
                map_matrice[lig][taille_jeu - 1] = map_complete[lig][prochaine_colonne]
            else:
                map_matrice[lig][taille_jeu - 1] = '0'

        compteur += 1

    return compteur, niveau_fini

def au_sol():
    global joueur_x, joueur_y
    if map_matrice[joueur_x+1][joueur_y] == '0':
        return True
    return False

def physique():
    global joueur_x, joueur_y, saute, saut_restant

    if not saute and au_sol():
        saut_restant = 2

    if saute:
        if saut_restant == 2:
            if joueur_x > 0 and map_matrice[joueur_x - 1][joueur_y] != '1':
                joueur_x -= 1
            saut_restant -= 1
            print("ici")
        elif saut_restant == 0:
            joueur_x += 1
            saute = False
        else:
            saut_restant -= 1




def on_press(key):
    global saute
    if key == Key.space:
        saute = True

listener = Listener(on_press=on_press)
listener.start()

render_console(level)

listener.stop()