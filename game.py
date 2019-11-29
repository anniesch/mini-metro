from graphics import *
import enum
import time
import random

WINDOW_SIZE = 700
MARGIN = 50
colors = ['red', 'blue', 'green', 'brown', 'yellow', 'purple', \
			'magenta', 'cyan', 'maroon', 'aquamarine', 'orange', \
			'teal', 'gray']
			# black is kinda useless
TRAIN_LENGTH = 50
TRAIN_WIDTH = 25
LINE_WIDTH = 3 # how thick for the line
SPEED = 10
SLEEP = 0.001
STATION_LIMIT = 3

class Station(int, enum.Enum):
	Empty = 0
	Triangle = 1
	Circle = 2
	Square = 3

def buildText(window, block_size, tracks, t, c, s):
	x = MARGIN
	y = MARGIN
	if len(tracks) != 0:
		x_coor = tracks[0][0]
		y_coor = tracks[0][1]
		x = MARGIN + block_size*x_coor
		y = MARGIN + block_size*y_coor
	text = ''
	if STATION_LIMIT >= 1:
		text += 'T: ' + str(t)
	if STATION_LIMIT >= 2:
		text += '    C: ' + str(c)
	if STATION_LIMIT >= 3:
		text += '\nS: ' + str(s)
	textG = Text(Point(x, y), text)
	textG.setSize(8)
	textG.setStyle('bold')
	textG.draw(window)
	return textG
	

# [(0, 0), (0, 1), (1, 1)] would become [(0, 0), (0, 1), (1, 1), (0, 1)]
# to make it easier to loop back around
def createLine(tracks):
	line = [tracks[i] for i in range(len(tracks))]
	for i in range(1, len(tracks) - 1):
		line.append(tracks[len(tracks) - 1 - i])
	return line

def colorTracks(window, tracks, block_size, color_ind):
	drawnTracks = []
	for i in range(len(tracks) - 1):
		start = tracks[i]
		end = tracks[i + 1]
		x1 = MARGIN + start[0]*block_size
		y1 = MARGIN + start[1]*block_size
		x2 = MARGIN + end[0]*block_size
		y2 = MARGIN + end[1]*block_size
		track = Line(Point(x1+color_ind, y1+color_ind), Point(x2+color_ind, y2+color_ind))
		track.setWidth(LINE_WIDTH)
		track.setOutline(colors[color_ind])
		track.draw(window)
		drawnTracks.append(track)
	return drawnTracks

def createTrain(window, tracks, block_size, i):
	x = MARGIN
	y = MARGIN
	if len(tracks) != 0:
		x_coor = tracks[0][0]
		y_coor = tracks[0][1]
		x = MARGIN + block_size*x_coor
		y = MARGIN + block_size*y_coor
	a = Point(x - TRAIN_LENGTH/2, y - TRAIN_WIDTH/2)
	b = Point(x + TRAIN_LENGTH/2, y - TRAIN_WIDTH/2)
	c = Point(x + TRAIN_LENGTH/2, y + TRAIN_WIDTH/2)
	d = Point(x - TRAIN_LENGTH/2, y + TRAIN_WIDTH/2)
	train = Polygon(a, b, c, d)
	train.setFill(colors[i])
	train.draw(window)
	return train

def createHeader(window):
	h = Text(Point(WINDOW_SIZE + 200, 50), 'Information of Lines')
	h.setSize(20)
	h.setStyle('bold')
	h.draw(window)

def textForTextBox(color_ind, t, c, s):
	text = colors[color_ind] + ' Line (' + str(color_ind) + '):     '
	if STATION_LIMIT >= 1:
		text += 'T: ' + str(t)
	if STATION_LIMIT >= 2:
		text += '      C: ' + str(c)
	if STATION_LIMIT >= 3:
		text += '      S: ' + str(s)
	return text

