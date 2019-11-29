import random
import numpy as np
import enum
import matplotlib.pyplot as plt
import collections


LINES_LIMIT = 0.7 	# the fraction of number of total possible tracks that
					# gives us the maximum number of lines we're allowed

class Station(int, enum.Enum):
	Empty = 0
	Triangle = 1
	Circle = 2
	Square = 3

class Track(int, enum.Enum):
	NoTrack = 0
	Track = 1

def enum_point(r, c, dim):
	return r*(dim + 1) + c

def de_enum_point(point, dim):
	return (int(point/(dim + 1)), (point % (dim + 1)))

class MiniMetroGame:
	def __init__(self, dim=3, n_types=2):
		self.dim = dim
		self.n_station_types = n_types
		self.lines = {} # each line is a key which points to a set of tracks
		self.tracks = {} # lookup dictionary if an edge is a track or not
		self.stations = {} # lookup dictionary if a point is a station and if so, which station
		self.stationToLines = {} # lookup dictionary from station (tuple of point and type of station) to a set of lines it belongs to
		self.n_stations = 0
		self.triangleStations = set()
		self.circleStations = set()
		self.squareStations = set()
		for r in range(self.dim + 1):
			for c in range(self.dim + 1):
				cur = enum_point(r, c, self.dim)
				self.stations[cur] = int(Station.Empty)
				if c + 1 != self.dim + 1:
					curBelow = enum_point(r, c + 1, self.dim)
					self.tracks[(cur, curBelow)] = (int(Track.NoTrack), 0) # second value refers to number of times that the track is used
				if r + 1 != self.dim + 1:
					curRight = enum_point(r + 1, c, self.dim)
					self.tracks[(cur, curRight)] = (int(Track.NoTrack), 0)
		self.maxNumLines = int(LINES_LIMIT*len(self.tracks))
		self.totalTracksUtilized = 0 # only increment for the first time we utilize a track
		self.totalTracksCovered = 0 # this includes double counts if two lines (or even one line) use the same track along its path

		self.all_lines = [] # list of all lists representing lines
		self.station_pairs = {} # lookup dictionary from (station, station) (of diff types) to 0 or the line list for if a line is built between them
		self.all_stations = collections.defaultdict(int)

	def addLine_2(self, line):
		if len(self.lines) == self.maxNumLines:
			raise Exception('addLine(): Reached maximum number of lines')
		newLine = len(self.lines) + 1 # LINES ARE ONE-INDEXED - sorry lol
		self.lines[newLine] = set(line) # set of tracks

	def addLine(self):
		if len(self.lines) == self.maxNumLines:
			raise Exception('addLine(): Reached maximum number of lines')
		newLine = len(self.lines) + 1 # LINES ARE ONE-INDEXED - sorry lol
		self.lines[newLine] = set() # set of tracks

	def addTrackToLine(self, line, point1, point2):
		# TODO!!! - think about how we double count (or more) a track for the same line?
		# it would not update the set of tracks in self.lines but it would increase self.totalTracksCovered
		if len(self.lines) == 0:
			raise Exception('addTrackToLine(): There are no current lines')
		if line not in self.lines:
			raise Exception('addTrackToLine(): Entered invalid line')
		track = (point1, point2)
		if track not in self.tracks:
			track = (point2, point1)
		if track not in self.tracks:
			raise Exception('addTrackToLine(): Entered invalid track')
		if self.tracks[track][0] == int(Track.Track):
			self.tracks[track] = (int(Track.Track), self.tracks[track][1] + 1)
			self.lines[line].add(track)
			self.totalTracksCovered += 1
		else:
			self.tracks[track] = (int(Track.Track), 1) # if it's already a track, that's aight
			self.lines[line].add(track)
			self.totalTracksUtilized += 1
			self.totalTracksCovered += 1

	def removeTrackFromLine(self, line, point1, point2):
		# TODO!! How do we deal with double counts of a track for a line?
		# Should someone have to call this multiple times?
		if line not in self.lines:
			raise Exception('removeTrackFromLine(): Entered invalid line')
		track = (point1, point2)
		if track not in self.tracks:
			track = (point2, point1)
		if track not in self.tracks:
			raise Exception('removeTrackFromLine(): Entered invalid track')
		elif self.tracks[track][0] == Track.NoTrack:
			raise Exception('removeTrackFromLine(): Tried to remove a track not in use')
		elif track not in self.lines[line]:
			raise Exception('removeTrackFromLine(): Tried to remove a track not in use by this line')
		if self.tracks[track][1] == 1:
			self.tracks[track] = (int(Track.NoTrack), 0)
			self.lines[line].remove(track)
			self.totalTracksCovered -= 1
			self.totalTracksUtilized -= 1
		else:
			self.tracks[track] = (int(Track.Track), self.tracks[track][1] - 1)
			# !!!! account for double counts here, maybe don't remove from set
			self.lines[line].remove(track)
			# !!!! account for double counts here, maybe don't remove from set
			self.totalTracksCovered -= 1

	# def addStation(self, point, station_type):
	# 	if (1 > station_type) or (station_type > self.n_station_types) or point not in self.stations:
	# 		raise Exception('addStation(): Entered invalid station')
	# 	if self.stations[point] != Station.Empty:
	# 		raise Exception('addStation(): Station has already been added')
	# 	self.stations[point] = station_type
	# 	self.n_stations += 1
	# 	if station_type == Station.Triangle:
	# 		self.triangleStations.add(point) # de_enum_point(point, self.dim)
	# 	elif station_type == Station.Circle:
	# 		self.circleStations.add(point)
	# 	elif station_type == Station.Square:
	# 		self.squareStations.add(point)

	def addStation(self, point, station_type):
		if self.all_stations[point] != Station.Empty:
			raise Exception('addStation(): Station has already been added')
		self.all_stations[point] = station_type
		self.n_stations += 1
		if station_type == Station.Triangle:
			self.triangleStations.add(point) # de_enum_point(point, self.dim)
		elif station_type == Station.Circle:
			self.circleStations.add(point)
		elif station_type == Station.Square:
			self.squareStations.add(point)

	def constructLine(self, line):
		# TODO!!! - basically update tracks by using a path searching algorithm
		# that creates a list of tracks (including double counts) which lays out
		# the shortest path covering all the tracks in the set (from self.lines)
		# ANOTHER THING - remove (and/or add) tracks if it makes sense to and update
		# all values accordingly
		# update self.totalTracksCovered, self.totalTracksUtilized, self.lines, self.stations, etc.
		print('TODO!!!')

	def getDim(self):
		return self.dim

	def getNumStationTypes(self):
		return self.n_station_types

	def getLines(self):
		return self.lines

	def getTracks(self):
		return self.tracks

	def getStations(self):
		return self.stations

	def getStationsToLine(self):
		return self.stationToLines

	def getNumStations(self):
		return self.n_stations

	def getTriangleStations(self):
		return self.triangleStations

	def getCircleStations(self):
		return self.circleStations

	def getSquareStations(self):
		return self.squareStations

	def getMaxNumLines(self):
		return self.maxNumLines

	def getTotalTracksUtilized(self):
		return self.totalTracksUtilized

	def getTotalTracksCovered(self):
		return self.totalTracksCovered

	def getState(self):
		return self.getDim(), self.getLines(), self.getTracks(), self.getStations(), self.getNumStations()


	def reward(self, state, a):
		reward = 0
		if action < len(self.pair_to_index.keys()): # action is to add line	
			reward -= 1
		else: # action is to remove line
			reward -= 2
		# Add distance to passengers as negative reward!!


	def init_station_pairs(self):
		# creates a station-pair dictionary that maps to if a line has been built between the pair of stations 
		for triangle in self.triangleStations:
			for square in self.squareStations:
				self.station_pairs[(triangle, square)] = 0
			for circle in self.circleStations:
				self.station_pairs[(triangle, circle)] = 0
		for square in self.squareStations:
			for circle in self.circleStations:
				self.station_pairs[(circle, square)] = 0

	def init_states(self):
		self.index_to_pair = {}
		self.pair_to_index = {}
		self.index_to_line = {}
		#self.state = {}
		#list_all_states = []
		print("Station pairs", self.station_pairs)
		for i, pair in enumerate(self.station_pairs):
			self.index_to_pair[i] = pair
			self.pair_to_index[pair] = i
			self.index_to_line[i] = 0 # start out with no lines
			#self.state[]
		print("INDEX to pair", self.index_to_pair)


	def createLine(self, first_station, second_station): # same as constructLine
		# returns the state achieved after taking action to create line 
		line = []
		x_first, y_first = first_station[0], first_station[1]
		x_second, y_second = second_station[0], second_station[1]
		while x_first > x_second:
			line.append(((x_first, y_first), (x_first - 1, y_first)))
			x_first -= 1
		while x_first < x_second:
			line.append(((x_first, y_first), (x_first + 1, y_first)))
			x_first += 1
		while y_first > y_second:
			line.append(((x_first, y_first), (x_first, y_first - 1)))
			y_first -= 1
		while y_first < y_second:
			line.append(((x_first, y_first), (x_first, y_first + 1)))
			y_first += 1

		self.addLine_2(line)
		self.all_lines.append(line)
		pair = (first_station, second_station)
		self.station_pairs[pair] = line
		self.index_to_line[self.pair_to_index[pair]] = 1


	def removeLine(self, first_station, second_station):
		# returns the state achieved after taking action to remove line
		self.station_pairs[(first_station, second_station)] = 0
		pair = (first_station, second_station)
		self.index_to_line[self.pair_to_index[pair]] = 0
		# for line in self.all_lines:
		# 	# find and remove line
		# 	first_edge = line[0]
		# 	last_edge = line[len(line) - 1]
		# 	if (first_edge[0] is first_station and last_edge[1] is second_station) or (first_edge[0] is second_station and last_edge[1] is first_station):
		# 		self.all_lines.remove(line)


	def pos_actions(self, state):
		# returns a list of possible actions from a state: tuples of (track added/removed, and corresponding new state)
		actions = []
		# If not at the max num of lines and train tracks allowed, can add a line
		if len(self.lines.keys()) < self.maxNumLines:
			# Can add line
			# Check which station pairs don't have lines already
			for pair in state.keys():
				if not state[pair]: # doesn't have line already
					# add line
					actions.append(self.pair_to_index[pair]) # adding action is between 0 and num+pairs - 1
				else:
					# Can also remove an existing line
					actions.append(self.pair_to_index[pair] + len(self.pair_to_index.keys()))
		return actions


	def transition_probs(self, state, action):
		# returns a list of transition probabilities for each state given an action and an original state
		rand_num = np.random.uniform()
		new_state = 0
		if rand_num < 0.7: # with prob 0.7, the correct action is executed			
			if action < len(self.pair_to_index.keys()): # action is to add line	
				pair = self.index_to_pair[action]
				self.createLine(pair[0], pair[1])
				new_state = state + 2**action
			else: # action is to remove line
				pair = self.index_to_pair[action - len(self.index_to_pair.keys())]
				self.removeLine(pair[0], pair[1])
				action -= len(self.index_to_pair.keys())
				new_state = state - 2**action
		else: # with prob 0.3, no action is taken (due to regulations)
			new_state = state
		return new_state

	def qlearning(self):
		self.init_station_pairs()
		self.init_states()
		# performs Q learning
		# Initialize Q table, learning rate
		learning_rate = 0.8
		discount = 0.98
		self.Q = np.zeros((2**len(self.station_pairs), 2 * len(self.station_pairs))) # each station pair can have a line or not

		# Training
		# track state by number of zeroes/which station pairs have lines between them
		# state s = number in binary, i.e. sum 2^i for each station pair i 
		num_episodes = 1
		episode_rewards = np.zeros(num_episodes)
		for i in range(num_episodes):
			t = 0
			while t < 20:
				for curr_state_index in range(2**len(self.station_pairs)): # j is the state
					# Handle current state
					bin_j = bin(curr_state_index) # binary j
					bin_j = bin_j[2:]
					# get station pairs & existing lines from bin_j
					curr_state = {}
					for digit_index in range(len(str(bin_j))):
						curr_state[self.index_to_pair[digit_index]] = int(str(bin_j)[digit_index])

					print("CURR STATE", curr_state, curr_state_index)
					# Choose action
					pos_acts = self.pos_actions(curr_state) # possible actions from the current state (either add or remove line)
					print(pos_acts)
					if len(pos_acts) == 0:
						break
					best_next_action = np.argmax(self.Q[curr_state_index, :])
					if best_next_action not in pos_acts: # if not a possible action
						best_next_action = np.random.choice(pos_acts) # choose action randomly FIX THIS LATER
					new_state_index = self.transition_probs(curr_state_index, best_next_action)

					# Learning step (TD update)
					predict_val = self.Q[curr_state_index, best_next_action]
					reward = self.reward(curr_state, best_next_action)
					target = reward + discount * np.max(self.Q[new_state_index, :])
					self.Q[curr_state_index, best_next_action] += learning_rate * (target - predict_val)
					
					episode_rewards[i] += reward
					t += 1


		print("Episode rewards: ", episode_rewards)
		plt.plot(episode_rewards)
		plt.show()

		# Test Evaluation after Q learning


# def main():
#     minimetro = MiniMetroGame()
#     minimetro.qlearning()


# if __name__ == '__main__':
#     main()




