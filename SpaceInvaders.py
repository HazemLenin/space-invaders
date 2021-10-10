# importing libraries
import pygame, random, sys

# initialize pygame
pygame.init()
pygame.display.init()
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
scr_width, scr_height = pygame.display.get_desktop_sizes()[0]

# setup window
win = pygame.display.set_mode((scr_width, scr_height), pygame.FULLSCREEN)

pygame.display.set_caption('Space Invaders')

icon = pygame.image.load(r'.\assets\images\New Piskel-5.png')
pygame.display.set_icon(icon)

from gameSprites import Player, Bullet, Enemy, EnemyBullet

# define colors
WHITE = (255, 255, 255)
LIGHT_GREY = (192, 192, 192)
DARK_GREY = (128, 128, 128)
BLACK = (0, 0, 0)

jumps_to_255 = 60
sleep_between_jumps = 70


def fade_in(render_func):
    fade_surface = pygame.Surface((scr_width, scr_height))
    fade_surface.fill(BLACK)
    for alpha in range(-255, 0, jumps_to_255):
        fade_surface.set_alpha(-alpha)
        render_func()
        win.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(sleep_between_jumps)


def fade_out(render_func):
    fade_surface = pygame.Surface((scr_width, scr_height))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, jumps_to_255):
        fade_surface.set_alpha(alpha)
        render_func()
        win.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(sleep_between_jumps)