def buildTextBoxes(window, trains):
	textBoxes = []
	for l in trains:
		text = textForTextBox(trains[l].color_ind, trains[l].num_t, \
								trains[l].num_c, trains[l].num_s)
		cur = Text(Point(WINDOW_SIZE + 150, 80 + l*20), text)
		cur.setTextColor(colors[trains[l].color_ind])
		cur.draw(window)
		textBoxes.append(cur)
	return textBoxes

class Sideline:
	def __init__(self, window, trains={}):
		self.trains = trains
		self.window = window
		self.textBoxes = buildTextBoxes(self.window, self.trains)
		createHeader(self.window)

	def updateSideline(self, trains):
		self.trains = trains
		for l in self.textBoxes:
			l.undraw()
		self.textBoxes = buildTextBoxes(self.window, self.trains)

class Train:
	def __init__(self, tracks, color_ind, window, block_size):
		self.window = window
		self.tracks = tracks
		self.block_size = block_size
		self.color_ind = color_ind
		self.train = createTrain(self.window, self.tracks, self.block_size, self.color_ind)
		self.line = createLine(tracks)
		self.curP = 0
		self.curFrac = 0
		self.num_t = 0
		self.num_c = 0
		self.num_s = 0
		self.drawnTracks = colorTracks(self.window, self.tracks, self.block_size, self.color_ind)
		self.text = buildText(self.window, self.block_size, self.tracks, self.num_t, self.num_c, self.num_s)

	def reset(self):
		self.curP = 0
		self.curFrac = 0
		self.num_t = 0
		self.num_c = 0
		self.num_s = 0
		self.train.undraw()
		self.train = createTrain(self.window, self.tracks, self.block_size, self.color_ind)
		self.text.undraw()
		self.text = buildText(self.window, self.block_size, self.tracks, self.num_t, self.num_c, self.num_s)

	def updateTracks(self, tracks):
		self.tracks = tracks
		self.line = createLine(tracks)
		for t in self.drawnTracks:
			t.undraw()
		self.drawnTracks = colorTracks(self.window, self.tracks, self.block_size, self.color_ind)
		self.reset()

	def moveTrain(self, dist, curX, curY, nextX, nextY):
		if curX + 1 == nextX and curY == nextY:
			self.train.move(dist, 0)
			self.text.move(dist, 0)
		elif curX - 1 == nextX and curY == nextY:
			self.train.move(-dist, 0)
			self.text.move(-dist, 0)
		elif curY + 1 == nextY and curX == nextX:
			self.train.move(0, dist)
			self.text.move(0, dist)
		elif curY - 1 == nextY and curX == nextX:
			self.train.move(0, -dist)
			self.text.move(0, -dist)
		else:
			raise Exception('Wrong Coordinates')
		
	def move(self):
		if self.curFrac != SPEED:
			self.moveTrain(self.block_size/SPEED, \
						self.line[self.curP][0], self.line[self.curP][1], \
						self.line[(self.curP + 1) % len(self.line)][0], \
						self.line[(self.curP + 1) % len(self.line)][1])
			self.curFrac += 1
		else:
			self.curP = (self.curP + 1) % len(self.line)
			self.moveTrain(self.block_size/SPEED, \
						self.line[self.curP][0], self.line[self.curP][1], \
						self.line[(self.curP + 1) % len(self.line)][0], \
						self.line[(self.curP + 1) % len(self.line)][1])
			self.curFrac = 1


