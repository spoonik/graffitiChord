#! python2

import ui
from midiutil.MidiFile import MIDIFile
from consts import chordstyle, keys, midikeys, midibass, root, outputfile
import sound, time
import threading
import datetime

class PlayMidiThread(threading.Thread):
	def __init__(self, n, t):
		super(PlayMidiThread, self).__init__()
		self.n = n
		self.t = t
	def run(self):
		sound.stop_all_effects()
		player = sound.MIDIPlayer(outputfile)
		player.play()
		time.sleep(1)

def play_chord_midi(r, s):
	midi = MIDIFile(5)
	midi.addTempo(0, 0, 180)
	midi.addProgramChange(0, 0, 0, 1)
	duration = 1
	tone =[]
	rootpos = root.index(r)
	chord = chordstyle[s]
	for k in chord:
		tone.append((k+rootpos)%12)

	trck = 0
	for k in tone:
		pitch = midikeys[k]
		# track, channel, pitch, time, duration, volume
		midi.addNote(trck, 0, pitch, 0, duration, 100)
		trck+=1
	if len(tone) !=1:
		pitch = midibass[tone[0]]
		midi.addNote(trck, 0, pitch, 0, duration, 100)

	with open(outputfile, 'w') as f:
		midi.writeFile(f)

	th_cl = PlayMidiThread(5, 5)
	th_cl.start()
