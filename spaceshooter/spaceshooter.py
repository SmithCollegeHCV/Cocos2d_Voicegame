import pygame
import sys
import random
import pyaudio
import aubio
import numpy as np
import time

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

#blinking images
sparks = ["assets2/spark_1.png","assets2/spark_2.png","assets2/spark_3.png","assets2/spark_4.png",
     "assets2/spark_5.png","assets2/spark_6.png","assets2/spark_7.png","assets2/spark_8.png",
     "assets2/spark_9.png","assets2/spark_8.png","assets2/spark_7.png","assets2/spark_6.png",
     "assets2/spark_5.png","assets2/spark_4.png","assets2/spark_3.png","assets2/spark_2.png",
     "assets2/spark_1.png"]

## global list for testing volume and pitch
volume_avg_list = []
volume_avg = 0.0003
volume_std=0.0002
speaker = ["assets2/test_1.png","assets2/test_2.png","assets2/test_3.png"]

## global list for testing nosies
silence_list = []
silence_avg = 0
silence_std= 0


#Initialize menu
def main_menu():
    global screen
    menu_song = pygame.mixer.music.load("sounds/menu.mp3")
    pygame.mixer.music.play(-1)
    title = pygame.image.load("assets2/Logan_space_title.png")
    count = 0
    spark = sparks[0]
    pygame.display.flip()

    while True:
        count = count + 1
        if count%21 == 0 or count%21 == 20:
            spark = sparks[0]
        elif count%21 == 1 or count%21 == 19:
            spark = sparks[1]
        elif count%21 == 2 or count%21 == 18:
            spark = sparks[2]
        elif count%21 == 3 or count%21 == 17:
            spark = sparks[3]
        elif count%21 == 4 or count%21 == 16:
            spark = sparks[4]
        elif count%21 == 5 or count%21 == 15:
            spark = sparks[5]
        elif count%21 == 6 or count%21 == 14:
            spark = sparks[6]
        elif count%21 == 7 or count%21 == 13:
            spark = sparks[7]
        elif count%21 == 8 or count%21 == 12:
            spark = sparks[8]
        else:
            spark = sparks[9]

        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        else:
            enter = pygame.image.load("assets2/subtitle_1.png")
            quitt = pygame.image.load("assets2/subtitle_2.png")
            spark_draw = pygame.image.load(spark)
            window.blit(spark_draw,(40,70))
            window.blit(title,(120,100))
            window.blit(enter,(120,520))
            window.blit(quitt,(120,580))
            pygame.display.flip()
            clock.tick(7)
            window.fill(pygame.Color("black"))

def instruction():
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        else:
            instruction_1 = pygame.image.load("assets2/instruction1.png")
            window.blit(instruction_1,(0,0))
            instruction_2 = pygame.image.load("assets2/instruction2.png")
            window.blit(instruction_2,(0,0))
            instruction_3 = pygame.image.load("assets2/instruction3.png")
            window.blit(instruction_3,(0,0))
            pygame.display.flip()

def silence_test():
    window.fill(pygame.Color("black"))
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        else:

            text = pygame.image.load("assets2/silent_text.png")
            window.blit(text,(0,0))
            pygame.display.flip()
            clock.tick(2)

            data = stream.read(CHUNK,exception_on_overflow = False)
            sample = np.fromstring(data, dtype=aubio.float_type)
            volume=np.sum(sample**2)/len(sample)
            silence_list.append(volume)
            #print(volume)


def voice_test():
    count = 0
    speaker_tmp = speaker[0]
    window.fill(pygame.Color("black"))
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        else:
            count = count + 1
            if count%3 == 0:
                speaker_tmp = speaker[0]
            elif count%3 == 1:
                speaker_tmp = speaker[1]
            else:
                speaker_tmp = speaker[2]

            speaker_draw = pygame.image.load(speaker_tmp)
            speaker_draw = pygame.transform.scale(speaker_draw, (100,100))
            text = pygame.image.load("assets2/test_0.png")
            window.blit(text,(0,0))
            window.blit(speaker_draw,(220,380))
            pygame.display.flip()
            clock.tick(2)
            window.fill(pygame.Color("black"))

            data = stream.read(CHUNK,exception_on_overflow = False)
            sample = np.fromstring(data, dtype=aubio.float_type)
            volume=np.sum(sample**2)/len(sample)
            if (volume > silence_avg+silence_std):
                volume_avg_list.append(volume)
            #print(volume)