def intro():
    font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 70)
    text = font.render('HAZEM LENIN', True, WHITE)

    def render_intro():
        win.blit(text, (
            ((scr_width // 2) - (text.get_width() // 2)),
            ((scr_height // 2) - (text.get_height() // 2)),
        ))

    intro_image = pygame.image.load(r'.\assets\images\space-invaders.jpg')

    width = scr_width * 0.9
    height = width * intro_image.get_height() / intro_image.get_width()

    # width = width * (scr_height * 0.8) / height  # reduce width to keep ratio
    # height = scr_height * 0.8  # max height

    intro_image = pygame.transform.scale(
        intro_image,
        (
            int(width),
            int(height)
        )
    )

    def render_intro_image():
        win.blit(intro_image, (
            (scr_width//2) - (intro_image.get_width()//2), 0
        ))

    fade_in(render_intro)
    pygame.time.delay(2000)
    fade_out(render_intro)

    fade_in(render_intro_image)
    pygame.time.delay(2000)
    fade_out(render_intro_image)

    home()

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


def home():
    index = 0
    choices = ['START', 'QUIT']

    title_font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 70)
    selection_font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 50)
    title = title_font.render('SPACE INVADERS', True, WHITE)

    start_text = selection_font.render('> START', True, WHITE)
    quit_text = selection_font.render('QUIT', True, WHITE)

    change_selection_sound = pygame.mixer.Sound(r'.\assets\sounds\change_selection.wav')
    select_sound = pygame.mixer.Sound(r'.\assets\sounds\select.wav')

    def render_home():
        win.fill(BLACK)
        render_stars()
        win.blit(title, (((scr_width // 2) - (title.get_width() // 2)), 130))
        win.blit(start_text, (636, 500))
        win.blit(quit_text, (636, 600))

    fade_in(render_home)

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
                        index -= 1

                    if event.key == pygame.K_DOWN:
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
            if choices[index] == 'START':
                fade_out(render_home)
                main_game()
                break

            elif choices[index] == 'QUIT':
                pygame.quit()
                sys.exit()
                break

        render_home()

        pygame.display.update()


def pause():
    font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 50)
    pause_text = font.render('PAUSED', True, WHITE)
    continue_text = font.render('PRESS P TO CONTINUE', True, WHITE)
    restart_text = font.render('PRESS R TO RESTART', True, WHITE)
    quit_text = font.render('PRESS ESC TO quit', True, WHITE)
    home_text = font.render('PRESS H TO GO HOME', True, WHITE)

    def render_pause():
        win.blit(pause_text, (
            ((scr_width // 2) - (pause_text.get_width() // 2)),
            ((scr_height // 2) - (pause_text.get_height() // 2)),
        ))
        win.blit(restart_text, (
            ((scr_width // 2) - (restart_text.get_width() // 2)),
            ((scr_height // 2) - (restart_text.get_height() // 2) + 50)
        ))
        win.blit(continue_text, (
            ((scr_width // 2) - (continue_text.get_width() // 2)),
            ((scr_height // 2) - (continue_text.get_height() // 2) + 100),
        ))
        win.blit(quit_text, (
            ((scr_width // 2) - (quit_text.get_width() // 2)),
            ((scr_height // 2) - (quit_text.get_height() // 2) + 150),
        ))
        win.blit(home_text, (
            ((scr_width // 2) - (home_text.get_width() // 2)),
            ((scr_height // 2) - (home_text.get_height() // 2) + 200)
        ))

    render_pause()

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
                if event.key == pygame.K_r:
                    fade_out(render_pause)
                    main_game()
                    break
                if event.key == pygame.K_h:
                    fade_out(render_pause)
                    home()
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    break

        pygame.display.update()


def main_game():
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    players = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    enemy_delay = enemy_delay_default = .6
    bullet_delay = bullet_delay_default = .7

    player = Player(
        x=(scr_width // 2) - 45,
        y=800,
        width=90,
        height=90,
        health=4,
        vel=10,
        score=0
    )
    player.add(players)

    enemies_direction = enemies_last_direction = 'RIGHT'

    rows, cols = 6, 12

    x = y = 200

    for i in range(rows):

        for j in range(cols):
            Enemy(
                x=x,
                y=y,
                width=60,
                height=60,
            ).add(enemies)

            x += 75

        y += 45
        x = 200

    bullet = Bullet(
        x=player.rect.x + (player.rect.width // 2) - 4,
        y=player.rect.y,
    )

    bullet.add(bullets)

    font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 40)

    boom_sound = pygame.mixer.Sound(r'.\assets\sounds\boom.wav')
    hit_sound = pygame.mixer.Sound(r'.\assets\sounds\hit.wav')

    move_index = 0
    move_sound = (
        pygame.mixer.Sound(r'.\assets\sounds\move1.wav'),
        pygame.mixer.Sound(r'.\assets\sounds\move2.wav')
    )

    def render_main_game():
        players.update()
        bullets.update()
        enemies.update()
        enemy_bullets.update()

        win.fill(BLACK)
        render_stars()
        players.draw(win)
        enemy_bullets.draw(win)
        enemies.draw(win)
        if not player.ready: bullets.draw(win)

        win.blit(font.render(f'score: {player.score:0>5d}', True, WHITE), (0, 0))
        win.blit(font.render(f'FPS: {clock.get_fps():.2f}', True, WHITE), (0, 30))

    fade_in(render_main_game)

    def move_aliens():
        nonlocal enemies_direction
        for enemy in enemies.sprites():
            if enemies_direction == 'RIGHT':
                enemy.rect.x += enemy.vel
            elif enemies_direction == 'LEFT':
                enemy.rect.x -= enemy.vel
            elif enemies_direction == 'DOWN':
                enemy.rect.y += enemy.height

            enemy.change_img()

        if enemies_direction == 'DOWN':
            enemies_direction = 'RIGHT' if enemies_last_direction == 'LEFT' else 'LEFT'

    def shoot():
        enemy = random.choice(enemies.sprites())
        EnemyBullet(
            x=enemy.rect.centerx,
            y=enemy.rect.bottom,
            width=5,
            height=15,
            vel=20
        ).add(enemy_bullets)

    while True:
        dt = clock.tick(30) / 1000

        enemy_delay -= dt
        bullet_delay -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    break

                if event.key == pygame.K_w:
                    fade_out(render_main_game)
                    win_game(font, player.score)
                    break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.rect.x > player.vel:
            player.rect.x -= player.vel
        if keys[pygame.K_RIGHT] and player.rect.x < scr_width - player.rect.width - player.vel:
            player.rect.x += player.vel


        if keys[pygame.K_SPACE] and player.ready:
            bullet.rect.centerx, bullet.rect.y = player.rect.centerx, player.rect.y
            player.ready = False

        for bullet in bullets.sprites():

            if not player.ready:
                bullet.rect.y -= bullet.vel

            if bullet.rect.y <= 0 - bullet.rect.height:
                player.ready = True
                bullet.rect.y = player.rect.y

        for enemy in enemies.sprites():

            if bullet.rect.colliderect(enemy.rect) and not player.ready:
                player.ready = True
                bullet.rect.y = player.rect.y
                enemy.hit()
                # enemy.health = 0

                pygame.mixer.Channel(0).play(boom_sound) if enemy.health == 0 else pygame.mixer.Channel(0).play(hit_sound)

                player.score += 50

            if player.rect.colliderect(enemy.rect):
                player.health = 0

        if enemy_delay <= 0:
            for enemy in enemies.sprites():
                if (enemies_direction == 'LEFT' and (enemy.rect.x - enemy.vel) <= 0) or \
                        (enemies_direction == 'RIGHT' and (enemy.rect.right + enemy.vel) >= scr_width):
                    enemies_last_direction = enemies_direction
                    enemies_direction = 'DOWN'

                    move_aliens()
                    break
            move_aliens()

            enemy_delay = enemy_delay_default
            pygame.mixer.Channel(1).play(move_sound[move_index])
            move_index += 1
            move_index %= len(move_sound)

        for enemy_bullet in enemy_bullets.sprites():
            if enemy_bullet.rect.y < scr_height - enemy_bullet.vel:
                enemy_bullet.rect.y += enemy_bullet.vel

            else:
                enemy_bullet.kill()

            if player.rect.colliderect(enemy_bullet):
                player.health = 0

        if bullet_delay <= 0:
            shoot()
            bullet_delay = bullet_delay_default

        if len(enemies.sprites()) <= 0:
            fade_out(render_main_game)
            win_game(font, player.score)
            break

        if len(players.sprites()) <= 0:
            fade_out(render_main_game)
            lose_game(font, player.score)
            break

        render_main_game()

        pygame.display.update()


def win_game(score_font, score):
    global star_field

    font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 40)
    win_text = font.render('YOU WIN!!!', True, WHITE)
    restart_text = font.render('PRESS R TO RESTART', True, WHITE)
    quit_text = font.render('PRESS ESC TO QUIT', True, WHITE)
    home_text = font.render('PRESS H TO GO HOME', True, WHITE)

    win_sound = pygame.mixer.Sound(r'.\assets\sounds\win.wav')
    pygame.mixer.Channel(2).play(win_sound)

    def render_win_game():
        win.blit(score_font.render(f'score: {score:0>5d}', True, WHITE), (0, 0))
        win.blit(win_text, (
            ((scr_width // 2) - (win_text.get_width() // 2)),
            ((scr_height // 2) - (win_text.get_height() // 2)),
        ))
        win.blit(restart_text, (
            ((scr_width // 2) - (restart_text.get_width() // 2)),
            ((scr_height // 2) - (restart_text.get_height() // 2) + 50),
        ))
        win.blit(home_text, (
            ((scr_width // 2) - (home_text.get_width() // 2)),
            ((scr_height // 2) - (home_text.get_height() // 2) + 150))
                 )
        win.blit(quit_text, (
            ((scr_width // 2) - (quit_text.get_width() // 2)),
            ((scr_height // 2) - (quit_text.get_height() // 2) + 100),
        ))

    render_win_game()

    while True:
        dt = clock.tick(30) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    fade_out(render_win_game)
                    main_game()
                    break

                if event.key == pygame.K_h:
                    fade_out(render_win_game)
                    home()
                    break

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    break

        pygame.display.update()


def lose_game(score_font, score):
    global star_field

    font = pygame.font.Font(r'.\assets\fonts\slkscr.ttf', 40)
    lose_text = font.render('YOU LOST!', True, WHITE)
    play_again_text = font.render('PRESS R TO RESTART', True, WHITE)
    quit_text = font.render('PRESS ESC TO QUIT', True, WHITE)
    home_text = font.render('PRESS H TO GO HOME', True, WHITE)

    lose_sound = pygame.mixer.Sound(r'.\assets\sounds\lose.wav')
    pygame.mixer.Channel(2).play(lose_sound)

    def render_lose_game():
        win.blit(score_font.render(f'score: {score:0>5d}', True, WHITE), (0, 0))
        win.blit(lose_text, (
            ((scr_width // 2) - (lose_text.get_width() // 2)),
            ((scr_height // 2) - (lose_text.get_height() // 2)),
        ))
        win.blit(play_again_text, (
            ((scr_width // 2) - (play_again_text.get_width() // 2)),
            ((scr_height // 2) - (play_again_text.get_height() // 2) + 50),
        ))
        win.blit(quit_text, (
            ((scr_width // 2) - (quit_text.get_width() // 2)),
            ((scr_height // 2) - (quit_text.get_height() // 2) + 100),
        ))
        win.blit(home_text, (
            ((scr_width // 2) - (home_text.get_width() // 2)),
            ((scr_height // 2) - (home_text.get_height() // 2) + 150)
        ))

    render_lose_game()

    while True:
        dt = clock.tick(30) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    fade_out(render_lose_game)
                    main_game()
                    break

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    break

                if event.key == pygame.K_h:
                    fade_out(render_lose_game)
                    home()
                    break

        pygame.display.update()


if __name__ == '__main__':
    intro()
