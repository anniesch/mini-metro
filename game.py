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
SPEED = 100 # should be like 10
SLEEP = 0.001
STATION_LIMIT = 3
TRAIN_PASSENGER_LIMIT = 100
STATION_PASSENGER_LIMIT = 100

class StationType(int, enum.Enum):
	Empty = 0
	Triangle = 1
	Circle = 2
	Square = 3

def trainText(t, c, s):
	text = ''
	if STATION_LIMIT >= 1:
		text += 'T: ' + str(t)
	if STATION_LIMIT >= 2:
		text += '    C: ' + str(c)
	if STATION_LIMIT >= 3:
		text += '\nS: ' + str(s)
	return text

def buildText(window, block_size, tracks, t, c, s):
	x = MARGIN
	y = MARGIN
	if len(tracks) != 0:
		x_coor = tracks[0][0]
		y_coor = tracks[0][1]
		x = MARGIN + block_size*x_coor
		y = MARGIN + block_size*y_coor
	text = trainText(t, c, s)
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

def stationText(stationType, x, y, t, c, s):
	text = ''
	if stationType == StationType.Triangle:
		text = 'Triangle'
	elif stationType == StationType.Circle:
		text = 'Circle'
	elif stationType == StationType.Square:
		text = 'Square'
	text += ' Station (' + str(x) + ', ' + str(y) + '):     '
	if STATION_LIMIT >= 1:
		text += 'T: ' + str(t)
	if STATION_LIMIT >= 2:
		text += '      C: ' + str(c)
	if STATION_LIMIT >= 3:
		text += '      S: ' + str(s)
	return text

def buildTextBoxes(window, trains, stations):
	textBoxes = []
	for l in trains:
		text = textForTextBox(trains[l].color_ind, trains[l].num_t, \
								trains[l].num_c, trains[l].num_s)
		cur = Text(Point(WINDOW_SIZE + 150, 80 + l*20), text)
		cur.setTextColor(colors[trains[l].color_ind])
		cur.draw(window)
		textBoxes.append(cur)
	if stations != None:
		count = 0
		for key in stations:
			s = stations[key]
			text = stationText(s.station, s.x_coor, s.y_coor, s.n_passengers[0], s.n_passengers[1], s.n_passengers[2])
			cur = Text(Point(WINDOW_SIZE + 150, 360 + count*20), text)
			cur.setTextColor(colors[int(s.station) - 1] )
			cur.draw(window)
			textBoxes.append(cur)
			count += 1
	return textBoxes

class Sideline:
	def __init__(self, window, trains={}, stations=None):
		self.trains = trains
		self.window = window
		self.stations = stations
		self.textBoxes = buildTextBoxes(self.window, self.trains, self.stations)
		createHeader(self.window)

	def updateSideline(self, trains, stations=None):
		self.trains = trains
		self.stations = stations
		for l in self.textBoxes:
			l.undraw()
		self.textBoxes = buildTextBoxes(self.window, self.trains, self.stations)

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
		self.stationsOnLine = {}

	def reset(self):
		self.train.undraw()
		self.train = createTrain(self.window, self.tracks, self.block_size, self.color_ind)
		self.text.undraw()
		self.text = buildText(self.window, self.block_size, self.tracks, self.num_t, self.num_c, self.num_s)

	def updateTracks(self, tracks):
		self.curP = 0
		self.curFrac = 0
		self.tracks = tracks
		self.line = createLine(tracks)
		for t in self.drawnTracks:
			t.undraw()
		self.drawnTracks = colorTracks(self.window, self.tracks, self.block_size, self.color_ind)
		self.num_t = 0
		self.num_c = 0
		self.num_s = 0
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
		self.moveTrain(self.block_size/SPEED, \
					self.line[self.curP][0], self.line[self.curP][1], \
					self.line[(self.curP + 1) % len(self.line)][0], \
					self.line[(self.curP + 1) % len(self.line)][1])
		self.curFrac += 1
		if self.curFrac == SPEED:
			self.curFrac = 0
			self.curP = (self.curP + 1) % len(self.line)

	def updateText(self):
		self.text.undraw()
		self.text.setText(trainText(self.num_t, self.num_c, self.num_s))
		self.text.draw(self.window)

	def addPassengers(self, t, c, s, station):
		if self.num_t + self.num_c + self.num_s + t + c + s <= TRAIN_PASSENGER_LIMIT:
			self.num_t += t
			self.num_c += c
			self.num_s += s
			sType = 'Triangle'
			if station == StationType.Circle:
				sType = 'Circle'
			elif station == StationType.Square:
				sType = 'Square'
			if t == 0 and c == 0 and s == 0:
				print(colors[self.color_ind] + ' Line picked up no passengers at ' + sType + ' station (' + str(self.line[self.curP][0]) + ', ' + str(self.line[self.curP][1]) + ')')
			else:
				print(colors[self.color_ind] + ' Line picked up ' + str(t) + \
					' triangle, ' + str(c) + ' circle, and ' \
					+ str(s) + ' square passengers at ' + sType + ' station (' + str(self.line[self.curP][0]) + ', ' + str(self.line[self.curP][1]) + ')')
		else:
			raise Exception('Exceeded train passenger limit')

	def removePassengers(self, station):
		if station == StationType.Triangle and self.num_t != 0:
			print(colors[self.color_ind] + ' Line dropped off ' + str(self.num_t) + \
				 ' triangle passengers at Triangle station (' + str(self.line[self.curP][0]) + ', ' + str(self.line[self.curP][1]) + ')')
			self.num_t = 0
		elif station == StationType.Circle and self.num_c != 0:
			print(colors[self.color_ind] + ' Line dropped off ' + str(self.num_c) + \
				 ' circle passengers at Circle station (' + str(self.line[self.curP][0]) + ', ' + str(self.line[self.curP][1]) + ')')
			self.num_c = 0
		elif station == StationType.Square and self.num_s != 0:
			print(colors[self.color_ind] + ' Line dropped off ' + str(self.num_s) + \
				 ' square passengers at Square station (' + str(self.line[self.curP][0]) + ', ' + str(self.line[self.curP][1]) + ')')
			self.num_s = 0

	


