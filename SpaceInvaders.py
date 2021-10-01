# importing libraries
import pygame
import random
import tkinter
import sys

from gameSprites import Player, Bullet, Enemy

# setup tkinter to get screen info
root = tkinter.Tk()

# initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
"""
channel 0: main theme/fx (hit/boom)
channel 1: change selection/select/alien movement
channel 2: win/lose music
"""

# setup clock
clock = pygame.time.Clock()

# get screen size
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()

# setup window
win = pygame.display.set_mode((scr_width, scr_height), pygame.FULLSCREEN)

pygame.display.set_caption('Space Invaders')

# define colors
WHITE = (255, 255, 255)
LIGHT_GREY = (192, 192, 192)
DARK_GREY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# fade to show main menu
# def fade_intro(width, height):
#     fade = pygame.Surface((width, height))
#     fade.fill(BLACK)
#
#     for alpha in range(0, 10):
#         fade.set_alpha(alpha * 28)
#         render_intro()
#         win.blit(fade, (0, 0))
#         pygame.display.update()
#         clock.tick(20)
#
#
# def fade_window(width, height):
#     fade = pygame.Surface((width, height))
#     fade.fill(BLACK)
#
#     for alpha in range(-10, 0):
#         fade.set_alpha(-(alpha * 28))
#         renderWindow()
#         win.blit(fade, (0, 0))
#         pygame.display.update()
#         clock.tick(20)


star_field = []  # to store stars positions

# start stars with random positions
for stars in range(50):
    star_loc_x = random.randrange(0, scr_width)
    star_loc_y = random.randrange(0, scr_height)
    star_field.append([star_loc_x, star_loc_y])


