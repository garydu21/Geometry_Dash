import pygame

from world_generation import *

# Initialize Pygame
pygame.init()

level = 0

bg = pygame.image.load(image_backgroung(level))

# Set up the game window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Hello Pygame")

def lanceur():
    running = True
    camera_x = 0
    speed = 1.5
    gravite = 1
    vitesse_y = 0

    map = read_csv(level)

    skin = {
        "0": pygame.image.load(f"images/texture/block/block_{level}.png").convert_alpha(),
        "S": pygame.image.load(f"images/texture/object/spike.png").convert_alpha(),
        "J": pygame.image.load(f"images/texture/object/orb-yellow.png").convert_alpha(),
        "P": pygame.image.load(f"images/texture/object/jump-pad-yellow.png").convert_alpha(),
        "B": pygame.image.load(f"images/texture/player_skin/avatar.png").convert_alpha(),
    }

    player_x, player_y = trouver_joueur(map)
    player_largeur = skin["B"].get_width()
    player_hauteur = skin["B"].get_height()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        for x in range(15):
            for y in range(2):
                screen.blit(bg, (x * 800 - camera_x, y * 800))

        if not fin_niveau():
            camera_x += speed
            player_x += speed

        vitesse_y += gravite

        prochain_y = player_y + vitesse_y

        if collision_bloc(map, player_x, prochain_y, player_largeur, player_hauteur):
            if vitesse_y > 0:
                while not collision_bloc(map, player_x, player_y + 1, player_largeur, player_hauteur):
                    player_y += 1
            vitesse_y = 0
        else:
            player_y = prochain_y

        build_map(screen, camera_x, 0, skin, map)
        draw_player(screen, camera_x, skin, player_x, player_y)

        pygame.display.update()

    pygame.quit()

lanceur()