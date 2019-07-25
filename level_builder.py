import pygame
import settings

def build(win, platforms, drawing_status):
    mouse = pygame.mouse.get_pressed()
    if drawing_status == False and mouse[0] == 1:
        settings.pos = pygame.mouse.get_pos()
        settings.platforms.append([settings.pos[0],
                                   settings.pos[1],
                                   pygame.mouse.get_pos()[0] - settings.pos[0],
                                   pygame.mouse.get_pos()[1] - settings.pos[1]])
        drawing_status = True
    if mouse[0] == 1:
        settings.platforms[-1] = ([settings.pos[0],
                                       settings.pos[1],
                                       pygame.mouse.get_pos()[0] - settings.pos[0],
                                       pygame.mouse.get_pos()[1] - settings.pos[1]])
    if drawing_status and mouse[0] == 0:
        settings.pos = (settings.pos) + pygame.mouse.get_pos()
        pos_box = ([settings.pos[0],
                    settings.pos[1],
                    pygame.mouse.get_pos()[0] - settings.pos[0],
                    pygame.mouse.get_pos()[1] - settings.pos[1]])
        settings.platforms.append(pos_box)
        settings.pos = ()
        drawing_status = False
    return platforms, drawing_status

def run():
    pass