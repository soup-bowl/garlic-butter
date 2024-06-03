import unittest

from butter.cli import get_config
from butter.game import detect_game, generate_variants
from butter.game_list import GamelistLoader

class GameTest(unittest.TestCase):
	def setUp(self):
		self.value = 'https://thumbnails.libretro.com/Sega%20-%20Mega%20Drive%20-%20Genesis/Named_Boxarts/OutRun%202019%20%28Europe%29.png'
		self.conf = get_config("butter/global.yaml")
		self.possibles = GamelistLoader().load_data()

	def test_game_string_detection(self):
		detections = detect_game('./tests/Games/MD/OutRun 2019.txt', 'MD', self.possibles, self.conf)
		assert self.value in detections, f"'{self.value}' not found in the array"

	def test_game_string_split(self):
		result_with_variant = generate_variants(self.value)
		assert "Named_Boxarts" in result_with_variant
		assert "Named_Snaps" in result_with_variant
		assert "Named_Titles" in result_with_variant
		assert result_with_variant["Named_Boxarts"] == self.value


if __name__ == '__main__':
	unittest.main()
