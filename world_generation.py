import csv

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

def build_map(level):
    path = f"maps/level_{level}.csv"
    map = read_csv(path)

