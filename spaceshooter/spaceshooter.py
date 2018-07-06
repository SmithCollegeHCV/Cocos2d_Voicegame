import pygame
import sys
import random
import pyaudio
import aubio
import numpy as np

#Audio initialization
CHUNK = 1024
RATE = 44100
voice = pyaudio.PyAudio()
stream = voice.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
voiceDetection = aubio.pitch("default", CHUNK*2, CHUNK, RATE)
voiceDetection.set_unit("Hz")
voiceDetection.set_silence(-40)

#Constants definition
WIDTH = 540
HEIGHT = 720

#Initialize the game
pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#Initialize menu
def main_menu():
    global screen
    menu_song = pygame.mixer.music.load("sounds/menu.mp3")

class Sprite:
    pass

def display_sprite(sprite):
    window.blit(sprite.image, (sprite.x, sprite.y))

def fire_bullet():
    bullet = Sprite()
    bullet.x = ship.x + 20
    bullet.y = ship.y - 10
    bullet.image = bullet_image
    bullet.used = False
    bullets.append(bullet)

def add_alien():
    alien = Sprite()
    alien.x = random.randrange(0, window.get_width()-alien_image.get_width())
    alien.y = 10
    alien.image = alien_image
    alien.hit = False
    alien.alpha = 255
    aliens.append(alien)

def add_rock():
    rock = Sprite()
    rock.x = random.randrange(0, window.get_width()-rock_image.get_width())
    rock.y = 10
    rock.image = rock_image
    rock.hit = False
    rock.alpha = 255
    rocks.append(rock)

def add_star():
    star = Sprite()
    star_size = random.randrange(1,4)
    star.x = random.randrange(0, window.get_width())
    star.y = 10
    star.image = pygame.Surface((star_size,star_size))
    star.image.fill((255,255,255))
    stars.append(star)

def get_sprite_rectangle(sprite):
    return sprite.image.get_rect().move(sprite.x, sprite.y)

