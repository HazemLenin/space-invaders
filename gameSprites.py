import pygame, sys
from spriteSheet import SpriteSheet

sprite_sheet = SpriteSheet('./assets/images/New Piskel.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health, vel, score):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frames = (
            sprite_sheet.parse_sprite('New Piskel4.png'),
            sprite_sheet.parse_sprite('New Piskel7.png')
        )
        self.frames_index = 0
        self.image = pygame.transform.scale(
            self.frames[self.frames_index],
            (self.width, self.height)
        )
        self.health = health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = vel
        self.ready = True
        self.score = score

    def update(self):
        if self.health <= 1:
            self.frames_index = 1
            self.image = pygame.transform.scale(
                self.frames[self.frames_index],
                (self.width, self.height)
            )
        if self.health <= 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 2
        self.height = 30
        self.vel = 30
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((0, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frames = (
            (
                sprite_sheet.parse_sprite('New Piskel0.png'),
                sprite_sheet.parse_sprite('New Piskel1.png')
            ),
            (
                sprite_sheet.parse_sprite('New Piskel2.png'),
                sprite_sheet.parse_sprite('New Piskel3.png')
            )
        )
        self.frames_index = 0
        self.healthy_index = 0
        self.image = pygame.transform.scale(
            self.frames[0][self.frames_index],
            (self.width, self.height)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 2

        self.steps_default = 140
        self.steps = 140
        self.vel = 5

    def hit(self):
        self.health -= 1

    def change_img(self):
        self.frames_index += 1
        self.frames_index %= len(self.frames)
        self.image = pygame.transform.scale(
            self.frames[self.healthy_index][self.frames_index],
            (self.width, self.height)
        )

    def update(self):
        if self.health <= 1:
            self.healthy_index = 1
            self.image = pygame.transform.scale(
                self.frames[self.healthy_index][self.frames_index],
                (self.width, self.height)
            )

        if self.health <= 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vel):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.image = pygame.Surface((width, height))

        self.image.fill((255, 255, 0))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
