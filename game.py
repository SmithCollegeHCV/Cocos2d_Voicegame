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

global WIDTH, HEIGHT, num_pitches, flowers, x_coors, num_bloomed, num_flowers, flower_under_mouse
WIDTH=960
HEIGHT=568
num_pitches=[0]*7
flowers=list()
x_coors=list(range(0,285,15))
num_bloomed=0
num_flowers=19
flower_under_mouse=None

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
        self.nutritionicon.position=self.nutritionicon_initial+flower.nutrition,275
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
        else:
            self.reset()

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
        self.watericon.position=self.watericon_initial+flower.water,315
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
        else:
            self.reset()

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

        self.pitchLabel.position=780,100
        self.volumeLabel.position=780,140
        self.plantLabel.position=780,480
        self.bloomLabel.position=780,440
        self.colorLabel.position=780,400

        self.add(self.pitchLabel)
        self.add(self.volumeLabel)
        self.add(self.plantLabel)
        self.add(self.bloomLabel)
        self.add(self.colorLabel)

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
        self.flowerid=1
        self.flower=Flower(self.flowerid,'ui/white.png')
        self.colorLabel.element.text='Color of the newest flower: white'
        flowers.append(self.flower)
        self.add(self.flower)

        self.water=WaterBar(self.flower)
        self.nutrition=NutritionBar(self.flower)

        self.schedule(self.update)

    def on_mouse_motion(self, x, y, dx, dy):
        global flowers, flower_under_mouse
        x,y=director.get_virtual_coordinates(x,y)
        if (flower_under_mouse != None):
            position_x,position_y=flower_under_mouse.position
            if (flower_under_mouse.stage4):
                dx1=2
                dx2=18
                dy1=1
                dy2=20
            elif (flower_under_mouse.stage5):
                dx1=2
                dx2=20
                dy1=1
                dy2=30
            elif (flower_under_mouse.stage6):
                dx1=8
                dx2=27
                dy1=0
                dy2=58
            elif (flower_under_mouse.stage7):
                dx1=8
                dx2=27
                dy1=0
                dy2=59
            else:
                dx1=5
                dx2=15
                dy1=0
                dy2=15
            if (not ((position_x+dx1 < x/2 < position_x+dx2) and (position_y+dy1 < y/2 < position_y+dy2))):
                flower_under_mouse=None
                self.remove(self.water)
                self.remove(self.nutrition)
        else:
            for flower in flowers:
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
                if ((position_x+dx1 < x/2 < position_x+dx2) and (position_y+dy1 < y/2 < position_y+dy2)):
                    flower_under_mouse=flower
            if (flower_under_mouse != None):
                self.water=WaterBar(flower_under_mouse)
                self.nutrition=NutritionBar(flower_under_mouse)
                self.add(self.water)
                self.add(self.nutrition)

    # def on_mouse_press(self, x, y, buttons, modifiers):

    def update(self,dt):
        global num_pitches, flowers, x_coors, num_bloomed, num_flowers
        if (num_bloomed < num_flowers):
            data = self.stream.read(self.CHUNK,exception_on_overflow = False)
            sample = np.fromstring(data, dtype=aubio.float_type)
            pitch=self.pDetection(sample)[0]
            volume=np.sum(sample**2)/len(sample)
            num_pitch=50

            if (0 < pitch < 200):
                num_pitches[0]+=1
                if ((num_pitches[0]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/purple.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: purple'
            elif (200 <= pitch < 250):
                num_pitches[1]+=1
                if ((num_pitches[1]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/blue.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: blue'
            elif (250 <= pitch < 300):
                num_pitches[2]+=1
                if ((num_pitches[2]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/cyan.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: cyan'
            elif (300 <= pitch < 400):
                num_pitches[3]+=1
                if ((num_pitches[3]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/orange.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: orange'
            elif (400 <= pitch < 600):
                num_pitches[4]+=1
                if ((num_pitches[4]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/pink.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: pink'
            elif (600 <= pitch < 1200):
                num_pitches[5]+=1
                if ((num_pitches[5]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/yellow.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: yellow'
            elif (pitch >= 1200):
                num_pitches[6]+=1
                if ((num_pitches[6]%num_pitch == 0) and (len(x_coors) > 0)):
                    print(self.flowerid)
                    self.flowerid+=1
                    new_flower=Flower(self.flowerid,'ui/white.png')
                    flowers.append(new_flower)
                    self.add(new_flower)
                    self.colorLabel.element.text='Color of the newest flower: white'

            if(volume > 0.0002):
                n=len(flowers)
                num_bloomed=0
                for flower in flowers:
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
            self.plantLabel.element.text='Number of flowers planted: '+str(len(flowers))
            self.bloomLabel.element.text='Number of flowers bloomed: '+str(num_bloomed)
            if (num_bloomed == num_flowers):
                self.remove(self.pitchLabel)
                self.remove(self.volumeLabel)
                self.remove(self.colorLabel)
                self.congratsLabel=cocos.text.Label('Congratulations!',
                                                  font_name='Times New Roman',
                                                  font_size=36,
                                                  anchor_x='center', anchor_y='center')
                self.congratsLabel.position=780,200
                self.add(self.congratsLabel)

def main():
    director.init(width=WIDTH, height=HEIGHT, resizable=False, autoscale=False)
    scroller = ScrollingManager()
    #mapLayer = TmxObjectLayer("map_garden_back.tmx")
    mapLayer = load("assets/map/map_garden_back_01.tmx")["TileLayer1"]
    scroller.add(mapLayer)
    #scroller.add(NutritionBar())
    #scroller.add(WaterBar())
    main_scene = cocos.scene.Scene()
    main_scene.add(scroller)
    main_scene.add(InputVoice())
 #   main_scene=cocos.scene.Scene(BackGround())
    director.run(main_scene)

if __name__=="__main__":
    main()