main_menu()
instruction()
pygame.mixer.music.stop()
silence_test()
silence_avg=np.array(silence_list).mean()
silence_std=np.array(silence_list).std()
print("Average nosies is %s" % silence_avg)
print("Nosies Standard Deviation is %s" % silence_std)
voice_test()
volume_avg=np.array(volume_avg_list).mean()
volume_std=np.array(volume_avg_list).std()
print("Average volume is %s" % (volume_avg))
print("Volume Standard Deviation is %s" % (volume_std))
pygame.time.wait(1000)

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

def add_spaceship():
    spaceship = Sprite()
    spaceship.score = random.randrange(3,8)*2
    spaceship.blood = (spaceship.score-4)*5
    scale = spaceship.score/200
    spaceship.image = spaceship_image
    spaceship.image = pygame.transform.scale(spaceship.image, (int(spaceship.image.get_width()*scale), int(spaceship.image.get_height()*scale)))
    spaceship.x = random.randrange(window.get_width()-spaceship.image.get_width())
    spaceship.y = 10
    spaceship.hit = False
    spaceship.alpha = 255
    spaceships.append(spaceship)

def add_rock():
    global rock_images,rock_broken_images
    rock = Sprite()
    index = random.randrange(4)
    rock.image = rock_images[index]
    rock.score = random.randrange(7,14)
    rock.blood = (rock.score-6)*5
    scale = rock.score/200
    if index == 0:
        scale *= 2
    rock.image = pygame.transform.scale(rock.image, (int(rock.image.get_width()*scale), int(rock.image.get_height()*scale)))
    rock.broken_image = rock_broken_images[index]
    if index == 0:
        scale *= 0.8
    rock.broken_image = pygame.transform.scale(rock.broken_image, (int(rock.broken_image.get_width()*scale), int(rock.broken_image.get_height()*scale)))
    rock.x = random.randrange(0, window.get_width()-rock.image.get_width())
    rock.y = 10
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

def load_image(name):
    return pygame.image.load("assets2/"+name+".png")

def scale_image(image, scale):
    return pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))

#Creating score bar
font = pygame.font.Font(None,24)
foreground = (200,200,200)
#Creating the background
background = (0,0,0)
#Creating the spaceship
ship_image = scale_image(load_image("spaceship"),0.1)
#Creating the bullet
bullet_image = scale_image(load_image("bullet"),0.02)
#Creating aliens
alien_image = scale_image(load_image("alien"),0.02)
#Creating spaceship
spaceship_image = load_image("ufo")
spaceships = []
frames_until_next_spaceship = random.randrange(10, 20)
#Creating rocks
rock_image = load_image("rock")
rock_broken_image = load_image("rock_broken")
rock2_image = load_image("rock2")
rock2_broken_image = load_image("rock2_broken")
rock3_image = load_image("rock3")
rock3_broken_image = load_image("rock3_broken")
rock4_image = load_image("rock4")
rock4_broken_image = load_image("rock4_broken")
rock_images = [rock_image,rock2_image,rock3_image,rock4_image]
rock_broken_images = [rock_broken_image,rock2_broken_image,rock3_broken_image,rock4_broken_image]
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
alien = None
num_enemies = 0
pygame.key.set_repeat(10,10)

