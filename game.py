#package for audio
import pyaudio
import aubio
import numpy as np

#package for game
import cocos
from cocos.director import director
from cocos.actions import *

#class for nutrition
class NutritionBar(cocos.layer.Layer):

    def __init__(self):
        super(NutritionBar,self).__init__()

        #Draw nutritionbar
        self.nutritionbar=cocos.sprite.Sprite('NutritionBar.png')
        self.nutritionbar.scale_y=0.2
        self.nutritionbar.scale_x=0.2
        self.nutritionbar.position=320-self.nutritionbar.width/2,260
        self.nutritionbar.image_anchor=0,0
        self.add(self.nutritionbar)

        #Draw nutritionicon
        self.nutritionicon=cocos.sprite.Sprite('NutritionIcon.png')
        self.nutritionicon.scale_y=0.0625
        self.nutritionicon.scale_x=0.0625
        self.nutritionicon_initial=300-self.nutritionbar.width/2
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
        self.waterbar.position=320-self.waterbar.width/2,300
        self.add(self.waterbar)


        #Draw watericon
        self.watericon=cocos.sprite.Sprite('WaterIcon.png')
        self.watericon.scale_y=0.02
        self.watericon.scale_x=0.02
        self.watericon_initial=300-self.waterbar.width/2
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
        self.pitchLabel.position=320,240
        self.volumeLabel.position=320,260

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
        self.schedule(self.update)

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass


    def update(self,dt):
        data = self.stream.read(self.CHUNK,exception_on_overflow = False)
        sample = np.fromstring(data, dtype=aubio.float_type)
        pitch=self.pDetection(sample)[0]
        volume=np.sum(sample**2)/len(sample)
        if(volume > 0.0002):
            self.water.set_value(1)
            self.nutrition.set_value(2)
            print(self.water.get_value())
            print(self.water.get_value())

        volume="{:.6f}".format(volume)
        #print(dt)
        self.pitchLabel.element.text='Pitch: '+pitch.astype('str')
        self.volumeLabel.element.text='Volume: '+volume



#class Window(cocos.layer.ColorLayer):

    #def __init__(self):
 #       DIM = (450, 800) #DIMENSIONS
       # super(Window, self).__init__(64,64,224,255)
 #       self.input=InputVoice()


def main():
    director.init(resizable=True)
    main_scene=cocos.scene.Scene(InputVoice())
    director.run(main_scene)

if __name__=="__main__":
    main()
