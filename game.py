import pygame

from world_generation import *

# Initialize Pygame
pygame.init()

level = 1

bg = pygame.image.load(image_backgroung(level))

# Set up the game window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Hello Pygame")

def lanceur():
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False
        for x in range(3):
            for y in range(2):
                screen.blit(bg, (x*800, y*800))
        pygame.display.update()



    # Quit Pygame
    pygame.quit()

lanceur()