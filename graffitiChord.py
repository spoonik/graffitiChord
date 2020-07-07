#! python2

from scene import *
from colorsys import hsv_to_rgb
from random import random
import sound, time
import analyzeTouch
from playMIDI import play_chord_midi

area = 40
key_width = 100

class TouchColors (Scene):
	current_chord = None

	def setup(self):
		self.touch_colors = {}

	def draw(self):
		background(0, 0, 0)
		self.draw_keyboard()
		for touch in self.touches.values():
			r, g, b = self.touch_colors[touch.touch_id]
			fill(r, g, b)
			ellipse(touch.location.x - area, touch.location.y - area, area*2, area*2)
		self.display_chords_name()

	def draw_keyboard(self):
		height = self.size.h/12

		#stroke(255,255,255)
		for i in range(12):
			if i in [0,2,4,6,7,9,11]:
				fill(255,255,255)
				rect(0, i*height, key_width, height)

	def touch_began(self, touch):
		self.touch_colors[touch.touch_id] = hsv_to_rgb(random(), 1, 1)

	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		del self.touch_colors[touch.touch_id]

	def display_chords_name(self):
		points = []
		for touch in self.touches.values():
			points.append([touch.location.x, touch.location.y])

		base, chord = analyzeTouch.get_chord_pattern(points, self.size.h)
		if base!=None and chord!=None:
			text(base+chord, x=110, y=100)
			if self.current_chord != base+chord:
				self.play_chord(base, chord)
			self.current_chord = base+chord
		elif base!=None and chord==None:
			if self.current_chord != None:
				self.stop_sound()
				return
			text(base, x=110, y=100)
			if self.current_chord != base:
				self.play_chord(base, chord)
			self.current_chord = base
		else:
			self.stop_sound()
			self.current_chord = None

	def play_chord(self, base, chord):
		if base == None:
			return
		elif chord == None:
			play_chord_midi(base, '1')
		else:
			play_chord_midi(base, chord)
		return
		
		#old------
		self.stop_sound()
		if base == None:
			return
		elif chord == None:
			chord_interval = chordstyle.get('1')
		else:
			chord_interval = chordstyle.get(chord)
			if chord_interval == None:
				return
		sounds = []
		base_idx = keys.index(base)
		for i in chord_interval:
			sound_file = 'sound/' + keys[base_idx+i] + '.m4a'
			play_id = sound.play_effect(sound_file)

	def stop_sound(self):
		sound.stop_all_effects()

run(TouchColors())
