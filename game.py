#package for audio
import pyaudio
import aubio
import numpy as np
import random

#package for game
import cocos
from cocos.director import director
from cocos.actions import *

from cocos.layer import ScrollingManager, ScrollableLayer, ColorLayer
from cocos.tiles import load
from cocos.tiles import MapLayer

from pyglet.app import exit
from cocos.menu import *
from cocos.scene import *
from cocos.scenes import FadeTransition
from cocos.layer import *
## cocos audio
from cocos.audio import pygame
import time

#package for plotting
import matplotlib.pyplot as plt

import sys

global WIDTH, HEIGHT, num_pitches, x_coors, num_bloomed, num_flowers, flower_under_mouse, num_flowers_list, audiomixer, clicksound, bgmplayed
WIDTH=960
HEIGHT=568
num_pitches=[0]*7
num_flowers_list=[0]*7
x_coors=list(range(0,285,15))
num_bloomed=0
num_flowers=19
flower_under_mouse=None

## global variable for audio
audiomixer=pygame.mixer
audiomixer.init()
clicksound=audiomixer.Sound('click.ogg')
bgmplayed=False

director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=False)

#scroller for game background
scroller = ScrollingManager()
mapLayer = load("assets/map/map_garden_back_01.tmx")["TileLayer1"]
scroller.add(mapLayer)

#scroller_menu for menu background
scroller_menu=ScrollingManager()
mapLayer_menu = load("assets/map/map_menu.tmx")["TileLayer1"]
scroller_menu.add(mapLayer_menu)

#class for flower
class Flower(cocos.layer.Layer):

    def __init__(self, idnum, color):
        global flowers, x_coors
        super(Flower,self).__init__()

        #flower property
        self.id=idnum
        self.color=color
        self.water=0
        self.nutrition=0
        self.stage="seed"
        x=random.choice(x_coors)
        x_coors.remove(x)
        self.position=x,75

        #Draw seed
        self.seed=cocos.sprite.Sprite('ui/seed.png')
        self.seed.scale_y=0.04
        self.seed.scale_x=0.04
        self.seed.position=self.position
        self.seed.image_anchor=0,0
        self.stage2=True
        self.stage3=False
        self.stage4=False
        self.stage5=False
        self.stage6=False
        self.stage7=False
        self.add(self.seed)
        self.schedule(self.update)

    def update(self, dt):
        if((self.stage2) and (self.water > 10) and (self.nutrition > 20)):
            print('stage2')
            self.remove(self.seed)
            self.seedling=cocos.sprite.Sprite('ui/Seedling.png')
            self.seedling.scale_y=0.02
            self.seedling.scale_x=0.02
            self.seedling.position=self.position
            self.seedling.image_anchor=0,0
            self.add(self.seedling)
            self.stage2=False
            self.stage3=True
            self.stage="seedling"
        if((self.stage3) and (self.water > 20) and (self.nutrition > 20)):
            print('stage3')
            self.remove(self.seedling)
            self.seedling2=cocos.sprite.Sprite('ui/Seedling2.png')
            self.seedling2.scale_y=0.04
            self.seedling2.scale_x=0.04
            x, y=self.position
            self.seedling2.position=x,y+5
            self.seedling2.image_anchor=0,0
            self.add(self.seedling2)
            self.stage3=False
            self.stage4=True
            self.stage="seedling2"
        if((self.stage4) and (self.water > 30) and (self.nutrition > 30)):
            print('stage4')
            self.remove(self.seedling2)
            self.flowerbud=cocos.sprite.Sprite('ui/Flowerbud.png')
            self.flowerbud.scale_y=0.04
            self.flowerbud.scale_x=0.04
            x, y=self.position
            self.flowerbud.position=x,y+5
            self.flowerbud.image_anchor=0,0
            self.add(self.flowerbud)
            self.stage4=False
            self.stage5=True
            self.stage="flowerbud"
        if((self.stage5) and (self.water > 40) and (self.nutrition > 40)):
            print('stage5')
            self.remove(self.flowerbud)
            self.flowerbud2=cocos.sprite.Sprite('ui/Flowerbud2.png')
            self.flowerbud2.scale_y=0.04
            self.flowerbud2.scale_x=0.04
            x, y=self.position
            self.flowerbud2.position=x,y+5
            self.flowerbud2.image_anchor=0,0
            self.add(self.flowerbud2)
            self.stage5=False
            self.stage6=True
            self.stage="flowerbud2"
        if((self.stage6) and (self.water >= 50) and (self.nutrition >= 50)):
            print('stage6')
            self.remove(self.flowerbud2)
            self.flowerstem=cocos.sprite.Sprite('ui/Withoutflower.png')
            self.flowerstem.scale_y=0.04
            self.flowerstem.scale_x=0.04
            x, y=self.position
            self.flowerstem.position=x,y+5
            self.flowerstem.image_anchor=0,0
            self.add(self.flowerstem)
            self.flower=cocos.sprite.Sprite(self.color)
            self.flower.scale_y=0.07
            self.flower.scale_x=0.07
            self.flower.image_anchor=0,0
            self.flower.position=x+15,y+80
            self.add(self.flower)
            self.stage6=False
            self.stage7=True
            self.stage="flower"

    #reset flower
    def reset(self):
        self.water=0
        self.nutrition=0
        self.stage2=True
        if (self.stage7):
            self.remove(self.flowerstem)
            self.remove(self.flower)
            self.stage7=False
        self.add(self.seed)

