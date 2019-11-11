import random
import numpy as np
import enum

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

	def addStation(self, point, station_type):
		if (1 > station_type) or (station_type > self.n_station_types) or point not in self.stations:
			raise Exception('addStation(): Entered invalid station')
		if self.stations[point] != Station.Empty:
			raise Exception('addStation(): Station has already been added')
		self.stations[point] = station_type
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




