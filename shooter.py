#!/usr/bin/env python3

import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75

#background color
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg(bg):
    screen.fill(bg)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        # object attributes
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # load all player images
        animation_types = ["Idle", "Run", "Jump"]
        for animation in animation_types:
            # reset temp_list of images
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                #get player image with relative path
                player_img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png")
                player_img = pygame.transform.scale(player_img, (int(player_img.get_width() * scale), int(player_img.get_height() * scale)))
                temp_list.append(player_img)
            self.animation_list.append(temp_list)

        self.player_image = self.animation_list[self.action][self.frame_index]
        self.player_rect = self.player_image.get_rect()
        self.player_rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0
        #assign movement variable if moving
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY

        #gravity limit
        if self.vel_y > 10:
            self.vel_y
        #jump velocity
        dy += self.vel_y

        #check collision with floor
        if self.player_rect.bottom + dy > 300:
            dy = 300 - self.player_rect.bottom
            self.in_air = False

        #update player_rect
        self.player_rect.x += dx
        self.player_rect.y += dy
    
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update player frame
        self.player_image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #reset animation loop
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            
    def update_action(self, new_action):
        # check action state and update
        if new_action != self.action:
            self.action = new_action
            #update animation parameters
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.player_image, self.flip, False), self.player_rect)


player = Soldier(char_type="player", x=200, y=200, scale=3, speed=5)
enemy0 = Soldier(char_type="enemy", x=400, y=200, scale=3, speed=5)


# player action variables
moving_left = False
moving_right = False

run = True
while run:

    clock.tick(FPS)
    draw_bg(BG)
    player.update_animation()
    enemy0.update_animation()
    player.draw()
    enemy0.draw()
    if player.alive:
        if player.in_air:
            player.update_action(2) # action 2 is jump
        # update player actions
        elif moving_left or moving_right:
            player.update_action(1) # action 1 is run
        else:
            player.update_action(0) # action 0 is idle
        player.move(moving_left=moving_left, moving_right=moving_right)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            # game exit key
            if event.key == pygame.K_ESCAPE:
                run = False
        #keyboard press release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
        

    pygame.display.update()

pygame.quit()