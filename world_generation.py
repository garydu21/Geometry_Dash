import csv, pygame.draw

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
    hauteur = len(map)
    longeur = len(map[0])
    size = 80
    bloc = skin["0"]

    for y in range(hauteur):
        for x in range(longeur):
            element = map[y][x]
            if element == "0":
                screen.blit(bloc, (x*size - camera_x, y*size - 400))
            if element == "S":
                pygame.draw.rect(screen, (0,255,0),(x*size-camera_x,y*size-400,size,size))