#Creating score bar
font = pygame.font.Font(None,24)
foreground = (200,200,200)
#Creating the background
background = (0,0,0)
#Creating the spaceship
ship_image = pygame.image.load("assets2/spaceship.png")
ship_image = pygame.transform.scale(ship_image, (int(ship_image.get_width()*0.1), int(ship_image.get_height()*0.1)))
#ship_image = pygame.transform.scale(ship_image, (70, 70))
#Creating the bullet
bullet_image = pygame.image.load("assets2/bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (int(bullet_image.get_width()*0.02), int(bullet_image.get_height()*0.02)))
#bullet_image = pygame.transform.scale(bullet_image, (20, 40))
#Creating aliens
alien_image = pygame.image.load("assets2/alien.png")
alien_image = pygame.transform.scale(alien_image, (int(alien_image.get_width()*0.02), int(alien_image.get_height()*0.02)))
#alien_image = pygame.transform.scale(alien_image, (70, 70))
rock_image = pygame.image.load("assets2/rock.png")
rock_image = pygame.transform.scale(rock_image, (int(rock_image.get_width()*0.1), int(rock_image.get_height()*0.1)))
rock_broken_image = pygame.image.load("assets2/rock-broken.png")
rock_broken_image = pygame.transform.scale(rock_broken_image, (int(rock_broken_image.get_width()*0.08), int(rock_broken_image.get_height()*0.08)))
rocks = []
frames_until_next_rock = random.randrange(30, 100)
#Creating stars
stars = []
frames_until_next_star = 0



#Initializing ship's coordinates
ship = Sprite()
ship.x = window.get_width() / 2
ship.y = window.get_height() - 10
ship.red = 0
ship.alpha = 0
ship.image = ship_image

#Initializing Score Bar
score = 0
highest_score = 0
lives = 3

bullets = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            print ("mouse at (%d, %d)" % event.pos)
        elif event.type == pygame.QUIT:
            sys.exit()
        elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE) and (lives == 0) and (ship.alpha == 0):
            ship = Sprite()
            ship.x = window.get_width() / 2
            ship.y = window.get_height() - 10
            ship.red = 0
            ship.alpha = 0
            ship.image = ship_image

            score = 0
            lives = 3
            bullets = []
            rocks = []
            stars = []
            frames_until_next_rock = 50
            frames_until_next_star = 0

            break

        if lives > 0:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_UP]:
                ship.y = ship.y - 10
            if pressed_keys[pygame.K_DOWN]:
                ship.y = ship.y + 10
            if pressed_keys[pygame.K_LEFT]:
                ship.x = ship.x - 10
            if pressed_keys[pygame.K_RIGHT]:
                ship.x = ship.x + 10

            # Stop ship going out of bounds
            if ship.y < 10:
                ship.y = 10

            if ship.y > window.get_height() - 10:
                ship.y = window.get_height() - 10

            if ship.x < 0:
                ship.x = 0

            if ship.x > window.get_width() - ship_image.get_width():
                ship.x = window.get_width() - ship_image.get_width()

    data = stream.read(CHUNK,exception_on_overflow = False)
    sample = np.fromstring(data, dtype=aubio.float_type)
    pitch=voiceDetection(sample)[0]
    volume=np.sum(sample**2)/len(sample)
    #print("Volume: %s" % (volume))
    #print("Pitch: %s" % (pitch))
    if (volume > 0.001) and (lives > 0):
        fire_bullet()

    for bullet in bullets:
        bullet.y = bullet.y - 13

    bullets = [bullet for bullet in bullets if bullet.y > - bullet_image.get_height() and not bullet.used]

    frames_until_next_rock = frames_until_next_rock - 1
    if frames_until_next_rock <= 0:
        frames_until_next_rock = random.randrange(30, 100)
        add_rock()

    ship.red = max(0, ship.red - 10)
    ship.alpha = max(0, ship.alpha - 2)
    ship_rect = get_sprite_rectangle(ship)

    for rock in rocks:
        rock.y = rock.y + 3
        if rock.hit:
            rock.alpha = max(0, rock.alpha - 10)

    rocks = [rock for rock in rocks if rock.y < window.get_height() and not (rock.hit and rock.alpha == 0)]

    frames_until_next_star = frames_until_next_star - 1
    if frames_until_next_star <= 0:
        frames_until_next_star = random.randrange(10, 30)
        add_star()

    for star in stars:
        star.y = star.y + 2

    stars = [star for star in stars if star.y < window.get_height()]

    for rock in rocks:
        if rock.hit:
            continue
        rock_rect = get_sprite_rectangle(rock)
        if rock_rect.colliderect(ship_rect) and lives > 0:
            rock.hit = True
            rock.x = rock.x - 6
            rock.y = rock.y - 6
            lives = lives - 1
            if lives == 0:
                # ship.x = ship.x - 50
                ship.alpha = 255
            else:
                ship.red = 255
            continue
        for bullet in bullets:
            if rock_rect.colliderect(get_sprite_rectangle(bullet)):
                rock.hit = True
                rock.x = rock.x - 6
                rock.y = rock.y - 6
                bullet.used = True
                score = score + 10
                highest_score = max(score, highest_score)
                continue

    window.fill(background)
    if lives == 0:
        tmp = pygame.Surface(ship_image.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255, 255, ship.alpha) )
        tmp.blit(ship_image, (0,0), ship_image.get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = tmp
        # tmp = pygame.Surface(ship_image_destroyed.get_size(), pygame.SRCALPHA, 32)
        # tmp.fill( (255, 255, 255, ship.alpha) )
        # tmp.blit(ship_image_destroyed, (0,0), ship_image_destroyed.get_rect(), pygame.BLEND_RGBA_MULT)
        # ship.image = tmp
    if ship.red > 0:
        tmp = pygame.Surface(ship_image.get_size(), pygame.SRCALPHA, 32)
        tmp.fill( (255, 255 - ship.red, 255 - ship.red, 255) )
        tmp.blit(ship_image, (0,0), ship_image.get_rect(), pygame.BLEND_RGBA_MULT)
        ship.image = tmp

    for star in stars:
        display_sprite(star)
    display_sprite(ship)
    for bullet in bullets:
        display_sprite(bullet)
    for rock in rocks:
        if rock.hit:
            tmp = pygame.Surface(rock_broken_image.get_size(), pygame.SRCALPHA, 32)
            tmp.fill( (255, 255, 255, rock.alpha) )
            tmp.blit(rock_broken_image, (0,0), rock_broken_image.get_rect(), pygame.BLEND_RGBA_MULT)
            rock.image = tmp
            # tmp = pygame.Surface(alien_dead_image.get_size(), pygame.SRCALPHA, 32)
            # tmp.fill( (255, 255, 255, alien.alpha) )
            # tmp.blit(alien_dead_image, (0,0), alien_dead_image.get_rect(), pygame.BLEND_RGBA_MULT)
            # alien.image = tmp
        display_sprite(rock)

    score_text = font.render("SCORE: " + str(score), 1, foreground)
    score_text_pos = score_text.get_rect()
    score_text_pos.right = window.get_width() - 10
    score_text_pos.top = 10
    window.blit(score_text, score_text_pos)
    highest_score_text = font.render("HIGHEST SCORE: " + str(highest_score), 1, foreground)
    highest_score_text_pos = highest_score_text.get_rect()
    highest_score_text_pos.left = (window.get_width() - (highest_score_text_pos.right-highest_score_text_pos.left))/2
    highest_score_text_pos.top = 10
    window.blit(highest_score_text, highest_score_text_pos)
    lives_text = font.render("LIVES: " + str(lives), 1, foreground)
    window.blit(lives_text, (10, 10))
    if (lives == 0) and (ship.alpha == 0):
        restart_text = font.render("PRESS SPACE TO RESTART THE GAME", 1, foreground)
        restart_text_pos = restart_text.get_rect()
        restart_text_pos.left = (window.get_width() - (restart_text_pos.right-restart_text_pos.left))/2
        restart_text_pos.bottom = window.get_height() - 10
        window.blit(restart_text, restart_text_pos)

    pygame.display.flip()
    clock.tick(50)
