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

#Draw stars
def add_star():
    star = Sprite()
    star_size = random.randrange(1,4)
    star.x = random.randrange(0, window.get_width())
    star.y = 0
    star.image = pygame.Surface((star_size,star_size))
    star.image.fill((255,255,255))
    stars.append(star)

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
        if count%19 == 0:
            spark = sparks[0]
        elif count%19 == 1:
            spark = sparks[1]
        elif count%19 == 2:
            spark = sparks[2]
        elif count%19 == 3:
            spark = sparks[3]
        elif count%19 == 4:
            spark = sparks[4]
        elif count%19 == 5:
            spark = sparks[5]
        elif count%19 == 6:
            spark = sparks[6]
        elif count%19 == 7:
            spark = sparks[7]
        elif count%19 == 8:
            spark = sparks[8]
        elif count%19 == 9:
            spark = sparks[9]
        elif count%19 == 10:
            spark = sparks[9]
        elif count%19 == 11:
            spark = sparks[9]
        elif count%19 == 12:
            spark = sparks[8]
        elif count%19 == 13:
            spark = sparks[7]
        elif count%19 == 14:
            spark = sparks[6]
        elif count%19 == 15:
            spark = sparks[5]
        elif count%19 == 16:
            spark = sparks[4]
        elif count%19 == 17:
            spark = sparks[3]
        elif count%19 == 18:
            spark = sparks[2]
        elif count%19 == 19:
            spark = sparks[1]
        
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
            
def voice_test():
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
            test_1 = pygame.image.load("assets2/test_1.png")
            window.blit(test_1,(0,0))
            pygame.display.flip()
            time.sleep(10)
            test_2 = pygame.image.load("assets2/test_2.png")
            window.blit(test_2,(0,0))
            pygame.display.flip()
            
        

    
    
    
main_menu()
pygame.time.wait(3000)
pygame.mixer.music.stop()

voice_test()
pygame.time.wait(1000)


#####################################################################################################
##class Sprite:
##    pass
##
##def display_sprite(sprite):
##    window.blit(sprite.image, (sprite.x, sprite.y))
##    
##def fire_bullet():
##    bullet = Sprite()
##    bullet.x = ship.x
##    bullet.y = ship.y
##    bullet.image = bullet_image
##    bullet.used = False
###    if bullet.used == True:
###        bullets.remove(bullet)
##    bullets.append(bullet)
##
##def add_alien():
##    alien = Sprite()
##    alien.x = random.randrange(0, window.get_width())
##    alien.y = 0
##    alien.image = alien_image
##    alien.hit = False
###    if alien.hit == True:
###        aliens.remove(alien)
##    aliens.append(alien)
##    
##
##
##def get_sprite_rectangle(sprite):
##    return sprite.image.get_rect().move(sprite.x, sprite.y)
##
###Creating score bar
##font = pygame.font.Font(None,24)
##foreground = (200,200,200)
###Creating the background
##background = (0,0,0)
###Creating the spaceship
##ship_image = pygame.image.load("assets2/spaceship_0.png")
###ship_image = pygame.transform.scale(ship_image, (70, 70))
###Creating the bullet
##bullet_image = pygame.image.load("assets2/bullet_0.png")
###bullet_image = pygame.transform.scale(bullet_image, (20, 40))
###Creating aliens
##alien_image = pygame.image.load("assets2/spaceship_0.png")
###alien_image = pygame.transform.scale(alien_image, (70, 70))
##aliens = []
##frames_until_next_alien = random.randrange(30, 100)
###Creating stars
##stars = []
##frames_until_next_star = 0
##
##
##
###Initializing ship's coordinates
##ship = Sprite()
##ship.x = 0
##ship.y = 600
##ship.image = ship_image
##
###Initializing Score Bar
##score = 0
##
##bullets = []
##
##
##while True:
##    for event in pygame.event.get():
##        if event.type == pygame.MOUSEMOTION:
##            print ("mouse at (%d, %d)" % event.pos)
##        if event.type == pygame.QUIT:
##            sys.exit()            
##        pressed_keys = pygame.key.get_pressed()
##        if pressed_keys[pygame.K_UP]:
##            ship.y = ship.y - 10
##        if pressed_keys[pygame.K_DOWN]:
##            ship.y = ship.y + 10
##        if pressed_keys[pygame.K_LEFT]:
##            ship.x = ship.x - 10
##        if pressed_keys[pygame.K_RIGHT]:
##            ship.x = ship.x + 10
####        if pressed_keys[pygame.K_SPACE]:
####            print("Pressed on space ")
####            fire_bullet()
##    data = stream.read(CHUNK,exception_on_overflow = False)
##    sample = np.fromstring(data, dtype=aubio.float_type)
##    pitch=voiceDetection(sample)[0]
##    volume=np.sum(sample**2)/len(sample)
##    #print("Volume: %s" % (volume))
##    #print("Pitch: %s" % (pitch))
##    if(volume > 0.02) :
##        fire_bullet()
##        
##    for bullet in bullets:
##        bullet.y = bullet.y - 13
##
##    for alien in aliens:
##        alien_rect = get_sprite_rectangle(alien)
##        #print(alien_rect)
##        for bullet in bullets:
##            if alien_rect.colliderect(get_sprite_rectangle(bullet)):
##                alien.hit = True
##                score = score + 10
##                bullet.used = True
##                continue
##            
##        
##
##    window.fill(background)
##    frames_until_next_alien = frames_until_next_alien - 1
##    if frames_until_next_alien < 0:
##        frames_until_next_alien = random.randrange(30, 100)
##        add_alien()
##    for alien in aliens:
##        alien.y = alien.y + 3
##
##    frames_until_next_star = frames_until_next_star - 1
##    if frames_until_next_star <= 0:
##        frames_until_next_star = random.randrange(10,30)
##        add_star()
##    for star in stars:
##        star.y = star.y + 2
##
##
##    for star in stars:
##        display_sprite(star)
##    display_sprite(ship)
##    for bullet in bullets:
##        if bullet.used == False:
##            display_sprite(bullet)
##    for alien in aliens:
##        if alien.hit == False:
##            display_sprite(alien)
##    score_text = font.render("SCORE: " + str(score),1, foreground)
##    score_text_pos =score_text.get_rect()
##    score_text_pos.right = window.get_width() - 10
##    score_text_pos.top = 10
##    window.blit(score_text, score_text_pos)
##    pygame.display.flip()
##    clock.tick(50)
##
##
##
##
