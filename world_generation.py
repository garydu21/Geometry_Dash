import csv, pygame.draw

taille_jeu = 28 # 24 affiché + 2 à gauche et 2 à droite

x_debut = 0
x_fin = 28

map_actuelle = []

def image_backgroung(level):
    return f"images/level1/bg_{level}.png"

def read_csv(level):
    path = f"maps/level_{level}.csv"
    matrice_niveau = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrice_niveau.append(row)
    return matrice_niveau

def build_map(screen,camera_x,camera_y,skin,map):
    global x_debut, x_fin, map_actuelle

    hauteur = len(map)
    map_actuelle = [ligne[x_debut:x_fin] for ligne in map]
    print(map_actuelle)

    size = 80
    bloc = skin["0"]
    spike = skin["S"]
    orb = skin["J"]
    pad = skin["P"]
    player = skin["B"]

    for y in range(hauteur):
        for x in range(len(map_actuelle[0])):
            element = map_actuelle[y][x]
            x_monde = x_debut + x
            if element == "0":
                screen.blit(bloc, (x_monde * size - camera_x, y*size - 400))
            if element == "S":
                screen.blit(spike, (x_monde * size - camera_x, y*size - 400))
            if element == "J":
                screen.blit(orb, (x_monde * size - camera_x, y * size - 400))
            if element == "P":
                screen.blit(pad, (x_monde * size - camera_x, y*size - 400 + 80 - 13)) #80 = taille bloc et 13 = taille pad
            if element == "B":
                screen.blit(player, (x_monde * size - camera_x, y * size - 400))

    colonne_camera = int(camera_x // size)

    x_debut = max(0, colonne_camera - 2)
    x_fin = min(len(map[0]), colonne_camera + 24 + 2)

def fin_niveau():
    return 'End' in map_actuelle[0] and len(map_actuelle[0]) <= taille_jeu - 1