#class for nutrition
class NutritionBar(cocos.layer.Layer):

    def __init__(self,flower):
        super(NutritionBar,self).__init__()

        #Draw nutritionbar
        self.nutritionbar=cocos.sprite.Sprite('ui/NutritionBar.png')
        self.nutritionbar.scale_y=0.2
        self.nutritionbar.scale_x=0.2
        self.nutritionbar.position=790-self.nutritionbar.width/2,260
        self.nutritionbar.image_anchor=0,0
        self.add(self.nutritionbar)

        #Draw nutritionicon
        self.nutritionicon=cocos.sprite.Sprite('ui/NutritionIcon.png')
        self.nutritionicon.scale_y=0.0625
        self.nutritionicon.scale_x=0.0625
        self.nutritionicon_initial=770-self.nutritionbar.width/2
        self.nutritionicon.position=self.nutritionicon_initial+min(self.nutritionbar.width,flower.nutrition),275
        self.nutritionicon.image_anchor=0,0
        self.add(self.nutritionicon)

    # get value of nutritionicon
    def get_value(self):
        position=self.nutritionicon.x-self.nutritionicon_initial
        return(position)

    def set_value(self,speed):
        #move=MoveBy((,0))
        #self.watericon.do(move)
        if(self.get_value()<=self.nutritionbar.width):
            self.nutritionicon.x+=speed
        # else:
        #     self.reset()

    def reset(self):
        self.speed=0
        self.nutritionicon.position=self.nutritionicon_initial,275

#class for water
class WaterBar(cocos.layer.Layer):

    def __init__(self,flower):
        super(WaterBar,self).__init__()

        #Draw waterbar
        self.waterbar=cocos.sprite.Sprite('ui/WaterBar.png')
        self.waterbar.scale_y=0.2
        self.waterbar.scale_x=0.2
        self.waterbar.image_anchor=0,0
        self.waterbar.position=790-self.waterbar.width/2,300
        self.add(self.waterbar)

        #Draw watericon
        self.watericon=cocos.sprite.Sprite('ui/WaterIcon.png')
        self.watericon.scale_y=0.02
        self.watericon.scale_x=0.02
        self.watericon_initial=770-self.waterbar.width/2
        self.watericon.position=self.watericon_initial+min(self.waterbar.width,flower.water),315
        self.watericon.image_anchor=0,0
        self.add(self.watericon)

    # get value of watericon
    def get_value(self):
        position=self.watericon.x-self.watericon_initial
        return(position)

    def set_value(self,speed):
        #move=MoveBy((,0))
        #self.watericon.do(move)
        if(self.get_value()<=self.waterbar.width):
            self.watericon.x+=speed
        # else:
        #     self.reset()

    def reset(self):
        self.speed=0
        self.watericon.position=self.watericon_initial,315

