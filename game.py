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
    # Game loop
    running = True
    camera_x = 0
    speed = 10
    map = read_csv(level)
    skin = {
        "0": pygame.image.load(f"images/texture/block/block_{level}.png").convert_alpha(),
        "S" : pygame.image.load(f"images/texture/object/spike.png").convert_alpha(),
        "J" : pygame.image.load(f"images/texture/object/orb-yellow.png").convert_alpha(),
        "P" : pygame.image.load(f"images/texture/object/jump-pad-yellow.png").convert_alpha(),
        "B" : pygame.image.load(f"images/texture/player_skin/avatar.png").convert_alpha(),
            }
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
        build_map(screen,camera_x,0,skin,map)
        pygame.display.update()

        if not fin_niveau():
            camera_x += speed


    # Quit Pygame
    pygame.quit()

lanceur()