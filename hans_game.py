import pygame
from sys import exit
from random import randint, choice
import helpful_functions
from sympy import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        empty = pygame.image.load("graphics/background/empty.png")
        empty = pygame.transform.scale(empty, player_dimension)
        player_stunned = pygame.image.load("graphics/Player/hans_stuned.png")
        player_stunned = pygame.transform.scale(player_stunned, player_dimension)
        player_walk_1 = pygame.image.load("graphics/Player/Hans_springe.png")
        player_walk_1 = pygame.transform.scale(player_walk_1, player_dimension)
        player_walk_2 = pygame.image.load("graphics/Player/Hand_springe2.png")
        player_walk_2 = pygame.transform.scale(player_walk_2, player_dimension)
        self.player_walk_list = [player_walk_1, player_walk_2]
        self.player_stunned_list = [player_stunned, empty]
        self.stunned_index = 0
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/Hans_hopping.png")
        self.player_jump = pygame.transform.scale(self.player_jump, player_dimension)
        self.player_crouch = pygame.image.load("graphics/Player/Hans_hopping.png")
        self.player_crouch = pygame.transform.scale(self.player_crouch, (68, 40))
        self.player_duble_jump = pygame.image.load("graphics/Player/evil_hans.png")
        self.player_duble_jump = pygame.transform.scale(self.player_duble_jump, player_dimension)

        self.image = self.player_walk_list[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.y_velocity = 0
        self.sound = pygame.mixer.Sound("audio/jump.mp3")


    def player_input(self):
        global allredy_double_jumped
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and not keys[pygame.K_LSHIFT] and not disable_ability \
                or keys[pygame.K_UP] and self.rect.bottom >= 300 and not keys[pygame.K_LSHIFT] and not disable_ability:
            self.y_velocity = -16
            self.sound.play()
            allredy_double_jumped = False

        elif not disable_ability and double_jump and not allredy_double_jumped and do_double_jump:
            self.y_velocity -= 12
            allredy_double_jumped = True
            thomas_wind_group.add(Boss2Wind(self.rect.bottom + 110, width=self.rect.right, from_player=True))

        elif keys[pygame.K_LSHIFT] and self.rect.bottom >= 300 and crouch \
                and not disable_ability or keys[pygame.K_DOWN] and self.rect.bottom >= 300 and crouch \
                and not disable_ability:
            self.image = self.player_crouch
            self.rect = self.image.get_rect(midbottom=(80, 300))
        else:
            self.image = self.player_walk_list[int(self.player_index)]

    def apply_gravity(self):
        self.y_velocity = helpful_functions.give_rect_movement(self.rect, velocity_y=self.y_velocity,
                                                               acceleration_y=gravity)
        global do_double_jump
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            do_double_jump = False

    def animation_state(self):
        if player_stunned:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_list):
                self.player_index = 0
            self.image = self.player_stunned_list[int(self.player_index)]
            self.rect = self.image.get_rect(midbottom=(80, 320))

        if self.rect.bottom < 300:
            self.image = self.player_jump
        elif self.image != self.player_crouch and not player_stunned:
            self.rect = self.image.get_rect(midbottom=(80, 300))
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_list):
                self.player_index = 0
            self.image = self.player_walk_list[int(self.player_index)]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and do_double_jump and double_jump or \
                keys[pygame.K_UP] and do_double_jump and double_jump:
            self.image = self.player_duble_jump

    def bounce_of_enemy(self):
        if boss_fight_nr_list[0]:
            if self.rect.left < boss_1.david_boss_rect.right and self.rect.right > boss_1.david_boss_rect.left \
                    and self.rect.bottom <= boss_1.david_boss_rect.top:
                if not boss_1.retreat:
                    self.y_velocity = -20
        if boss_fight_nr_list[1]:
            if self.rect.left < boss_2.rect.right and self.rect.right > boss_2.rect.left \
                    and self.rect.bottom <= boss_2.rect.top:
                if not boss_2.retreat:
                    self.y_velocity = -20

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.bounce_of_enemy()


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()
        if type == "thomas":
            fly_frame_1 = pygame.image.load("graphics/Fly/Thomas_flyge.png").convert_alpha()
            fly_frame_1 = pygame.transform.scale(fly_frame_1, thomas_dimension)
            fly_frame_2 = pygame.image.load("graphics/Fly/Thomas_flyge_2.png").convert_alpha()
            fly_frame_2 = pygame.transform.scale(fly_frame_2, thomas_dimension)
            self.frame_list = [fly_frame_1, fly_frame_2]
            y_pos = choice([220, 260])
        elif type == "david":
            david_frame_1 = pygame.image.load("graphics/snail/david_krype1.png").convert_alpha()
            david_frame_1 = pygame.transform.scale(david_frame_1, david_dimension)
            david_frame_1 = pygame.transform.rotozoom(david_frame_1, 0, 1)

            david_frame_2 = pygame.image.load("graphics/snail/david_krype_2.png").convert_alpha()
            david_frame_2 = pygame.transform.scale(david_frame_2, david_dimension)
            david_frame_2 = pygame.transform.rotozoom(david_frame_2, 0, 1)
            self.frame_list = [david_frame_1, david_frame_2]
            y_pos = 320

        self.animation_index = 0
        self.image = self.frame_list[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1000, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.05
        if self.animation_index >= len(self.frame_list): self.animation_index = 0
        self.image = self.frame_list[int(self.animation_index)]

    def destroy(self):
        global score, high_score, celebration, score_game_mode_2, score_game_mode_3
        if self.rect.right < 0:
            self.kill()
        elif self.rect.top - 20 < player.sprite.rect.bottom < self.rect.top and self.rect.left + 30 < player.sprite.rect.right and self.rect.right > player.sprite.rect.left:
            self.kill()

            if game_mode_nr_list[0]:
                score += 1
            elif player.sprite.rect.bottom < 250:
                # thomas_deth.play()
                if game_mode_nr_list[1]:
                    score_game_mode_2 += 2
                elif game_mode_nr_list[3]:
                    score_game_mode_3 += 2
                score += 2
            else:
                # david_deth.play()
                if game_mode_nr_list[1]:
                    score_game_mode_2 += 1
                elif game_mode_nr_list[3]:
                    score_game_mode_3 += 1
                score += 1
            # High score
            if high_score <= score:
                high_score = score
                celebration = True

    def update(self):
        self.animation_state()
        self.rect.x += obstacle_speed
        self.destroy()


class Boss1:
    def __init__(self):
        self.lives = 3
        self.david_boss_surf = pygame.image.load("graphics/snail/david_krype_2.png")
        self.david_boss_surf = pygame.transform.rotozoom(self.david_boss_surf, 0, 0.7)
        self.david_boss_rect = self.david_boss_surf.get_rect(bottomright=(800, 370))
        self.david_boss_lives_surf = font.render(f"Lives left: {self.lives}", False, (179, 223, 232))
        self.david_boss_lives_rect = self.david_boss_lives_surf.get_rect(center=(WIDTH / 2, 50))
        self.retreat = False
        self.charge_speed = 6

    def deth_of_the_boiled_one(self):
        global brake_before_attack, boss_fight_nr_list, game_mode_nr_list, obstacle_group, crouch
        brake_before_attack = False
        boss_fight_nr_list[0] = False
        game_mode_nr_list[0] = False
        game_mode_nr_list[1] = True
        game_mode_nr_unlocked_list[1] = True
        crouch = True

    def damage(self):
        global david_charge, timer, crouch
        if player.sprite.rect.left < self.david_boss_rect.right and player.sprite.rect.right > self.david_boss_rect.left \
                and player.sprite.rect.bottom <= self.david_boss_rect.top:
            if not self.retreat:
                self.david_boss_surf = pygame.transform.flip(self.david_boss_surf, True, False)
                self.lives -= 1
                self.charge_speed += 4
            self.retreat = True
            david_charge = False

        if self.lives <= 0:
            self.deth_of_the_boiled_one()
            obstacle_group.empty()
            crouch = True
            time = 0

    def player_kill(self):
        global david_charge
        if self.david_boss_rect.colliderect(player.sprite.rect):
            player_deth()
            self.lives = 3
            david_charge = False
            self.retreat = False
            self.david_boss_rect.bottomright = (800, 390)
            self.charge_speed = 6

    def display_and_update_score(self):
        self.david_boss_lives_surf = font.render(f"Lives left: {self.lives}", False, (179, 223, 232))
        screen.blit(self.david_boss_lives_surf, self.david_boss_lives_rect)

    def boss_movement(self):
        global david_charge
        if choice([True, False]):
            self.david_boss_rect.x -= 2
        else:
            self.david_boss_rect.x += 2

        if self.retreat:
            self.david_boss_rect.x += 25
            if self.david_boss_rect.right >= 800:
                self.david_boss_surf = pygame.transform.flip(self.david_boss_surf, True, False)
                self.david_boss_rect.right = 800
                self.retreat = False
                david_charge = False
        elif david_charge:
            self.david_boss_rect.x -= self.charge_speed

    def update(self):
        self.display_and_update_score()
        self.damage()
        self.player_kill()
        self.boss_movement()
        screen.blit(self.david_boss_surf, self.david_boss_rect)


class Boss2:
    def __init__(self):
        self.dimentions = (80, 120)
        thomas_boss_surf_blowing_1 = pygame.image.load("graphics/Fly/Thomas_flyge.png")
        thomas_boss_surf_blowing_2 = pygame.image.load("graphics/Fly/Thomas_flyge_2.png")
        thomas_boss_surf_blowing_1 = pygame.transform.rotozoom(thomas_boss_surf_blowing_1, -90, 1)
        thomas_boss_surf_blowing_2 = pygame.transform.rotozoom(thomas_boss_surf_blowing_2, -90, 1)
        thomas_boss_surf_blowing_1 = pygame.transform.scale(thomas_boss_surf_blowing_1, self.dimentions)
        thomas_boss_surf_blowing_2 = pygame.transform.scale(thomas_boss_surf_blowing_2, self.dimentions)
        self.thomas_blowing_surf_list = [thomas_boss_surf_blowing_1, thomas_boss_surf_blowing_2]

        thomas_approach_surf_1 = pygame.image.load("graphics/Fly/Thomas_flyge.png")
        thomas_approach_surf_2 = pygame.image.load("graphics/Fly/Thomas_flyge_2.png")
        thomas_approach_surf_3 = pygame.image.load("graphics/Fly/Thomas_flyge.png")
        thomas_approach_surf_4 = pygame.image.load("graphics/Fly/Thomas_flyge_2.png")
        thomas_approach_surf_5 = pygame.image.load("graphics/Fly/Thomas_flyge.png")
        thomas_approach_surf_6 = pygame.image.load("graphics/Fly/Thomas_flyge_2.png")

        self.dead_body = pygame.image.load("graphics/Player/evil_hans.png")
        self.dead_body = pygame.transform.scale(self.dead_body, (100, 140))
        self.dead_body_rect = self.dead_body.get_rect(bottomleft=(WIDTH, HEIGHT))

        self.surf_list = [thomas_approach_surf_1, thomas_approach_surf_2, thomas_approach_surf_3,
                          thomas_approach_surf_4, thomas_approach_surf_5, thomas_approach_surf_6]
        self.approach_index = 0
        self.surf = self.surf_list[self.approach_index]
        self.rect = self.surf.get_rect(bottomleft=(1250, 250))

        self.thomas_init_talking = False
        self.init = True
        self.thomas_attack_surf = pygame.image.load("graphics/Fly/Thomas_flyge.png")
        thomas_init_attack_1_surf = pygame.image.load("graphics/snail/david_krype_2.png")
        thomas_init_attack_2_surf = pygame.image.load("graphics/snail/david_krype1.png")
        self.init_attack_list = [thomas_init_attack_1_surf, thomas_init_attack_2_surf]
        self.break_before_attack_index = 0
        self.charge_surf = self.init_attack_list[0]
        self.charge_rect = self.charge_surf.get_rect(bottomright=(779, 250))
        self.y_velocity = 20

        self.lives = 3
        self.damage_disabled = False
        self.retreat = False
        self.retreat_index = 5
        self.talk_2_once = False
        self.talk_3_once = False
        self.talk_4_once = False
        self.once2 = False
        self.direction = []
        self.die = False

    def thomas_deth(self):
        global thomas_blow_count, double_jump, thomas_approaching
        obstacle_group.empty()
        thomas_blow_count = 0
        self.talk_2_once = False
        self.retreat_index = 5
        self.lives = 3
        double_jump = True
        game_mode_nr_unlocked_list[2] = True
        boss_fight_nr_list[1] = False
        game_mode_nr_list[1] = False
        game_mode_nr_list[2] = True

        thomas_approaching = True
        self.rect.bottomleft = (1250, 250)
        self.approach_index = 0
        self.lives = 3
        self.damage_disabled = False
        self.retreat = False
        self.retreat_index = 5
        self.talk_2_once = False
        self.once2 = False
        self.direction = []
        self.thomas_init_talking = False
        self.init = True
        self.y_velocity = 20
        self.talk_3_once = False
        self.talk_4_once = False


    def kill_player(self):
        global thomas_approaching, thomas_blow, thomas_blowing_attack, height_of_thomas_boss, thomas_charging, thomas_blow_count
        if player.sprite.rect.colliderect(self.rect) and not self.damage_disabled:
            player_deth()
            thomas_boss_music.fadeout(1000)
            thomas_approaching = True
            self.rect.bottomleft = (1250, 250)
            self.approach_index = 0
            self.lives = 3
            self.damage_disabled = False
            self.retreat = False
            self.retreat_index = 5
            self.talk_2_once = False
            self.talk_3_once = False
            self.talk_4_once = False
            self.once2 = False
            self.direction = []
            self.thomas_init_talking = False
            self.init = True
            self.thomas_init_talking = False
            self.y_velocity = 20
            thomas_blow = False
            thomas_blowing_attack = False
            height_of_thomas_boss = 220
            thomas_charging = False
            thomas_blow_count = 0


    def talking(self):
        if self.lives == 3:
            if pygame.mixer.Channel(0).get_busy():
                bg_music.fadeout(2000)
            elif not pygame.mixer.Channel(0).get_busy() and not self.thomas_init_talking and game_active:
                thomas_boss_talking.play()
                self.thomas_init_talking = True

        elif self.lives == 2:
            if pygame.mixer.Channel(0).get_busy():
                thomas_boss_music.fadeout(2000)
            if not self.talk_2_once:
                self.talk_2_once = True
                thomas_boss_talking_2.play()

        elif self.lives == 1:
            if pygame.mixer.Channel(0).get_busy() and not self.talk_3_once:
                thomas_boss_music.fadeout(2000)
            if not self.talk_3_once:
                self.talk_3_once = True
                thomas_boss_talking_3.play()
        elif self.lives == 0:
            if pygame.mixer.Channel(0).get_busy() and not self.talk_4_once:
                thomas_boss_music.fadeout(2000)
            if not self.talk_4_once:
                self.talk_4_once = True
                thomas_boss_talking_4.play()

    def animation(self):
        self.approach_index += 0.2
        if int(self.approach_index) >= len(self.surf_list): self.approach_index = 0
        self.surf = self.surf_list[int(self.approach_index)]


    def charge(self):
        global thomas_charging
        if thomas_charging:
            self.animation()
            if player_stunned:
                thomas_charging = False
            if self.rect.top < player.sprite.rect.centery:  # Am above
                if self.lives == 3 or self.lives == 1: self.y_velocity += 1
                elif self.lives == 2: self.y_velocity += 2
                self.rect.x -= 4
                self.rect.y += self.y_velocity
            elif self.rect.top >= player.sprite.rect.centery:  # Am below
                if self.y_velocity > 20:
                    self.y_velocity = 6
                if self.lives == 3 or self.lives == 1: self.y_velocity -= 1
                elif self.lives == 2: self.y_velocity -= 0.5
                self.rect.x -= 3
                self.rect.y += self.y_velocity

    def retreating(self):
        self.animation()
        if not self.rect.right > 920:
            self.rect.x += 10
            self.rect.y += self.retreat_index
            self.retreat_index -= 1
            self.surf = pygame.transform.flip(self.surf, True, False)
        else:
            self.rect.bottomright = (920, 250)
            self.retreat = False
            self.damage_disabled = False

    def approach_state(self):
        global thomas_blowing_attack, thomas_approaching, thomas_charging
        self.animation()
        self.talking()
        if self.rect.right > 940:
            self.rect.x -= 3
        elif not pygame.mixer.Channel(0).get_busy() or not self.init:
            self.init = False
            # When it arrives
            if not pygame.mixer.Channel(0).get_busy():
                thomas_boss_music.play(loops=-1)
            if int(self.break_before_attack_index) <= 1:
                self.break_before_attack_index += 0.02
                if int(self.break_before_attack_index) <= 1:
                    self.surf = self.init_attack_list[int(self.break_before_attack_index)]
            else:
                thomas_approaching = False
                thomas_charging = True

    def second_stage(self):
        global thomas_blowing_attack, thomas_charging
        if self.lives == 2:
            self.talking()
            self.animation()
            if player_stunned:
                if not self.once2:
                    self.once2 = True
                    thomas_killing_while_stunned.play()
            if not pygame.mixer.Channel(0).get_busy() and not player_stunned:
                if self.rect.left < 720:
                    self.rect.x += 5
                else:
                    self.rect.left = 720
                if self.rect.bottom < 400:
                    self.rect.y += 3
                else:
                    self.rect.bottom = 400
                if self.rect.bottomleft == (720, 400):
                    thomas_blowing_attack = True
                    thomas_boss_music.play()

    def third_stage(self):
        global thomas_charging, double_jump
        self.talking()
        self.animation()
        thomas_charging = True
        double_jump = True


    def no_life(self):
        self.dead_body_rect.y += 3
        self.rect.x += 3



    def damage(self):
        global thomas_charging
        if player.sprite.rect.left < self.rect.right and player.sprite.rect.right > self.rect.left \
                and player.sprite.rect.bottom <= self.rect.top and not self.damage_disabled:
            self.lives -= 1
            self.damage_disabled = True
            self.retreat = True
            thomas_charging = False
            if self.lives == 0:
                self.rect.topright = player.sprite.rect.bottomright
                self.dead_body_rect.topleft = player.sprite.rect.bottomleft
                self.surf = thomas_head_surf

    def blow_state(self, blow_height):
        global thomas_blowing_attack, thomas_charging
        self.rect.bottom = blow_height + 180
        self.rect.left = 720
        if player_stunned:
            thomas_boss_music.fadeout(1000)
            thomas_stunned_player.play()
            thomas_blowing_attack = False
        elif thomas_blow_count > 10:
            thomas_blowing_attack = False
            thomas_charging = True

        elif thomas_blow:
            self.surf = self.thomas_blowing_surf_list[0]
        else:
            self.surf = self.thomas_blowing_surf_list[1]


    def update(self, blow_height):
        self.damage()
        self.kill_player()
        if thomas_blowing_attack:
            self.blow_state(blow_height)
        elif thomas_approaching:
            self.approach_state()
        elif thomas_charging and not self.retreat:
            self.charge()
        elif self.retreat:
            self.retreating()
        elif self.lives == 2:
            self.second_stage()
            if player_stunned and not self.retreat:
                self.rect.x -= 2
                self.rect.bottom = 350
        elif self.lives == 1:
            self.third_stage()
        if self.lives <= 0:
            self.no_life()
            if self.die:
                self.thomas_deth()
            screen.blit(self.dead_body, self.dead_body_rect)

        screen.blit(self.surf, self.rect)


class Boss2Wind(pygame.sprite.Sprite):
    def __init__(self, height, width=750, from_player=False):
        super().__init__()
        wind_1 = pygame.image.load("graphics/effects/tornado/tornado_1.png")
        wind_2 = pygame.image.load("graphics/effects/tornado/tornado_2.png")
        wind_3 = pygame.image.load("graphics/effects/tornado/tornado_3.png")
        wind_4 = pygame.image.load("graphics/effects/tornado/tornado_4.png")
        wind_5 = pygame.image.load("graphics/effects/tornado/tornado_5.png")
        wind_6 = pygame.image.load("graphics/effects/tornado/tornado_6.png")
        wind_1 = pygame.transform.rotozoom(wind_1, 0, 1.6)
        wind_2 = pygame.transform.rotozoom(wind_2, 0, 1.6)
        wind_3 = pygame.transform.rotozoom(wind_3, 0, 1.6)
        wind_4 = pygame.transform.rotozoom(wind_4, 0, 1.6)
        wind_5 = pygame.transform.rotozoom(wind_5, 0, 1.6)
        wind_6 = pygame.transform.rotozoom(wind_6, 0, 1.6)

        self.from_player = from_player
        self.windex = 0
        self.wind_list = [wind_1, wind_2, wind_3, wind_4, wind_5, wind_6]
        self.image = wind_1
        self.rect = self.image.get_rect(bottomright=(width, height))
        self.wind_velocity = 5

    def animation_state(self):
        self.windex += 0.4
        if self.windex >= len(self.wind_list): self.windex = 0
        self.image = self.wind_list[int(self.windex)]

        if self.from_player:
            self.rect.y += 10
        else:
            self.wind_velocity += 0.1
            self.rect.x -= self.wind_velocity

    def destroy(self):
        if self.rect.right < 0 or self.rect.top > HEIGHT:
            self.kill()

    def update(self):
        self.animation_state()
        self.destroy()


pygame.init()

# Settings
WIDTH = 800
HEIGHT = 400
obstacle_speed = -4
gravity = 1
game_active = False
font = pygame.font.Font("font/Pixeltype.ttf", 50)
start_time = 0
timer = 0
score = 0
high_score = 0
celebration = False
game_over = False
obstacle_rect_list = []
david_dimension = (72, 31)
thomas_dimension = (84, 40)
counter = 0

# Player
player_dimension = (68, 84)
player_stunned = False

# Game modes
game_mode_nr_list = [True, False, False]
game_mode_nr_unlocked_list = [True, False, False]
boss_fight_nr_list = [False, False, False]

# Abilities
crouch = False
double_jump = False

disable_ability = False
allredy_double_jumped = False
do_double_jump = False

# Boss
#   David
david_charge = False
brake_before_attack = False
#   Thomas
thomas_blow = False
thomas_blowing_attack = False
thomas_approaching = True
height_of_thomas_boss = 220
thomas_charging = False
thomas_blow_count = 0

score_game_mode_2 = 0
score_game_mode_3 = 0
score_game_mode_4 = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

boss_1 = Boss1()

boss_2 = Boss2()

thomas_wind_group = pygame.sprite.Group()


def player_deth():
    global game_active, game_over, timer, celebration, boss_fight_nr_list, player_stunned, disable_ability
    obstacle_group.empty()
    thomas_wind_group.empty()
    game_active = False
    game_over = True
    boss_fight_nr_list = [False, False, False]
    player.sprite.rect.bottom = 300
    player.sprite.gravity = 0
    ground_rect.topleft = (0, 300)
    ground_2_rect.topleft = (800, 300)
    player_stunned = False
    disable_ability = False


    # hans_deth.play()


def display_score():
    if game_active:
        score_surf = font.render(f"{score}", False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(WIDTH / 2, 50))
        screen.blit(score_surf, score_rect)
    elif game_over:
        game_over_surf = font.render(f"Game over", False, (179, 223, 232))
        score_surf = font.render(f"Score: {score}", False, (179, 223, 232))
        game_over_rectangle = game_over_surf.get_rect(center=(WIDTH / 2, 50))
        score_rect = score_surf.get_rect(center=(WIDTH / 2, 350))
        screen.blit(game_over_surf, game_over_rectangle)
        screen.blit(score_surf, score_rect)
    elif not game_over:
        game_start_surf = font.render(f"Start", False, (179, 223, 232))
        pres_space_surf = font.render(f"Press Hans to start", False, (179, 223, 232))
        game_start_rectangle = game_start_surf.get_rect(center=(WIDTH / 2, 50))
        pres_space_rect = pres_space_surf.get_rect(center=(WIDTH / 2, 350))
        screen.blit(game_start_surf, game_start_rectangle)
        screen.blit(pres_space_surf, pres_space_rect)


def display_game_modes():
    global crouch, double_jump
    screen.blit(game_mode_1_text_surf, game_mode_1_text_rect)
    if game_mode_nr_unlocked_list[1]:
        crouch = True
        screen.blit(game_mode_2_text_surf, game_mode_2_text_rect)
    if game_mode_nr_unlocked_list[2]:
        crouch = True
        screen.blit(game_mode_2_text_surf, game_mode_2_text_rect)
        double_jump = True
        screen.blit(game_mode_3_text_surf, game_mode_3_text_rect)


def sprite_collisions():
    global game_active, game_over, timer, celebration, disable_ability, player_stunned, thomas_blowing_attack
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        player_deth()
        if timer == 0:
            timer = int((pygame.time.get_ticks() - start_time) / 1000)
        return False
    else:
        if pygame.sprite.spritecollide(player.sprite, thomas_wind_group, False) and boss_fight_nr_list[1]:
            disable_ability = True
            player_stunned = True
            thomas_blowing_attack = False
        return True


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thomas er best")
clock = pygame.time.Clock()

game_mode_1_text_surf = pygame.image.load("graphics/background/gamemode1.png")
game_mode_1_text_rect = game_mode_1_text_surf.get_rect(center=(600, 100))

game_mode_2_text_surf = pygame.image.load("graphics/background/gamemode2.png")
game_mode_2_text_rect = game_mode_2_text_surf.get_rect(center=(600, 150))

game_mode_3_text_surf = pygame.image.load("graphics/background/gamemode3.png")
game_mode_3_text_rect = game_mode_3_text_surf.get_rect(center=(600, 200))

star_background = pygame.image.load("graphics/background/himmel_og_fjell.jpg")
star_background = pygame.transform.scale(star_background, (1610, 970))
star_background = pygame.transform.rotozoom(star_background, 0, 0.5)

night_background = pygame.image.load("graphics/background/kvelds_himmel.jpg")
night_background = pygame.transform.scale(night_background, (1610, 970))
night_background = pygame.transform.rotozoom(night_background, 0, 0.5)

sky_surface = pygame.image.load("graphics/background/sol_og_himmel.jpg").convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))
ground_surface = pygame.image.load("graphics/background/bakken2.jpg").convert_alpha()
ground_surface = pygame.transform.scale(ground_surface, (800, 168))
ground_rect = ground_surface.get_rect(topleft=(0, 300))
ground_2_surface = pygame.image.load("graphics/background/bakken2.jpg").convert_alpha()
ground_2_surface = pygame.transform.scale(ground_2_surface, (800, 168))
ground_2_rect = ground_surface.get_rect(topleft=(800, 300))

