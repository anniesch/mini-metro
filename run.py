import mini_metro
from mini_metro import MiniMetroGame

def main():
	newGame = MiniMetroGame()
	dim, lines, tracks, stations = newGame.getState()
	# print(len(tracks))

if __name__ == '__main__':
	main()
