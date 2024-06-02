import unittest

from butter.cli import get_config
from butter.game import Game
from butter.gamelist import GamelistLoader

class GameTest(unittest.TestCase):
	def test_collage_generation(self):
		value = 'https://thumbnails.libretro.com/Sega%20-%20Mega%20Drive%20-%20Genesis/Named_Boxarts/OutRun%202019%20%28Europe%29.png'
		conf = get_config("butter/global.yaml")
		possibles = GamelistLoader().load_data()
		game = Game(possibles, conf)

		detections = game.detect_game('./tests/Games/MD/OutRun 2019.txt', 'MD')

		assert value in detections, f"'{value}' not found in the array"