class Station:
	def __init__(self, x_coor, y_coor, station):
		self.x_coor = x_coor
		self.y_coor = y_coor
		self.station = station
		self.n_passengers = [0, 0, 0] # t, c, s

	def addPassengers(self, t=0, c=0, s=0):
		if t == 0 and c == 0 and s == 0:
			nums = [0, 0, 0]
			for i in range(3):
				if i != int(self.station):
					nums[i] = random.randint(1, 3)
					self.n_passengers[i] += nums[i]

		else:
			if (t == 0 and self.station == StationType.Triangle) or \
				(c == 0 and self.station == StationType.Circle) or \
				(s == 0 and self.station == StationType.Square):
				self.n_passengers[0] += t
				self.n_passengers[1] += c
				self.n_passengers[2] += s
				if self.station == StationType.Triangle:
					print('Triangle Station at (' + str(self.x_coor) + ', ' + str(self.y_coor) + ') added ' \
						+ str(c) + ' circle and ' + str(s) + ' square passengers')
				elif self.station == StationType.Circle:
					print('Circle Station at (' + str(self.x_coor) + ', ' + str(self.y_coor) + ') added ' \
						+ str(t) + ' triangle and ' + str(s) + ' square passengers')
				elif self.station == StationType.Square:
					print('Square Station at (' + str(self.x_coor) + ', ' + str(self.y_coor) + ') added ' \
						+ str(t) + ' triangle and ' + str(c) + ' circle passengers')
			else:
				raise Exception('Tried adding an illegal passenger')

	def removePassengers(self, t, c, s):
		assert t <= self.n_passengers[0] and c <= self.n_passengers[1] and s <= self.n_passengers[2]
		assert t >= 0 and c >= 0 and s >= 0
		if (t == 0 and self.station == StationType.Triangle) or \
			(c == 0 and self.station == StationType.Circle) or \
			(s == 0 and self.station == StationType.Square):
			self.n_passengers[0] -= t
			self.n_passengers[1] -= c
			self.n_passengers[2] -= s
		else:
			raise Exception('Tried removing an illegal passenger')