def render_stars():
    global star_field

    for star in star_field:
        star[1] += 1
        if star[1] > scr_height:
            star[0] = random.randrange(0, scr_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.rect(win, WHITE, (star[0], star[1], 5, 5))


def render_home():
    index = 0
    choices = ['start', 'quit']

    title_font = pygame.font.Font(sys.path[0] + r'\assets\fonts\slkscr.ttf', 70)
    selection_font = pygame.font.Font(sys.path[0] + r'\assets\fonts\slkscr.ttf', 50)
    title = title_font.render('Space Invaders', True, WHITE)

    start_text = selection_font.render('> START', True, WHITE)
    quit_text = selection_font.render('QUIT', True, WHITE)

    change_selection_sound = pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\change_selection.wav')
    select_sound = pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\select.wav')

    while True:

        dt = clock.tick(30) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    pygame.mixer.Channel(1).play(change_selection_sound)
                    if event.key == pygame.K_UP:
                        # if selection_y == 600:
                        #     selection_y = 500
                        #     intro_state = 'start'
                        # else:
                        #     selection_y = 600
                        #     intro_state = 'quit'
                        index -= 1

                    if event.key == pygame.K_DOWN:
                        # if selection_y == 600:
                        #     selection_y = 500
                        #     intro_state = 'start'
                        #
                        # else:
                        #     selection_y = 600
                        #     intro_state = 'quit'
                        index += 1

                    index %= len(choices)
                    start_text = selection_font.render('START', True, WHITE)
                    quit_text = selection_font.render('QUIT', True, WHITE)

                    if index == 0:
                        start_text = selection_font.render('> START', True, WHITE)

                    elif index == 1:
                        quit_text = selection_font.render('> QUIT', True, WHITE)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            break

        if keys[pygame.K_RETURN]:
            pygame.mixer.Channel(1).play(select_sound)
            if choices[index] == 'start':
                # fade_intro(scr_width, scr_height)
                break

            elif choices[index] == 'quit':
                pygame.quit()
                sys.exit()
                break

        win.fill(BLACK)
        render_stars()

        win.blit(title, (((scr_width // 2) - (title.get_width() // 2)), 130))
        win.blit(start_text, (636, 500))
        win.blit(quit_text, (636, 600))

        pygame.display.update()


# fade_window(scr_width, scr_height)

def render_pause():
    pause_font = pygame.font.Font(sys.path[0] + r'\assets\fonts\slkscr.ttf', 50)
    pause_text = pause_font.render('PAUSED', True, WHITE)
    continue_text = pause_font.render('PRESS P TO CONTINUE', True, WHITE)
    quit_text = pause_font.render('PRESS ESC TO quit', True, WHITE)
    win.blit(pause_text, (
        ((scr_width // 2) - (pause_text.get_width() // 2)),
        ((scr_height // 2) - (pause_text.get_height() // 2)),
    ))
    win.blit(continue_text, (
        ((scr_width // 2) - (continue_text.get_width() // 2)),
        ((scr_height // 2) - (continue_text.get_height() // 2) + 50),
    ))
    win.blit(quit_text, (
        ((scr_width // 2) - (quit_text.get_width() // 2)),
        ((scr_height // 2) - (quit_text.get_height() // 2) + 100),
    ))
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    break
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            break

        pygame.display.update()


def render_main_game():
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    players = pygame.sprite.Group()

    enemy_delay_default = 4
    enemy_delay = 2

    player = Player(
        x=(scr_width // 2) - 45,
        y=800,
        width=90,
        height=90,
        vel=5,
        score=0
    )
    player.add(players)

    # rows, cols = 2, 4
    rows, cols = 6, 14

    x, y = 20, 40

    for i in range(rows):

        for j in range(cols):
            Enemy(
                x=x,
                y=y,
                width=60,
                height=60,
                health=3,
                vel=5
            ).add(enemies)

            x += 80

        y += 80
        x = 20

    bullet = Bullet(
        x=player.rect.x + (player.rect.width // 2) - 4,
        y=player.rect.y,
    )

    bullet.add(bullets)

    score_font = pygame.font.Font(sys.path[0] + r'\assets\fonts\slkscr.ttf', 40)

    boom_sound = pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\boom.wav')
    hit_sound = pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\hit.wav')

    move_index = 0
    move_sound = (
        pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\move1.wav'),
        pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\move2.wav')
    )

    while True:
        dt = clock.tick(30) / 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    render_pause()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.rect.x > player.vel:
            player.rect.x -= player.vel
        if keys[pygame.K_RIGHT] and player.rect.x < scr_width - player.rect.width - player.vel:
            player.rect.x += player.vel

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            break

        enemy_delay -= dt

        if keys[pygame.K_SPACE] and player.ready:
            bullet.rect.x = player.rect.x + (player.rect.width // 2) - (bullet.rect.width // 2)
            bullet.rect.y = player.rect.y
            player.ready = False

        win.fill(BLACK)
        render_stars()

        players.update()
        players.draw(win)

        for bullet in bullets.sprites():

            if not player.ready:
                bullet.rect.y -= bullet.vel

            if bullet.rect.y <= 0 - bullet.rect.height:
                player.ready = True
                bullet.rect.y = player.rect.y

        bullets.update()
        if not player.ready:
            bullets.draw(win)

        for enemy in enemies.sprites():

            if enemy_delay <= 0:
                enemy.move()

            if bullet.rect.colliderect(enemy.rect) and not player.ready:
                player.ready = True
                bullet.rect.y = player.rect.y
                enemy.hit()
                enemies.update()
                if enemy.alive():
                    pygame.mixer.Channel(0).play(hit_sound)
                else:
                    pygame.mixer.Channel(0).play(boom_sound)

                player.score += 50

            if player.rect.colliderect(enemy.rect):
                player.kill()

        enemies.draw(win)

        if len(enemies.sprites()) <= 0:
            render_win()
            break

        if len(players.sprites()) <= 0:
            render_game_over()
            break

        if enemy_delay <= 0:
            enemy_delay = enemy_delay_default
            pygame.mixer.Channel(1).play(move_sound[move_index])
            move_index += 1
            move_index %= len(move_sound)

        win.blit(score_font.render(f'score: {player.score}', True, WHITE), (0, 0))

        pygame.display.update()


def render_win():
    global star_field

    win_font = pygame.font.Font(sys.path[0] + r'\assets\fonts\slkscr.ttf', 40)
    win_text = win_font.render('YOU WIN!!!', True, WHITE)
    win.blit(win_text, (
        ((scr_width // 2) - (win_text.get_width() // 2)),
        ((scr_height // 2) - (win_text.get_height() // 2)),
    ))

    win_sound = pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\win.wav')
    pygame.mixer.Channel(2).play(win_sound)

    while True:
        dt = clock.tick(30) / 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            break

        pygame.display.update()


def render_game_over():
    global star_field

    lose_font = pygame.font.Font(sys.path[0] + r'\assets\fonts\slkscr.ttf', 40)
    lose_text = lose_font.render('YOU LOST!', True, WHITE)
    play_again_text = lose_font.render('PLAY AGAIN?(ENTER/RETURN)', True, WHITE)
    exit_text = lose_font.render('QUIT?', True, WHITE)
    win.blit(lose_text, (
        ((scr_width // 2) - (lose_text.get_width() // 2)),
        ((scr_height // 2) - (lose_text.get_height() // 2)),
    ))
    win.blit(lose_text, (
        ((scr_width // 2) - (play_again_text.get_width() // 2)),
        ((scr_height // 2) - (play_again_text.get_height() // 2) + 30),
    ))

    lose_sound = pygame.mixer.Sound(sys.path[0] + r'\assets\sounds\lose.wav')
    pygame.mixer.Channel(2).play(lose_sound)

    while True:
        dt = clock.tick(30) / 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            break

        pygame.display.update()


if __name__ == '__main__':
    render_home()
    render_main_game()