class AllTrains:
	def __init__(self, window, block_size, trains={}, trainColors = set()):
		self.window = window
		self.block_size = block_size
		self.trains = trains
		self.trainColors = trainColors
		self.sideline = Sideline(self.window, self.trains)
		self.allColors = set([i for i in range(len(colors))])
		self.stations = {}
	# (x_coor, y_coor) refers to (0, 0) or (1, 2) and this function 
	# figures out the actual pixel values
	def addStation(self, x_coor, y_coor, station):
		x = MARGIN + self.block_size*x_coor
		y = MARGIN + self.block_size*y_coor
		if station == Station.Triangle:
			t = Polygon(Point(x, y-10), Point(x-10, y+10), Point(x+10, y+10))
			t.setFill('red')
			t.draw(self.window)
			self.stations[(x_coor, y_coor)] = Station.Triangle
		elif station == Station.Circle:
			c = Circle(Point(x,y), 10)
			c.setFill('blue')
			c.draw(self.window)
			self.stations[(x_coor, y_coor)] = Station.Circle
		elif station == Station.Square:
			s = Rectangle(Point(x-10, y-10), Point(x+10, y+10))
			s.setFill('green')
			s.draw(self.window)
			self.stations[(x_coor, y_coor)] = Station.Square
		else:
			raise Exception('Wrong Station Type')

	def resetLines(self):
		for i in self.trains:
			self.trains[i].reset()

	def randNewColor(self): # based on remaining colors
		remColors = self.allColors - self.trainColors
		curColor = random.choice(list(remColors))
		return curColor

	def createNewLine(self, tracks, i=None):
		if i in self.allColors:
			if i in self.trainColors:
				raise Exception('AllTrains: ' + colors[i] + ' Line (' + str(i) + ') already in use')
			curTrain = Train(tracks, i, self.window, self.block_size)
			self.trainColors.add(i)
			self.trains[i] = curTrain
			self.sideline.updateSideline(self.trains)
			self.resetLines()
		elif i == None and len(self.trains) < len(colors):
			curColor = self.randNewColor()
			curTrain = Train(tracks, curColor, self.window, self.block_size)
			self.trainColors.add(curColor)
			self.trains[curColor] = curTrain
			self.sideline.updateSideline(self.trains)
			self.resetLines()
		else:
			raise Exception('AllTrains: Max Lines have been reached')

	def removeLine(self, i):
		if i in self.trainColors:
			self.trainColors.remove(i)
			del self.trains[curColor]
			self.sideline.updateSideline(self.trains)
			self.resetLines()
		else:
			raise Exception('AllTrains: Line does not exist')

	def move(self):
		for i in self.trains:
			self.trains[i].move()

	def updateTracks(self, tracks, i):
		self.trains[i].updateTracks(tracks)
		self.sideline.updateSideline(self.trains)
		self.resetLines()




def loadGrid(window, n):
	outer_grid = Rectangle(Point(MARGIN, MARGIN), \
		Point(WINDOW_SIZE - MARGIN, WINDOW_SIZE - MARGIN))
	outer_grid.draw(window)
	block_size = (WINDOW_SIZE - 2*MARGIN)/n
	for i in range(1, n):
		cur_h = Line(Point(MARGIN, MARGIN + i*block_size), Point(WINDOW_SIZE - MARGIN, MARGIN + i*block_size))
		cur_v = Line(Point(MARGIN + i*block_size, MARGIN), Point(MARGIN + i*block_size, WINDOW_SIZE - MARGIN))
		cur_h.draw(window)
		cur_v.draw(window)
	return block_size

def main():
	window = GraphWin("MiniMetro", WINDOW_SIZE + 400, WINDOW_SIZE)
	block_size = loadGrid(window, 4)
	allTrains = AllTrains(window, block_size)
	allTrains.addStation(0, 2, Station.Circle)
	allTrains.addStation(1, 3, Station.Triangle)
	allTrains.addStation(2, 1, Station.Square)
	print(allTrains.stations)
	tracks = [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]
	tracks2 = [(1, 1), (2, 1), (2, 0), (3, 0), (3, 1)]
	allTrains.createNewLine(tracks, 5)
	allTrains.createNewLine(tracks2, 6)
	for i in range(200):
		# time.sleep(SLEEP)
		allTrains.move()
	allTrains.updateTracks([(0, 0), (1, 0), (2, 0), (2, 1)], 5)
	count = 0
	while(True):
		# time.sleep(SLEEP/len(trains))
		# train.move()
		# train2.move()
		allTrains.move()
		count += 1
		if count % 200 == 0 and len(allTrains.trainColors) < len(colors):
			allTrains.createNewLine(tracks)
			allTrains.removeLine()
	window.close()    # Close window when done


if __name__ == '__main__':
	main()
