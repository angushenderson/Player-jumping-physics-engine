import pygame
import physics_engine as physics


class player(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.isjump = False
        self.jumpdir = 0
        self.jumpcount = 10
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.moveleft = True
        self.moveright = True
        self.onwall = False
        self.iswalljump = False
        self.walljumpcount = 0
        self.maxwalljump = 3
        self.walljumpdir = 0
        self.wallfallvel = 2
        self.wallfallstart = 0
        self.maxfalldist = 50
        self.iswallslip = False
        self.slip = False

    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)


def movement(player):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.iswallslip == 0:
        player.x -= player.vel
        player.update_hitbox()
        physics.wall_check(player, -1)

    elif keys[pygame.K_RIGHT] and player.iswallslip == 0:
        player.x += player.vel
        player.update_hitbox()
        physics.wall_check(player, 1)

    physics.wall_jump_detect(player)

    if not player.isjump:
        if keys[pygame.K_SPACE]:
            player.isjump = True
            if player.onwall and player.walljumpcount < player.maxwalljump:
                print('a')
                player.walljumpcount += 1
                player.iswalljump = True
                player.wallfallstart = 0
                player.jumpcount = 10
            elif player.walljumpcount >= player.maxwalljump:
                print('b')
                physics.wall_slide(player)
                player.onwall = True
                player.isjump = True
                player.slip = True

    if player.isjump or player.iswalljump or player.iswallslip != 0:
        physics.player_jump(player)

    elif player.onwall:
        physics.wall_slide(player)

    if not player.isjump and not player.onwall and not player.iswalljump and player.iswallslip == 0:
        physics.gravity(player)




