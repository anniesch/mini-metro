import random
import numpy as np
import enum

class Station(enum.Enum):
	Empty = 0
	Triangle = 1
	Circle = 2
	Square = 3

class Track(enum.Enum):
	NoTrack = 0
	Track = 1

def enum_point(r, c, dim):
	return r*(dim + 1) + c

class MiniMetroGame:
	def __init__(self, dim=3, n_types=2):
		self.dim = dim
		self.lines = {} # each line is a key which points to a list of its tracks
		self.tracks = {} # lookup dictionary if an edge is a track or not
		self.stations = {} # lookup dictionary if a point is a station and if so, which station
		for r in range(self.dim + 1):
			for c in range(self.dim + 1):
				cur = enum_point(r, c, self.dim)
				self.stations[cur] = Station.Empty
				if c + 1 != self.dim + 1:
					curBelow = enum_point(r, c + 1, self.dim)
					self.tracks[(cur, curBelow)] = Track.NoTrack
				if r + 1 != self.dim + 1:
					curRight = enum_point(r + 1, c, self.dim)
					self.tracks[(cur, curRight)] = Track.NoTrack

	def getState(self):
		return self.dim, self.lines, self.tracks, self.stations






