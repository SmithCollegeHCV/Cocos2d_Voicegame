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

from pyglet.window.key import symbol_string


global WIDTH, HEIGHT
WIDTH=375
HEIGHT=660
class Bullet(cocos.layer.Layer):

	def __init__(self, x, y):
		super(Bullet, self).__init__()
		self.bullet=cocos.sprite.Sprite('assets2/bullet.png')
		self.bullet.scale_y=0.03
		self.bullet.scale_x=0.03
		self.bullet.image_anchor=0,0
		self.bullet.position=x+(62.5-self.bullet.width/2), y+50
		self.bullet.do(MoveBy((0,600),3))
		self.add(self.bullet)




class Spaceship(cocos.layer.Layer):
	is_event_handler=True

	def __init__(self):
		super(Spaceship,self).__init__()
		self.CHUNK=1024
		self.RATE=44100

        #init voice input
		p=pyaudio.PyAudio()

        #Open stream
		self.stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        # Aubio's pitch detection
		self.pDetection = aubio.pitch("default", self.CHUNK*2, self.CHUNK, self.RATE)

        #Set unit.
		self.pDetection.set_unit("Hz")
		self.pDetection.set_silence(-40)

		self.bullets=cocos.cocosnode.CocosNode()
		self.add(self.bullets)

        #Draw spaceship
		self.spaceship=cocos.sprite.Sprite('assets2/sapceship.png')
		self.spaceship.scale_y=0.25
		self.spaceship.scale_x=0.25
		self.spaceship.image_anchor=0,0
		self.spaceship.position=375/2-self.spaceship.width/2, 30
		self.add(self.spaceship)


		self.schedule(self.update)

	def on_key_press(self, key, modifiers):
		move_left=MoveBy((-20,0),0.5)

		if self.spaceship.x>=0+20-self.spaceship.width/2 and symbol_string(key) == "LEFT":
			self.spaceship.do(move_left)
		if self.spaceship.x<=375-20-self.spaceship.width/2 and symbol_string(key) == "RIGHT":
			self.spaceship.do(Reverse(move_left))

	def update(self,dt):
		data = self.stream.read(self.CHUNK,exception_on_overflow = False)
		sample = np.fromstring(data, dtype=aubio.float_type)
		pitch=self.pDetection(sample)[0]
		volume=np.sum(sample**2)/len(sample)
		if(volume > 0.0002):
			new_bullet=Bullet(self.spaceship.x, self.spaceship.y)
			self.bullets.add(new_bullet)

def main():
	#scroller for testing background
	director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=False)
	scroller = ScrollingManager()
	mapLayer = load("assets2/map/background.tmx")["Tile Layer 1"]
	scroller.add(mapLayer)
	main_scene = cocos.scene.Scene(scroller, Spaceship())
	director.run(main_scene)

if __name__=="__main__":
	main()