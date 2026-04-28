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

    colonne_camera = int(camera_x // size)

    x_debut = max(0, colonne_camera - 2)
    x_fin = min(len(map[0]), colonne_camera + 24 + 2)

def fin_niveau():
    for ligne in map_actuelle:
        for val in ligne:
            if val == "End":
                return True
    return False

def trouver_joueur(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == "B":
                return x * 80, y * 80 - 400
    return 0, 0


def collision_bloc(map, x, y, largeur, hauteur):
    size = 80

    gauche = int(x // size)
    droite = int((x + largeur - 1) // size)
    haut = int((y + 400) // size)
    bas = int((y + 400 + hauteur - 1) // size)

    for j in range(haut, bas + 1):
        for i in range(gauche, droite + 1):
            if 0 <= j < len(map) and 0 <= i < len(map[0]):
                if map[j][i] == "0":
                    return True
    return False


def collision_spike(map, x, y, largeur, hauteur):
    size = 80

    marge_x = 18
    marge_y = 10

    gauche = int((x + marge_x) // size)
    droite = int((x + largeur - 1 - marge_x) // size)
    haut = int((y + 400 + marge_y) // size)
    bas = int((y + 400 + hauteur - 1) // size)

    for j in range(haut, bas + 1):
        for i in range(gauche, droite + 1):
            if 0 <= j < len(map) and 0 <= i < len(map[0]):
                if map[j][i] == "S":
                    return True
    return False


def collision_pad(map, x, y, largeur, hauteur):
    size = 80
    gauche = int(x // size)
    droite = int((x + largeur - 1) // size)
    haut = int((y + 400) // size)
    bas = int((y + 400 + hauteur - 1) // size)

    for j in range(haut, bas + 1):
        pad_top = j * size - 400 + size - 13  # position visuelle du pad en pixels
        if y + hauteur - 1 < pad_top:
            continue
        for i in range(gauche, droite + 1):
            if 0 <= j < len(map) and 0 <= i < len(map[0]):
                if map[j][i] == "P":
                    return True
    return False


def collision_orb(map, x, y, largeur, hauteur):
    size = 80
    gauche = int(x // size)
    droite = int((x + largeur - 1) // size)
    haut = int((y + 400) // size)
    bas = int((y + 400 + hauteur - 1) // size)

    for j in range(haut, bas + 1):
        for i in range(gauche, droite + 1):
            if 0 <= j < len(map) and 0 <= i < len(map[0]):
                if map[j][i] == "J":
                    return True
    return False


def draw_player(screen, camera_x, skin, player_x, player_y, angle=0):
    player = skin["B"]
    offset_x = 350
    rotated = pygame.transform.rotate(player, angle)
    orig_w, orig_h = player.get_size()
    rot_w, rot_h = rotated.get_size()
    dx = (rot_w - orig_w) // 2
    dy = (rot_h - orig_h) // 2
    screen.blit(rotated, (player_x - camera_x - offset_x - dx, player_y - dy))