#input voice class
class InputVoice(cocos.layer.Layer):
    is_event_handler=True

    def __init__(self):
        super(InputVoice,self).__init__()
        # init voice
        self.CHUNK=1024
        self.RATE=44100

        self.pitchLabel=cocos.text.Label('Pitch: ',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.volumeLabel=cocos.text.Label('Volume: ',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.plantLabel=cocos.text.Label('Number of flowers planted: ',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.bloomLabel=cocos.text.Label('Number of flowers bloomed: ',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.colorLabel=cocos.text.Label('Color of the newest flower: ',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.colorLabel2=cocos.text.Label('',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.stageLabel=cocos.text.Label('',
                                          font_name='Times New Roman',
                                          font_size=16,
                                          anchor_x='center', anchor_y='center')

        self.pitchLabel.position=780,100
        self.volumeLabel.position=780,140
        self.plantLabel.position=780,480
        self.bloomLabel.position=780,440
        self.colorLabel.position=780,400
        self.colorLabel2.position=780,220
        self.stageLabel.position=780,180

        self.add(self.pitchLabel)
        self.add(self.volumeLabel)
        self.add(self.plantLabel)
        self.add(self.bloomLabel)
        self.add(self.colorLabel)
        self.add(self.colorLabel2)
        self.add(self.stageLabel)

        #init voice input
        p=pyaudio.PyAudio()

        #Open stream
        self.stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        # Aubio's pitch detection
        self.pDetection = aubio.pitch("default", self.CHUNK*2, self.CHUNK, self.RATE)

        #Set unit.
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-40)

        #add flower
        self.flowers = cocos.cocosnode.CocosNode()
        self.flowerid=1
        self.flower=Flower(self.flowerid,'ui/white.png')
        self.colorLabel.element.text='Color of the newest flower: white'
        self.flowers.add(self.flower)
        num_flowers_list[6]+=1
        self.add(self.flowers)

        self.water=WaterBar(self.flower)
        self.nutrition=NutritionBar(self.flower)

        self.endmenuLayer=None

        self.schedule(self.update)

    # check is mouse is hovering over a flower
    def is_inside(self, flower, x, y):
        position_x,position_y=flower.position
        if (flower.stage4):
            dx1=2
            dx2=18
            dy1=1
            dy2=20
        elif (flower.stage5):
            dx1=2
            dx2=20
            dy1=1
            dy2=30
        elif (flower.stage6):
            dx1=8
            dx2=27
            dy1=0
            dy2=58
        elif (flower.stage7):
            dx1=8
            dx2=27
            dy1=0
            dy2=59
        else:
            dx1=5
            dx2=15
            dy1=0
            dy2=15
        return ((position_x+dx1 < x/2 < position_x+dx2) and (position_y+dy1 < y/2 < position_y+dy2))

    # mouse motion handler
    def on_mouse_motion(self, x, y, dx, dy):
        global flower_under_mouse
        x,y=director.get_virtual_coordinates(x,y)
        if (flower_under_mouse != None):
            if (not self.is_inside(flower_under_mouse,x,y)):
                flower_under_mouse=None
                self.remove(self.water)
                self.remove(self.nutrition)
                self.colorLabel2.element.text=''
                self.stageLabel.element.text=''
        else:
            for flower in self.flowers.get_children():
                if (self.is_inside(flower,x,y)):
                    flower_under_mouse=flower
                    break
            if (flower_under_mouse != None):
                self.water=WaterBar(flower_under_mouse)
                self.nutrition=NutritionBar(flower_under_mouse)
                self.colorLabel2.element.text='Color: '+flower_under_mouse.color[3:-4]
                self.stageLabel.element.text='Stage: '+flower_under_mouse.stage
                self.add(self.water)
                self.add(self.nutrition)

    def add_flower(self, i, color):
        global num_pitches, x_coors, flowers, num_flowers_list
        num_pitches[i]+=1
        if ((num_pitches[i]%50 == 0) and (len(x_coors) > 0)):
            print(self.flowerid)
            self.flowerid+=1
            new_flower=Flower(self.flowerid,'ui/'+color+'.png')
            self.flowers.add(new_flower)
            num_flowers_list[i]+=1
            self.colorLabel.element.text='Color of the newest flower: '+color

    def update(self,dt):
        global num_pitches, x_coors, num_bloomed, num_flowers, audiomixer
        if (num_bloomed < num_flowers):
            data = self.stream.read(self.CHUNK,exception_on_overflow = False)
            sample = np.fromstring(data, dtype=aubio.float_type)
            pitch=self.pDetection(sample)[0]
            volume=np.sum(sample**2)/len(sample)

            if (0 < pitch < 200):
                self.add_flower(0, 'purple')
            elif (200 <= pitch < 250):
                self.add_flower(1, 'blue')
            elif (250 <= pitch < 300):
                self.add_flower(2, 'cyan')
            elif (300 <= pitch < 400):
                self.add_flower(3, 'orange')
            elif (400 <= pitch < 500):
                self.add_flower(4, 'pink')
            elif (500 <= pitch < 600):
                self.add_flower(5, 'yellow')
            elif (600 <= pitch < 1100):
                self.add_flower(6, 'white')

            if(volume > 0.0002):
                n=len(self.flowers.get_children())
                num_bloomed=0
                for flower in self.flowers.get_children():
                    flower.water+=1/n
                    flower.nutrition+=2/n
                    if (flower.stage7):
                        num_bloomed+=1

                self.water.set_value(1/n)
                self.nutrition.set_value(2/n)

            volume="{:.6f}".format(volume)
            #print(dt)
            self.pitchLabel.element.text='Pitch: '+pitch.astype('str')
            self.volumeLabel.element.text='Volume: '+volume
            self.plantLabel.element.text='Number of flowers planted: '+str(len(self.flowers.get_children()))
            self.bloomLabel.element.text='Number of flowers bloomed: '+str(num_bloomed)
            if (flower_under_mouse != None):
                self.stageLabel.element.text='Stage: '+flower_under_mouse.stage
            if (num_bloomed == num_flowers):
                self.pitchLabel.element.text=''
                self.volumeLabel.element.text=''
                self.colorLabel.element.text=''
                self.congratsLabel=cocos.text.Label('Congratulations!',
                                                  font_name='Times New Roman',
                                                  font_size=36,
                                                  anchor_x='center', anchor_y='center')
                self.congratsLabel.position=780,120
                self.add(self.congratsLabel)

                audiomixer.unpause()
                #add end menu
                self.endmenuLayer=MultiplexLayer(GameEnd(self))
                endscene=cocos.scene.Scene(scroller_menu,self.endmenuLayer)
                director.replace(FadeTransition(endscene, duration=2))

    def  reset(self):
        #remove all flowers
        global num_pitches, num_bloomed, num_flowers, x_coors
        for f in self.flowers.get_children():
            if(f.id!=1):
                self.flowers.remove(f)

        #reset all children
        self.nutrition.reset()
        self.water.reset()
        self.flower.reset()

        #clear all lists
        num_pitches=[0]*7
        num_flowers_list=[0]*7
        num_bloomed=0
        x_coors=list(range(0,285,15))

        self.flowerid=1
        self.congratsLabel.element.text=''

#class for instruction
class Instruction(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(Instruction,self).__init__()

        #Draw Instruction board
        self.test=cocos.sprite.Sprite('assets/img/test.png')
        self.test.position=(480,300)
 #       self.test.image_anchor=0,0
        self.add(self.test)

        #Draw Go Back Button
        self.button=cocos.sprite.Sprite('assets/img/gobackbutton.png')
        self.button.position=(850,80)
        self.add(self.button)


    def on_mouse_press(self, x, y, buttons, modifiers):
        # This next line seems a bit odd, and that's because it is!
        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)
        print(self.position_x)
        print(self.position_y)
        if ((840 < self.position_x <860 ) and (70 < self.position_y < 90) ):
            clicksound.play()
            menuLayer_back = MultiplexLayer(MainMenus())
            main_menu_scene = cocos.scene.Scene(scroller_menu,menuLayer_back)
            director.replace(FadeTransition(main_menu_scene, duration=1))

#class for credits
class Credits(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(Credits,self).__init__()

        #Draw Instruction board
        self.test=cocos.sprite.Sprite('assets/img/credits.png')
        self.test.position=(480,300)
        self.add(self.test)

        #Draw Go Back Button
        self.button=cocos.sprite.Sprite('assets/img/gobackbutton.png')
        self.button.position=(850,80)
        self.add(self.button)

        #Draw Chris
        self.chris = cocos.sprite.Sprite('assets/img/chris.png')
        self.chris.position=(690,400)
        self.chris.scale=0.6
        self.chris.do(Repeat(RotateBy(10,0.2) + RotateBy(-10,0.2)))
        self.add(self.chris)
        self.chris_name = cocos.sprite.Sprite('assets/img/chris_name.png')
        self.chris_name.position=(690,340)
 #       self.chris_name.do(Repeat(RotateBy(-10,0.2) + RotateBy(10,0.2)))
        self.add(self.chris_name)

        #Draw Sherry
        self.sherry = cocos.sprite.Sprite('assets/img/sherry.png')
        self.sherry.position=(238,400)
        self.sherry.scale=0.6
        self.sherry.do(Repeat(RotateBy(10,0.2) + RotateBy(-10,0.2)))
        self.add(self.sherry)
        self.sherry_name = cocos.sprite.Sprite('assets/img/sherry_name.png')
        self.sherry_name.position=(238,340)
 #       self.sherry_name.do(Repeat(RotateBy(-10,0.2) + RotateBy(10,0.2)))
        self.add(self.sherry_name)

        #Draw Hening
        self.hening = cocos.sprite.Sprite('assets/img/hening.png')
        self.hening.position=(467,400)
        self.hening.scale=0.6
        self.hening.do(Repeat(RotateBy(10,0.2) + RotateBy(-10,0.2)))
        self.add(self.hening)
        self.hening_name = cocos.sprite.Sprite('assets/img/hening_name.png')
        self.hening_name.position=(467,340)
 #       self.hening_name.do(Repeat(RotateBy(-10,0.2) + RotateBy(10,0.2)))
        self.add(self.hening_name)

        #Draw Jordan
        self.jordan = cocos.sprite.Sprite('assets/img/jordan.png')
        self.jordan.position=(398,273)
        self.jordan.scale=0.57
        self.jordan.do(Repeat(RotateBy(10,0.2) + RotateBy(-10,0.2)))
        self.add(self.jordan)
        self.jordan_name = cocos.sprite.Sprite('assets/img/jordan_name.png')
        self.jordan_name.position=(540,262)
 #       self.jordan_name.do(Repeat(RotateBy(-10,0.2) + RotateBy(10,0.2)))
        self.add(self.jordan_name)

        #Draw logo
        self.logo = cocos.sprite.Sprite('assets/img/logo.png')
        self.logo.position=(400,145)
        self.logo.scale=0.55
        self.logo.do(Repeat(RotateBy(10,0.2) + RotateBy(-10,0.2)))
        self.add(self.logo)
        self.logo_name = cocos.sprite.Sprite('assets/img/logo_name.png')
        self.logo_name.position=(540,145)
 #       self.logo_name.do(Repeat(RotateBy(-10,0.2) + RotateBy(10,0.2)))
        self.add(self.logo_name)


    def on_mouse_press(self, x, y, buttons, modifiers):
        # This next line seems a bit odd, and that's because it is!
        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)
        print(self.position_x)
        print(self.position_y)
        if ((840 < self.position_x <860 ) and (70 < self.position_y < 90) ):
            clicksound.play()
            menuLayer_back = MultiplexLayer(MainMenus())
            main_menu_scene = cocos.scene.Scene(scroller_menu,menuLayer_back)
            director.replace(FadeTransition(main_menu_scene, duration=1))




main_scene = cocos.scene.Scene()
main_scene.add(scroller)
main_scene.add(InputVoice())
scroller_instruction = ScrollingManager()
scroller_instruction.add(mapLayer_menu)
instruction_scene = cocos.scene.Scene()
instruction_scene.add(scroller_instruction)
instruction_scene.add(Instruction())

credits_scene = cocos.scene.Scene()
credits_scene.add(scroller_instruction)
credits_scene.add(Credits())

#class for the main menu
class MainMenus(Menu):
    def __init__(self):
        global audiomixer, clicksound, bgmplayed
        super(MainMenus, self).__init__("  ")
        if (bgmplayed == False):
            self.bgm=audiomixer.Sound('game music.ogg')
            self.bgm.play(-1)
            bgmplayed=True

        pyglet.font.add_directory('.')
        self.font_title['font_size'] = 50
 #       self.menu_valign = CENTER+100
#        self.menu_halign = CENTER+300

##        self.background=cocos.sprite.Sprite('assets/img/map_garden_back.png')
##        self.background.position = (10,10)
##        self.add(self.background.position,z=0)
 #       self.menu_hmargin = 200
 #       self.menu_vmargin = 10
        self.font_title = {
            'text': 'title',
            'font_name': 'Arial',
            'font_size': 56,
            'color': (192, 192, 192, 255),
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'dpi': 96,
            'x': 100, 'y': 200,
        }
        self.font_item = {
            'font_name': 'Comic Sans MS',
            'font_size': 28,
            'bold': True,
            'italic': False,
            'anchor_y': "center",
            'anchor_x': "center",
            'color': (57, 34, 3, 255),
            'dpi': 96,
        }
        self.font_item_selected = {
            'font_name': 'Comic Sans MS',
            'font_size': 35,
            'bold': True,
            'italic': False,
            'anchor_y': "center",
            'anchor_x': "center",
            'color': (57, 34, 3, 255),
            'dpi': 96,
        }

        items = []
        items.append(MenuItem("        Start Game", self.on_new_game))
        items.append(MenuItem("        Instruction", self.on_instruction))
        items.append(MenuItem("        Credits", self.on_credits))
        items.append(MenuItem("        Exit", self.on_exit))
        items.append(MenuItem("            ", self.on_ignore))
        items.append(MenuItem("            ", self.on_ignore))

        self.create_menu(items, shake(), shake_back())

    def on_new_game(self):
 #       director.set_scene(main_scene)
        clicksound.play()
        time.sleep(0.5)
        audiomixer.pause()
        director.replace(FadeTransition(main_scene, duration=2))

    def on_instruction(self):
        print("To instruction")
        clicksound.play()
        director.replace(FadeTransition(instruction_scene, duration=1))
 #       self.parent.switch_to(2)

    def on_credits(self):
        clicksound.play()
        print("To cedits")
        director.replace(FadeTransition(credits_scene, duration=1))
 #       self.parent.switch_to(1)

    def on_ignore(self):
        pass

    def on_quit(self):
        clicksound.play()
        director.pop()

#class for the gameend menu
class GameEnd(Menu):
    def __init__(self, game):
        global audiomixer, clicksound
        # call superclass with the title
        super(GameEnd, self).__init__(" ")
        self.game=game
        pyglet.font.add_directory('.')
        self.font_title['font_size'] = 50

        self.font_item = {
           'font_name': 'Comic Sans MS',
           'font_size': 28,
           'bold': True,
           'italic': False,
           'anchor_y': "center",
           'anchor_x': "center",
           'color': (57, 34, 3, 255),
           'dpi': 96,
        }
        self.font_item_selected = {
           'font_name': 'Comic Sans MS',
           'font_size': 35,
           'bold': True,
           'italic': False,
           'anchor_y': "center",
           'anchor_x': "center",
           'color': (57, 34, 3, 255),
           'dpi': 96,
        }

        items = []
        items.append(MenuItem('     Save Data    ', self.on_save_data))
        items.append(MenuItem('      Replay      ', self.on_restart))
        items.append(MenuItem('       Quit       ', self.on_quit_game))

        self.create_menu(items, shake(), shake_back())

    def on_save_data(self):
        clicksound.play()
        #use bar plot to plot flower color
        num_list=num_flowers_list
        flower_list=['purple','blue','cyan','orange','pink','yellow','white']
        barlist=plt.bar(range(len(num_list)),num_list,tick_label=flower_list)
        barlist[0].set_color('#efd2f8')
        barlist[1].set_color('#cdf6ff')
        barlist[2].set_color('#cbf3d4')
        barlist[3].set_color('#ffb788')
        barlist[4].set_color('#ffbcbc')
        barlist[5].set_color('#ffecbe')
        barlist[6].set_color('#fffbfb')
        plt.savefig('output data/flower.png')

        #plot volume

    def on_restart(self):
        clicksound.play()
        #go back to main scene
        time.sleep(0.5)
        director.replace(FadeTransition(main_scene, duration=1))
        audiomixer.pause()
        self.game.reset()

    def on_quit_game(self):
        clicksound.play()
        time.sleep(0.5)
        director.pop()

def main():
    #scene for the main game
    menuLayer = MultiplexLayer(MainMenus())
    scene = cocos.scene.Scene(scroller_menu,menuLayer)
    director.run(scene)

if __name__=="__main__":
    main()