class AllTrains:
	def __init__(self, window, block_size, trains={}, trainColors = set()):
		self.window = window
		self.block_size = block_size
		self.trains = trains
		self.trainColors = trainColors
		self.stations = {}
		self.sideline = Sideline(self.window, self.trains, self.stations)
		self.allColors = set([i for i in range(len(colors))])
		self.curFrac = 0
		self.timeCount = 0

	# (x_coor, y_coor) refers to (0, 0) or (1, 2) and this function 
	# figures out the actual pixel values
	def addStation(self, x_coor, y_coor, station):
		if (x_coor, y_coor) not in self.stations:
			x = MARGIN + self.block_size*x_coor
			y = MARGIN + self.block_size*y_coor
			if station == StationType.Triangle:
				t = Polygon(Point(x, y-10), Point(x-10, y+10), Point(x+10, y+10))
				t.setFill('red')
				t.draw(self.window)
			elif station == StationType.Circle:
				c = Circle(Point(x,y), 10)
				c.setFill('blue')
				c.draw(self.window)
			elif station == StationType.Square:
				s = Rectangle(Point(x-10, y-10), Point(x+10, y+10))
				s.setFill('green')
				s.draw(self.window)
			else:
				raise Exception('Wrong Station Type')
			s = Station(x_coor, y_coor, station)
			self.stations[(x_coor, y_coor)] = s
		else:
			raise Exception('Station already exists at that location')

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
			self.sideline.updateSideline(self.trains, self.stations)
			self.resetLines()
		elif i == None and len(self.trains) < len(colors):
			curColor = self.randNewColor()
			curTrain = Train(tracks, curColor, self.window, self.block_size)
			self.trainColors.add(curColor)
			self.trains[curColor] = curTrain
			self.sideline.updateSideline(self.trains, self.stations)
			self.resetLines()
		else:
			raise Exception('AllTrains: Max Lines have been reached')

	def removeLine(self, i):
		if i in self.trainColors:
			self.trainColors.remove(i)
			del self.trains[curColor]
			self.sideline.updateSideline(self.trains, self.stations)
			self.resetLines()
		else:
			raise Exception('AllTrains: Line does not exist')

	def updateTracks(self, tracks, i):
		self.trains[i].updateTracks(tracks)
		self.sideline.updateSideline(self.trains, self.stations)
		self.resetLines()

	def addPassengersToStation(self, x_coor, y_coor, t=0, c=0, s=0):
		if (x_coor, y_coor) in self.stations:
			self.stations[(x_coor, y_coor)].addPassengers(t, c, s)
			self.sideline.updateSideline(self.trains, self.stations)
		else:
			raise Exception('Station does not exist')

	def removePassengersFromStation(self, x_coor, y_coor, t, c, s):
		if (x_coor, y_coor) in self.stations:
			self.stations[(x_coor, y_coor)].removePassengers(t, c, s)
			self.sideline.updateSideline(self.trains, self.stations)
		else:
			raise Exception('Station does not exist')

	def maxAdditions(self, train, station):
		num_t = 0
		num_c = 0
		num_s = 0
		curNum = train.num_t + train.num_c + train.num_s
		if curNum != TRAIN_PASSENGER_LIMIT:
			if curNum + station.n_passengers[0] > TRAIN_PASSENGER_LIMIT:
				curNum = TRAIN_PASSENGER_LIMIT
				num_t += (TRAIN_PASSENGER_LIMIT - curNum)
			else:
				curNum += station.n_passengers[0]
				num_t = station.n_passengers[0]

			if curNum + station.n_passengers[1] > TRAIN_PASSENGER_LIMIT:
				curNum = TRAIN_PASSENGER_LIMIT
				num_c += (TRAIN_PASSENGER_LIMIT - curNum)
			else:
				curNum += station.n_passengers[1]
				num_c = station.n_passengers[1]

			if curNum + station.n_passengers[2] > TRAIN_PASSENGER_LIMIT:
				curNum = TRAIN_PASSENGER_LIMIT
				num_s += (TRAIN_PASSENGER_LIMIT - curNum)
			else:
				curNum += station.n_passengers[2]
				num_s = station.n_passengers[2]
		return num_t, num_c, num_s


	def checkForPassengers(self):
		for key in self.trains:
			t = self.trains[key]
			(curX, curY) = t.line[t.curP]
			if (curX, curY) in self.stations:
				s = self.stations[(curX, curY)]
				t.removePassengers(s.station)
				num_t, num_c, num_s = self.maxAdditions(t, s)
				s.removePassengers(num_t, num_c, num_s)
				t.addPassengers(num_t, num_c, num_s, s)
			t.updateText()
		self.sideline.updateSideline(self.trains, self.stations)



	def move(self):
		if self.curFrac == 0:
			print('\n')
			print('TIME COUNT: ', self.timeCount)
			self.checkForPassengers()
			self.timeCount += 1
		for i in self.trains:
			self.trains[i].move()
		self.curFrac = (self.curFrac + 1) % SPEED
		

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
	allTrains.addStation(1, 3, StationType.Triangle)
	allTrains.addStation(0, 2, StationType.Circle)
	allTrains.addStation(2, 1, StationType.Square)
	# print(allTrains.stations)
	tracks = [(0, 1), (0, 2), (0, 3), (1, 3), (1, 2), (1, 1), (2, 1), (2, 0)]
	# tracks2 = [(1, 1), (2, 1), (2, 0), (3, 0), (3, 1)]
	allTrains.createNewLine(tracks, 11)
	# allTrains.createNewLine(tracks2, 6)
	count = 0
	while(True): # for i in range(200):
		# time.sleep(SLEEP)
		allTrains.move()
		# if len(allTrains.trainColors) < len(colors):
		# 	allTrains.createNewLine([(0,0),(0,1)])
		count = (count + 1) % 200
		if count % 200 == 0:
			# allTrains.addPassengersToStation(0, 2)
			allTrains.addPassengersToStation(1, 3, 0, 2, 1)
			allTrains.addPassengersToStation(2, 1, 1, 1, 0)

	# allTrains.updateTracks([(0, 0), (1, 0), (2, 0), (2, 1)], 5)
	







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
