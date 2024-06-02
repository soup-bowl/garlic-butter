import unittest
from PIL.PngImagePlugin import PngImageFile

from butter.cli import get_config
from butter.game import Game
from butter.gameart import GameArtwork
from butter.gamelist import GamelistLoader

class GameListTest(unittest.TestCase):
	def setUp(self):
		self.conf = get_config("butter/global.yaml")
		self.possibles = GamelistLoader().load_data()
		self.game = Game(self.possibles, self.conf)
		self.gart = GameArtwork()

	def test_image_spread(self):
		images = self.gart.convert_urls_to_images(self.game.generate_variants(
			"https://thumbnails.libretro.com/Sega%20-%20Mega%20Drive%20-%20Genesis/Named_Boxarts/OutRun%202019%20%28Europe%29.png"
		))

		if len(images) == 3:
			for image in images:
				try:
					self.assertIsInstance(image, PngImageFile, "Image is not a valid PngImageFile object")
				except Exception as e:
					self.fail(f"Data is not a valid image: {e}")
		else:
			self.fail(f"Not enough images in data array.")


if __name__ == '__main__':
	unittest.main()
