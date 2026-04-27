import pygame
from world_generation import *

pygame.init()

LEVEL = 0
SPEED = 13
GRAVITE = 2
VITESSE_SAUT = -27
VITESSE_PAD = -24
FPS = 60

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(f"musiques/world_music_{LEVEL}.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

death_sound = pygame.mixer.Sound("soundeffect/explode.ogg")
death_sound.set_volume(0.2)

win_sound = pygame.mixer.Sound("soundeffect/end.ogg")
win_sound.set_volume(0.7)


def dessiner_fond(screen, bg, camera_x):
    bg_w = bg.get_width()
    bg_h = bg.get_height()
    screen_w, screen_h = screen.get_size()
    start_x = -(camera_x % bg_w)
    x = start_x
    while x < screen_w:
        y = 0
        while y < screen_h:
            screen.blit(bg, (x, y))
            y += bg_h
        x += bg_w


def lanceur():
    running = True
    camera_x = 0
    vitesse_y = 0
    au_sol = False
    game_over = False
    niveau_complete = False
    peut_sauter_orb = True
    player_angle = 0.0
    jump_held = False

    bg = pygame.image.load(image_backgroung(LEVEL))
    map = read_csv(LEVEL)

    skin = {
        "0": pygame.image.load(f"images/texture/block/block_{LEVEL}.png").convert_alpha(),
        "S": pygame.image.load(f"images/texture/object/spike.png").convert_alpha(),
        "J": pygame.image.load(f"images/texture/object/orb-yellow.png").convert_alpha(),
        "P": pygame.image.load(f"images/texture/object/jump-pad-yellow.png").convert_alpha(),
        "B": pygame.image.load(f"images/texture/player_skin/avatar.png").convert_alpha(),
    }

    player_x, player_y = trouver_joueur(map)
    player_largeur = skin["B"].get_width()
    player_hauteur = skin["B"].get_height()

    font_big = pygame.font.SysFont(None, 100)
    font_small = pygame.font.SysFont(None, 50)
    screen_w, screen_h = screen.get_size()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and (game_over or niveau_complete):
                    lanceur()
                    return
                if event.key in (pygame.K_SPACE, pygame.K_UP) and not game_over and not niveau_complete:
                    jump_held = True
                    cx = player_x - 350
                    if au_sol:
                        vitesse_y = VITESSE_SAUT
                    elif collision_orb(map, cx, player_y, player_largeur, player_hauteur) and peut_sauter_orb:
                        vitesse_y = VITESSE_SAUT
                        peut_sauter_orb = False
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    jump_held = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over and not niveau_complete:
                    jump_held = True
                    cx = player_x - 350
                    if au_sol:
                        vitesse_y = VITESSE_SAUT
                    elif collision_orb(map, cx, player_y, player_largeur, player_hauteur) and peut_sauter_orb:
                        vitesse_y = VITESSE_SAUT
                        peut_sauter_orb = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    jump_held = False

        dessiner_fond(screen, bg, camera_x)

        if not game_over and not niveau_complete:
            camera_x += SPEED
            player_x += SPEED

            prochain_x = player_x

            cx = prochain_x - 350
            if collision_bloc(map, cx, player_y, player_largeur, player_hauteur):
                game_over = True
                death_sound.play()

            cx = player_x - 350
            vitesse_y += GRAVITE

            # Jump pad
            if collision_pad(map, cx, player_y, player_largeur, player_hauteur) and vitesse_y >= 0:
                vitesse_y = VITESSE_PAD

            # Vertical movement + collision
            prochain_y = player_y + vitesse_y
            if collision_bloc(map, cx, prochain_y, player_largeur, player_hauteur):
                if vitesse_y > 0:
                    while not collision_bloc(map, cx, player_y + 1, player_largeur, player_hauteur):
                        player_y += 1
                    au_sol = True
                else:
                    au_sol = False
                vitesse_y = 0
            else:
                player_y = prochain_y
                au_sol = False

            if au_sol:
                peut_sauter_orb = True
                player_angle = round(player_angle / 90) * 90
                if jump_held:
                    vitesse_y = VITESSE_SAUT
            else:
                player_angle -= 2.5

            # Mort
            if collision_spike(map, cx, player_y, player_largeur, player_hauteur):
                game_over = True
                death_sound.play()
            if player_y > screen_h:
                game_over = True

            # Fin Level
            if fin_niveau():
                niveau_complete = True
                win_sound.play()

        build_map(screen, camera_x, 0, skin, map)
        draw_player(screen, camera_x, skin, player_x, player_y, player_angle)

        if game_over:
            text = font_big.render("GAME OVER", True, (255, 50, 50))
            sub = font_small.render("R pour relancer  |  ESC pour quitter", True, (255, 255, 255))
            screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - 80))
            screen.blit(sub, (screen_w // 2 - sub.get_width() // 2, screen_h // 2 + 20))

            pygame.mixer.music.stop()

        elif niveau_complete:
            text = font_big.render("NIVEAU TERMINÉ !", True, (50, 255, 100))
            sub = font_small.render("R pour relancer  |  ESC pour quitter", True, (255, 255, 255))
            screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - 80))
            screen.blit(sub, (screen_w // 2 - sub.get_width() // 2, screen_h // 2 + 20))
            pygame.mixer.music.stop()

        pygame.display.update()

    pygame.quit()


lanceur()
