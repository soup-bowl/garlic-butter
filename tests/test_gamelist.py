import unittest

from butter.gamelist import GamelistLoader

class GameListTest(unittest.TestCase):
	def setUp(self):
		self.glist = GamelistLoader()

	def test_valid_value_array(self):
		haystack = self.glist.load_data()
		needle = "https://thumbnails.libretro.com/Nintendo%20-%20Game%20Boy/Named_Boxarts/Tetris%202%20%28USA%29.png"
		assert needle in haystack, f"'{needle}' not found in the array"

if __name__ == '__main__':
	unittest.main()
