import unittest

from butter.cli import get_config
from butter.game import Game
from butter.gamelist import GamelistLoader

class GameTest(unittest.TestCase):
	def setUp(self):
		self.value = 'https://thumbnails.libretro.com/Sega%20-%20Mega%20Drive%20-%20Genesis/Named_Boxarts/OutRun%202019%20%28Europe%29.png'
		self.conf = get_config("butter/global.yaml")
		self.possibles = GamelistLoader().load_data()
		self.game = Game(self.possibles, self.conf)

	def test_game_string_detection(self):
		detections = self.game.detect_game('./tests/Games/MD/OutRun 2019.txt', 'MD')
		assert self.value in detections, f"'{self.value}' not found in the array"

	def test_game_string_split(self):
		strings = self.game.generate_variants(self.value)
		assert len(strings) == 3

if __name__ == '__main__':
	unittest.main()
