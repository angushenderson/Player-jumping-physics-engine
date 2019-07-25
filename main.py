import pygame
import level_builder
import settings
import player
pygame.init()
settings.build_init()
win_width = 1300
win_height = 650
drawing_status = False
mode = 'build'

win = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()


def redrawGameWindow(win):
    pygame.draw.rect(win, (255, 255, 255), (0, 0, 1300, 650))
    for p in settings.platforms:
        pygame.draw.rect(win, (0, 0, 0), (p[0], p[1], p[2], p[3]))
    man.draw(win)
    pygame.display.update()

run = True

man = player.player(100, 600, 50, 50, 5)

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if mode == 'build':
        platforms, drawing_status = level_builder.build(win, settings.platforms, drawing_status)
        player.movement(man)

    redrawGameWindow(win)

pygame.quit()