player_stand_surf = pygame.image.load("graphics/player/evil_hans.png")
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 0.5)
player_stand_rect = player_stand_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))

player_start_surf = pygame.image.load("graphics/player/Midtskille_hans.png")
player_start_surf = pygame.transform.rotozoom(player_start_surf, 0, 0.5)
player_start_rect = player_stand_surf.get_rect(center=(WIDTH / 2 + 25, HEIGHT / 2 + 120))

thomas_head_surf = pygame.image.load("graphics/player/evil_hans.png")
player_head_rect = thomas_head_surf.get_rect(bottomleft=(WIDTH, HEIGHT))

# Music
# pygame.mixer.Channel(0)
bg_music = pygame.mixer.Sound("audio/sommarbelodi.mp3")
thomas_boss_talking = pygame.mixer.Sound("audio/hmmm.wav")
thomas_boss_music = pygame.mixer.Sound("audio/boss_battle/final_boss_battle_remake.wav")
thomas_boss_music.set_volume(0.5)
thomas_boss_talking_2 = pygame.mixer.Sound("audio/nei_ditta_vakje_snilt.mp3")
thomas_boss_talking_2.set_volume(2)
thomas_boss_talking_3 = pygame.mixer.Sound("audio/jump.mp3")
thomas_boss_talking_4 = pygame.mixer.Sound("audio/jump.mp3")
thomas_stunned_player = pygame.mixer.Sound("audio/jump.mp3")
thomas_stunned_player.set_volume(2)
thomas_killing_while_stunned = pygame.mixer.Sound("audio/du_skal_dø.mp3")
thomas_killing_while_stunned.set_volume(2)

