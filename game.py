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
    speed = 1.5
    map = read_csv(level)
    skin = {
        "0": pygame.image.load(f"images/block_texture/block_{level}.png").convert_alpha()
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
        camera_x += speed


    # Quit Pygame
    pygame.quit()

lanceur()