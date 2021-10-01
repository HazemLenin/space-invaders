import pygame, sys


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vel, score):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.blit(
            pygame.transform.scale(
                pygame.image.load(sys.path[0] + r'\assets\images\spaceship.png'),
                (self.width, self.height)
            ),
            (0, 0)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = vel
        # self.shoot_timer_default = 10
        # self.shoot_timer = 10
        self.ready = True
        self.score = score


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


def alien_img(width=60, height=60, red=False):
    return pygame.transform.scale(
        pygame.image.load(sys.path[0] + rf'\assets\images\alien_{"red" if red else "green"}.png'),
        (width, height)
    )


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health, vel):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.blit(
            alien_img(self.width, self.height),
            (0, 0)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = health
        self.direction_before = 'DOWN'
        self.direction = 'RIGHT'
        self.steps_default = 140
        self.steps = 140
        self.vel = vel

    def hit(self):
        self.health -= 1

    def move(self):
        if self.steps <= 0:
            # if self.direction == 'RIGHT':
            #     self.direction = 'DOWN'
            #     self.steps_default = 45
            #     self.direction_before = 'RIGHT'
            # elif self.direction == 'LEFT':
            #     self.direction = 'DOWN'
            #     self.direction_before = 'LEFT'
            #     self.steps_default = 45
            if self.direction in ['RIGHT', 'LEFT']:
                self.direction_before = self.direction
                self.direction = 'DOWN'
                self.steps_default = 45
            elif self.direction == 'DOWN':
                if self.direction_before == 'RIGHT':
                    self.direction = 'LEFT'
                elif self.direction_before == 'LEFT':
                    self.direction = 'RIGHT'
                self.steps_default = 140
            self.steps = self.steps_default
        else:
            if self.direction == 'RIGHT':
                self.rect.x += self.vel
            elif self.direction == 'LEFT':
                self.rect.x -= self.vel
            elif self.direction == 'DOWN':
                self.rect.y += self.vel
            self.steps -= self.vel

    def update(self):
        if self.health == 1:
            self.image.blit(alien_img(self.width, self.height, True), (0, 0))

        if self.health <= 0:
            self.kill()
