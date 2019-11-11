import mini_metro
from mini_metro import MiniMetroGame

def main():
	newGame = MiniMetroGame(2, 2)
	dim, lines, tracks, stations, n_stations = newGame.getState()
	maxNumLines = newGame.getMaxNumLines()
	print(maxNumLines)
	# print(len(tracks))

if __name__ == '__main__':
	main()
