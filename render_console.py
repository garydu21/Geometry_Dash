from world_generation import *

level = 1

def render_console(level):
    map_matrice = read_csv(level)

    hauteur = len(map_matrice)
    longeur = len(map_matrice[0])

    for x in range(hauteur):
        for y in range(longeur):
            print(map_matrice[x][y], end='  ')
        print()

render_console(level)