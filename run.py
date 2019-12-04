import mini_metro
from mini_metro import MiniMetroGame, Station, Track

# import mini_metro_graph
# from mini_metro_graph import MiniMetroGame, Station, Track

def enum_point(r, c, dim):
	return r*(dim + 1) + c

def de_enum_point(point, dim):
	return int(point/(dim + 1)), (point % (dim + 1))



def tryThings():
	newGame = MiniMetroGame(2, 2) # 2x2 GRID
	maxNumLines = newGame.maxNumLines
	# print(maxNumLines)
	# print(len(tracks))

	# newGame.addStation(enum_point(0, 0, dim), Station.Triangle)
	# newGame.addStation(enum_point(0, 2, dim), Station.Triangle)
	# newGame.addStation(enum_point(1, 1, dim), Station.Circle)
	newGame.addStation((0,0), Station.Triangle)
	newGame.addStation((0,2), Station.Triangle)
	newGame.addStation((1,2), Station.Circle)
	newGame.addStation((2,3), Station.Square)
	newGame.addStation((1,3), Station.Square)

	# newGame.addLine()
	# newGame.addLine()
	# newGame.addTrackToLine(1, enum_point(0, 1, dim), enum_point(0, 0, dim))
	# newGame.addTrackToLine(1, enum_point(0, 1, dim), enum_point(1, 1, dim))
	# newGame.addTrackToLine(2, enum_point(0, 2, dim), enum_point(0, 1, dim))
	# newGame.addTrackToLine(2, enum_point(0, 1, dim), enum_point(1, 1, dim))
	# print('triangle stations:', newGame.getTriangleStations())
	# print('circle stations:', newGame.getCircleStations())
	# print('tracks:', newGame.getTracks())
	# print('num stations:', newGame.getNumStations())
	# print('tracks utilized:', newGame.getTotalTracksUtilized())
	# print('tracks covered:', newGame.getTotalTracksCovered())
	# newGame.removeTrackFromLine(1, enum_point(0, 1, dim), enum_point(0, 0, dim))
	# print('\n\nRemoved Track from (0, 0) to (0, 1)!\n\n')
	# print('tracks:', newGame.getTracks())
	# print('num stations:', newGame.getNumStations())
	# print('tracks utilized:', newGame.getTotalTracksUtilized())
	# print('tracks covered:', newGame.getTotalTracksCovered())

	newGame.qlearning()
	newGame.baseline()
	newGame.local_search()

def main():
	print('do real stuff here')

if __name__ == '__main__':
	tryThings()
	# main()
