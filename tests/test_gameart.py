import unittest
from PIL.PngImagePlugin import PngImageFile

from butter.game import generate_variants
from butter.game_art import convert_urls_to_images

class GameListTest(unittest.TestCase):
	def test_image_spread(self):
		images = convert_urls_to_images(generate_variants(
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
