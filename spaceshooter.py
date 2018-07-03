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

class Spaceship(cocos.layer.Layer):
	is_event_handler=True

	def __init__(self):
		super(Spaceship,self).__init__()
		self.spaceship=cocos.sprite.Sprite('assets2/sapceship.png')
		self.spaceship.scale_y=0.25
		self.spaceship.scale_x=0.25
		self.spaceship.image_anchor=0,0
		self.spaceship.position=375/2-self.spaceship.width/2, 30
		self.add(self.spaceship)

	def on_key_press(self, key, modifiers):
		move_left=MoveBy((-20,0),0.5)

		if self.spaceship.x>=0+20-self.spaceship.width/2 and symbol_string(key) == "LEFT":
			self.spaceship.do(move_left)
		if self.spaceship.x<=375-20-self.spaceship.width/2 and symbol_string(key) == "RIGHT":
			self.spaceship.do(Reverse(move_left))

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