while True:
    global num_enemies
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

    if (max(volume_avg - volume_std,volume_avg/2) < volume < volume_avg + volume_std) and (lives > 0):
        fire_bullet()

    for bullet in bullets:
        bullet.y = bullet.y - 13

    bullets = [bullet for bullet in bullets if bullet.y > - bullet_image.get_height() and not bullet.used]

    frames_until_next_rock -= 1
    if frames_until_next_rock <= 0:
        num_enemies += 1
        if num_enemies % frames_until_next_spaceship == 0:
            add_spaceship()
            frames_until_next_spaceship = random.randrange(10, 20)
            num_enemies = 0
        else:
            add_rock()
        frames_until_next_rock = random.randrange(30, 100)

    ship.red = max(0, ship.red - 10)
    ship.alpha = max(0, ship.alpha - 2)
    ship_rect = get_sprite_rectangle(ship)

    for rock in rocks:
        rock.y = rock.y + 3
        if rock.hit:
            rock.alpha = max(0, rock.alpha - 10)

    for spaceship in spaceships:
        spaceship.y = spaceship.y + 3
        if spaceship.hit:
            spaceship.alpha = max(0, spaceship.alpha - 10)

    rocks = [rock for rock in rocks if rock.y < window.get_height() and not (rock.hit and rock.alpha == 0)]

    spaceships = [spaceship for spaceship in spaceships if spaceship.y < window.get_height() and not (spaceship.hit and spaceship.alpha == 0)]

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
                rock.blood -= 10
                if rock.blood <= 0:
                    rock.hit = True
                    rock.x = rock.x - 6
                    rock.y = rock.y - 6
                    score = score + rock.score
                    highest_score = max(score, highest_score)
                bullet.used = True
                continue

    for spaceship in spaceships:
        if spaceship.hit:
            continue
        spaceship_rect = get_sprite_rectangle(spaceship)
        if spaceship_rect.colliderect(ship_rect) and lives > 0:
            spaceship.hit = True
            lives = lives - 1
            if lives == 0:
                ship.alpha = 255
            else:
                ship.red = 255
            continue
        for bullet in bullets:
            if spaceship_rect.colliderect(get_sprite_rectangle(bullet)):
                spaceship.blood -= 10
                if spaceship.blood <= 0:
                    spaceship.hit = True
                    score = score + spaceship.score
                    highest_score = max(score, highest_score)
                bullet.used = True
                continue

    if alien != None:
        alien.y = alien.y + 3
        if alien.hit:
            alien.alpha = max(0, alien.alpha - 10)
            tmp = pygame.Surface(alien.image.get_size(), pygame.SRCALPHA, 32)
            tmp.fill( (255, 255, 255, alien.alpha) )
            tmp.blit(alien.image, (0,0), alien.image.get_rect(), pygame.BLEND_RGBA_MULT)
            alien.image = tmp
        alien_rect = get_sprite_rectangle(alien)
        if alien_rect.colliderect(ship_rect) and lives > 0:
            alien.hit = True
            lives = 0
            ship.alpha = 255
            continue
        for bullet in bullets:
            if alien_rect.colliderect(get_sprite_rectangle(bullet)):
                alien.blood -= 10
                if alien.blood <= 0:
                    alien.hit = True
                    score = score + alien.score
                    highest_score = max(score, highest_score)
                bullet.used = True
                continue
    elif score >= 300:
        alien = Sprite()
        alien.x = random.randrange(0, window.get_width()-alien_image.get_width())
        alien.y = 10
        alien.image = alien_image
        alien.hit = False
        alien.alpha = 255
        alien.score = 50
        alien.blood = 50
        window.fill(background)
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
            tmp = pygame.Surface(rock.broken_image.get_size(), pygame.SRCALPHA, 32)
            tmp.fill( (255, 255, 255, rock.alpha) )
            tmp.blit(rock.broken_image, (0,0), rock.broken_image.get_rect(), pygame.BLEND_RGBA_MULT)
            rock.image = tmp
        display_sprite(rock)
    for spaceship in spaceships:
        if spaceship.hit:
            tmp = pygame.Surface(spaceship.image.get_size(), pygame.SRCALPHA, 32)
            tmp.fill( (255, 255, 255, spaceship.alpha) )
            tmp.blit(spaceship.image, (0,0), spaceship.image.get_rect(), pygame.BLEND_RGBA_MULT)
            spaceship.image = tmp
        display_sprite(spaceship)
    if alien != None:
        display_sprite(alien)
        if alien.y > window.get_height():
            lives = 0
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

    if alien != None and alien.hit and alien.alpha == 0:
        break
font = pygame.font.Font(None,54)
comgrats_text = font.render("CONGRATULATIONS!", 1, foreground)
comgrats_text_pos = comgrats_text.get_rect()
comgrats_text_pos.left = (window.get_width() - (comgrats_text_pos.right-comgrats_text_pos.left))/2
comgrats_text_pos.bottom = window.get_height()/2
window.blit(comgrats_text, comgrats_text_pos)
