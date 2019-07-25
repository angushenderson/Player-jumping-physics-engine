# physics engine for player jumping
import settings


def jump_equation(player):
    if player.iswallslip == -1 or player.iswallslip == 1:
        player.x += player.vel * player.iswallslip
        player.update_hitbox()
        wall_check(player, player.iswallslip)
    if player.iswalljump:
        player.x += player.vel * 2 * player.walljumpdir
        player.update_hitbox()
        wall_check(player, player.walljumpdir)
    player.y -= (player.jumpcount ** 2) * 0.5 * player.jumpdir
    player.update_hitbox()


def platform_collision_detect(player, platform):
    if player[1] < platform[1] + platform[3] and player[1] + player[3] > platform[1]:
        if player[0] + player[2] > platform[0] and player[0] < platform[0] + platform[2]:
            return True
    return False


def player_jump(player):
    if player.jumpcount < 0:
        player.jumpdir = -1
    else:
        player.jumpdir = 1
    if player.jumpcount <= -10:
        player.jumpcount = -10
    old_hitbox = player.hitbox[:]
    jump_equation(player)
    player.jumpcount -= 1
    if player.jumpdir == -1:
        jump_hitbox = [old_hitbox[0], old_hitbox[1], old_hitbox[2], old_hitbox[3] + (old_hitbox[1] - player.hitbox[1])]
    elif player.jumpdir == 1:
        jump_hitbox = [player.hitbox[0], player.hitbox[1], player.hitbox[2], player.hitbox[3] + (player.hitbox[1] - old_hitbox[1])]
    # detect on top of platform
    if head_check(player, jump_hitbox):
        for p in settings.platforms:
            #if platform_collision_detect(player.hitbox, p)
            if jump_hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] > p[1]:
                if player.hitbox[0] + player.hitbox[2] > p[0] and player.hitbox[0] < p[0] + p[2]:
                    # alligned with platform
                    player.y = p[1] - player.hitbox[3]
                    player.update_hitbox()
                    player.isjump = False
                    player.jumpcount = 10
    if player.hitbox[1] + player.hitbox[3] >= 650:
        player.y = 650 - player.hitbox[3]
        player.update_hitbox()
        player.isjump = False
        player.jumpcount = 10


def onground(player):
    for p in settings.platforms:
        if player.hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] >= p[1]:
            if player.hitbox[0] + player.hitbox[2] > p[0] and player.hitbox[0] < p[0] + p[2]:
                player.isjump = False
                player.onwall = False
                player.iswalljump = False
                player.iswallslip = 0
                player.walljumpcount = 0
                return True
    if player.hitbox[1] + player.hitbox[3] >= 650:
        player.iswalljump = False
        player.iswallslip = 0
        player.walljumpcount = 0
        return True
    return False


def gravity(player):
    if not onground(player):
        player.isjump = True
        player.jumpdir = -1
        player.jumpcount = -1


def head_check(player, jump_hitbox):
    for p in settings.platforms:
        if player.jumpdir == 1:
            if jump_hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] > p[1]:
                if player.hitbox[0] + player.hitbox[2] > p[0] and player.hitbox[0] < p[0] + p[2]:
                    player.y = p[1] + p[3] + 1
                    player.update_hitbox()
                    player.jumpdir = -1
                    player.jumpcount = 0
                    player.isjump = True
                    return False
    return True


def wall_check(player, direction):    # this isn't working here for wall collisions
    for p in settings.platforms:
        if direction == -1:    # left
            if player.hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] > p[1]:
                if player.hitbox[0] + player.hitbox[2] > p[0] - player.vel and player.hitbox[0] < p[0] + p[2]:
                    player.x = p[0] + p[2]
                    player.update_hitbox()
                    player.moveleft = False
                    player.moveright = True
                    player.iswallslip = False
                    break

        elif direction == 1:   # right
            if player.hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] > p[1]:
                if player.hitbox[0] + player.hitbox[2] > p[0] and player.hitbox[0] < p[0] + p[2] + player.vel:
                    player.x = p[0] - player.width
                    player.update_hitbox()
                    player.moveright = False
                    player.moveleft = True
                    player.iswallslip = False
                    break

        else:
            player.moveright = True
            player.moveleft = True


def wall_jump_detect(player):
    if not onground(player) and player.jumpdir == -1:
        for p in settings.platforms:
            if player.hitbox[0] == p[0] + p[2]:   # left
                if player.hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] > p[1]:
                    # on a left hand wall
                    player.onwall = True
                    player.iswalljump = False
                    player.isjump = False
                    player.jumpcount = 0
                    player.jumpdir = -1
                    player.walljumpdir = 1     # going to the right
                    break

            elif player.hitbox[0] + player.hitbox[2] == p[0]:
                if player.hitbox[1] < p[1] + p[3] and player.hitbox[1] + player.hitbox[3] > p[1]:
                    # collided with right hand wall
                    player.onwall = True
                    player.iswalljump = False
                    player.isjump = False
                    player.jumpcount = 0
                    player.jumpdir = -1
                    player.walljumpdir = -1    # going to the left
                    break
            else:
                player.onwall = False

    else:
        player.onwall = False


def wall_slide(player):
    if player.wallfallstart == 0:
        player.wallfallstart = player.hitbox[1]
    player.y += player.wallfallvel
    if player.y - player.wallfallstart >= player.maxfalldist or player.slip:
        player.slip = False
        player.onwall = False
        player.wallfallstart = 0
        player.walljumpcount = 0
        if player.walljumpdir == -1:
            player.iswallslip = -1
            player.isjump = True
            player.jumpcount = -1
            player.jumpdir = -1
        else:
            player.iswallslip = 1
            player.isjump = True
            player.jumpcount = -1
            player.jumpdir = -1
    player.update_hitbox()





