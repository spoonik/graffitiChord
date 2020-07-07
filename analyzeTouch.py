#! python2

from operator import itemgetter
from consts import root

chord_graffiti = {'10':'m7', '20':'7', '1010':'M7', '01':'m9', '1020':'M9', '11':'dim7', '21':'aug', '2010':'7sus4'}

area = 40
key_width = 100

def get_sabuns(points):
	#points.sort(key=itemgetter(1))
	points.sort()
	sabun = []
	for i in range(len(points)-1):
		sabun.append([points[i][0]-points[i+1][0], points[i][1]-points[i+1][1]])
	return sabun

def convert_sabuns_to_chord_index(sabuns):
	ret = []
	for sabun in sabuns:
		ret.append([abs(int(sabun[0]/(area*2))), abs(int(sabun[1]/(area*2)))])

	text = ''
	for r in ret:
		text = text + str(r[0]) + str(r[1])
	return text

def separate_base_and_chord(points):
	base_point = None
	chord_points = []
	for p in points:
		if p[0] < key_width:
			base_point = p
		else:
			chord_points.append(p)
	return base_point, chord_points

def get_base_name(p, height):
	if p == None:
		return None
	y = height - p[1]
	key_idx = int(y / (height/len(root)))
	return root[key_idx]

def get_chord_pattern(points, height):
	if len(points) == 0:
		return None, None
	base_point, chord_point = separate_base_and_chord(points)
	base = get_base_name(base_point, height)
	sabuns = get_sabuns(chord_point)
	idx = convert_sabuns_to_chord_index(sabuns)
	return base, chord_graffiti.get(idx)
