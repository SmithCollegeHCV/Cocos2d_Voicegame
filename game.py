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

global WIDTH, HEIGHT, num_pitches, prev_pitch, flowers
WIDTH=960
HEIGHT=568
num_pitches=0
prev_pitch=0
flowers=list()

#class for flower
class Flower(cocos.layer.Layer):

    def __init__(self, filename):
        global flowers
        super(Flower,self).__init__()

        #Draw flower
        self.flower=cocos.sprite.Sprite(filename)
        self.flower.scale_y=0.01
        self.flower.scale_x=0.01
        self.flower.position=random.randrange(HEIGHT),random.randrange(int(HEIGHT/3))
        self.flower.image_anchor=0,0
        self.water=0
        self.nutrition=0
        self.add(self.flower)

#class for nutrition
class NutritionBar(cocos.layer.Layer):

    def __init__(self):
        super(NutritionBar,self).__init__()

        #Draw nutritionbar
        self.nutritionbar=cocos.sprite.Sprite('NutritionBar.png')
        self.nutritionbar.scale_y=0.2
        self.nutritionbar.scale_x=0.2
        self.nutritionbar.position=790-self.nutritionbar.width/2,260
        self.nutritionbar.image_anchor=0,0
        self.add(self.nutritionbar)

        #Draw nutritionicon
        self.nutritionicon=cocos.sprite.Sprite('NutritionIcon.png')
        self.nutritionicon.scale_y=0.0625
        self.nutritionicon.scale_x=0.0625
        self.nutritionicon_initial=770-self.nutritionbar.width/2
        self.nutritionicon.position=self.nutritionicon_initial,275
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
            print(self.nutritionicon.x)
            self.nutritionicon.x+=speed
        else:
            self.reset()

    def reset(self):
        self.speed=0
        self.nutritionicon.position=self.nutritionicon_initial,275

#class for water
class WaterBar(cocos.layer.Layer):

    def __init__(self):
        super(WaterBar,self).__init__()

        #Draw waterbar
        self.waterbar=cocos.sprite.Sprite('WaterBar.png')
        self.waterbar.scale_y=0.2
        self.waterbar.scale_x=0.2
        self.waterbar.image_anchor=0,0
        self.waterbar.position=790-self.waterbar.width/2,300
        self.add(self.waterbar)


        #Draw watericon
        self.watericon=cocos.sprite.Sprite('WaterIcon.png')
        self.watericon.scale_y=0.02
        self.watericon.scale_x=0.02
        self.watericon_initial=770-self.waterbar.width/2
        self.watericon.position=self.watericon_initial,315
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
            print(self.watericon.x)
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
        self.pitchLabel.position=780,100
        self.volumeLabel.position=780,140

        self.add(self.pitchLabel)
        self.add(self.volumeLabel)

        #init voice input
        p=pyaudio.PyAudio()

        #Open stream
        self.stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        # Aubio's pitch detection
        self.pDetection = aubio.pitch("default", self.CHUNK*2, self.CHUNK, self.RATE)

        #Set unit.
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-40)

        #get water
        self.water=WaterBar()
        self.add(self.water)


        #add nutrition
        self.nutrition=NutritionBar()
        self.add(self.nutrition)

        #add flower
        self.flower=Flower('NutritionIcon.png')
        flowers.append(self.flower)
        self.add(self.flower)

        self.schedule(self.update)

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass


    def update(self,dt):
        global num_pitches, prev_pitch, flowers
        data = self.stream.read(self.CHUNK,exception_on_overflow = False)
        sample = np.fromstring(data, dtype=aubio.float_type)
        pitch=self.pDetection(sample)[0]
        volume=np.sum(sample**2)/len(sample)
        if ((abs(pitch-prev_pitch) > 200) and (pitch > 50)):
            num_pitches+=1
            if (num_pitches>20):
                num_pitches=0
                new_flower=Flower('NutritionIcon.png')
                flowers.append(new_flower)
                self.add(new_flower)
        prev_pitch = pitch
        if(volume > 0.0002):
            self.water.set_value(1)
            self.nutrition.set_value(2)
            # print(self.water.get_value())
            # print(self.water.get_value())
            n=len(flowers)
            for i in range(n):
                flower=flowers[i]
                flower.water+=1/n
                flower.nutrition+=2/n
                if ((flower.water > 1) and (flower.nutrition > 1)):
                    new_flower=Flower('WaterIcon.png')
                    new_flower.flower.position=flower.flower.position
                    new_flower.water=flower.water
                    new_flower.nutrition=flower.nutrition
                    self.remove(flower)
                    self.add(new_flower)
                    flowers[i]=new_flower
                    print(n)

        volume="{:.6f}".format(volume)
        #print(dt)
        self.pitchLabel.element.text='Pitch: '+pitch.astype('str')
        self.volumeLabel.element.text='Volume: '+volume



def main():
    director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=True)
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