# david_deth = best_game.mixer.Sound("audio/David_aooo.mp3")
# david_deth.set_volume(2)
# thomas_deth = best_game.mixer.Sound("audio/Thomas_nei_ikkje.mp3")
# thomas_deth.set_volume(2)
# hans_deth = best_game.mixer.Sound("audio/Hans_nei.mp3")
# hans_deth.set_volume(2)

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

boss_1_timer = pygame.USEREVENT + 2
pygame.time.set_timer(boss_1_timer, 5000)

thomas_wind_timer = pygame.USEREVENT + 3
pygame.time.set_timer(thomas_wind_timer, 250)

while True:
    for event in pygame.event.get():
        # Checking for inputs
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:

            if event.type == pygame.MOUSEBUTTONDOWN and player_stand_rect.collidepoint(pygame.mouse.get_pos()) or \
                    event.type == pygame.MOUSEBUTTONDOWN and game_mode_1_text_rect.collidepoint(
                pygame.mouse.get_pos()) or \
                    event.type == pygame.MOUSEBUTTONDOWN and game_mode_2_text_rect.collidepoint(
                pygame.mouse.get_pos()) or \
                    event.type == pygame.MOUSEBUTTONDOWN and game_mode_3_text_rect.collidepoint(pygame.mouse.get_pos()):

                bg_music.play(loops=-1)

                game_active = True
                timer = 0
                score = 0
                score_game_mode_2 = 0
                celebration = False
                start_time = pygame.time.get_ticks()

                if game_mode_1_text_rect.collidepoint(pygame.mouse.get_pos()):
                    game_mode_nr_list = [True, False, False]
                    boss_fight_nr_list = [False, False, False]
                    boss_1 = Boss1()
                    boss_2 = Boss2()
                elif game_mode_2_text_rect.collidepoint(pygame.mouse.get_pos()) and game_mode_nr_unlocked_list[1]:
                    game_mode_nr_list = [False, True, False]
                    boss_fight_nr_list = [True, False, False]
                    boss_1.deth_of_the_boiled_one()
                    boss_2 = Boss2()
                elif game_mode_3_text_rect.collidepoint(pygame.mouse.get_pos()) and game_mode_nr_unlocked_list[2]:
                    pass

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not allredy_double_jumped and player.sprite.rect.bottom < 300\
                        or event.key == pygame.K_UP and not allredy_double_jumped and player.sprite.rect.bottom < 300:
                    do_double_jump = True

            if event.type == obstacle_timer:
                obstacle_type = "david"
                if game_mode_nr_list[0]:
                    obstacle_type = "david"
                elif game_mode_nr_list[1]:
                    obstacle_type = choice(["thomas", "david"])
                obstacle_group.add(Obstacle(obstacle_type))

            if event.type == boss_1_timer:
                if boss_fight_nr_list[0] and brake_before_attack:
                    david_charge = True
                brake_before_attack = True

            if event.type == thomas_wind_timer:
                if boss_fight_nr_list[1]:
                    if thomas_blowing_attack:
                        counter += 0.5
                        if thomas_blow:
                            thomas_blow = False
                        elif thomas_blow_count <= 10:
                            thomas_blow_count += 1
                            thomas_blow = True
                            height_of_thomas_boss = choice([220, 350])
                            thomas_wind_group.add(Boss2Wind(height_of_thomas_boss))

    if game_active:
        # Checking if it should be a boss fight
        if score == 10 and game_mode_nr_list[0]:
            boss_fight_nr_list[0] = True
        elif game_mode_nr_list[1]:
            if score_game_mode_2 == 10 or score_game_mode_2 == 11:
                boss_fight_nr_list[1] = True

        screen.blit(sky_surface, (0, 0))

        # Moving ground
        ground_rect.x -= 2
        ground_2_rect.x -= 2
        if ground_rect.right <= 0:
            ground_rect.topleft = (800, 300)
        elif ground_2_rect.right <= 0:
            ground_2_rect.topleft = (800, 300)
        screen.blit(ground_surface, ground_rect)
        screen.blit(ground_2_surface, ground_2_rect)

        if not boss_fight_nr_list[0] and not boss_fight_nr_list[1] and not boss_fight_nr_list[2]:
            display_score()

            if obstacle_speed < 8:
                obstacle_speed -= 0.001
            timer = int((pygame.time.get_ticks() - start_time) / 1000)

            game_active = sprite_collisions()
            game_over = sprite_collisions()

            obstacle_group.draw(screen)
            obstacle_group.update()

        else:
            if boss_fight_nr_list[0]:
                boss_1.update()

            if boss_fight_nr_list[1]:
                boss_2.update(height_of_thomas_boss)
                sprite_collisions()

        thomas_wind_group.draw(screen)
        thomas_wind_group.update()
        player.draw(screen)
        player.update()

    else:
        if game_over:
            obstacle_speed = -4
            screen.blit(night_background, (0, 0))

            # Celebration screen
            if celebration:
                print("yayyy")
            screen.blit(player_stand_surf, player_stand_rect)

            # Game_modes
            display_game_modes()

            bg_music.fadeout(600)
        else:
            screen.blit(star_background, (0, 0))
            screen.blit(player_start_surf, player_start_rect)

        display_score()

    pygame.display.update()
    # Makes fastest possible frame rate 60 fps
    clock.tick(60)
