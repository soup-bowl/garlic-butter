import requests
from PIL import Image
from io import BytesIO
from os.path import exists
from os import makedirs

class GameArtwork():
	def create_image(self, image_urls, directory, filename):
		new_image = Image.new("RGBA", (250, 250), (255, 255, 255, 0))
		images = self.convert_urls_to_images(image_urls)

		if len(images) < 2:
			return None

		# Load the images from binary data
		background_image = images[1]
		foreground_image = images[0]

		# Create a new image with dimensions 250x250 with a transparent background
		new_image = Image.new("RGBA", (250, 250), (255, 255, 255, 0))

		# Calculate the position to center the background image slightly offset to the top
		bg_width, bg_height = background_image.size
		bg_position = ((250 - bg_width) // 2, (250 - bg_height) // 2 - 10)

		# Paste the background image onto the new image
		new_image.paste(background_image, bg_position, background_image.convert("RGBA"))

		# Resize box art
		foreground_image = foreground_image.resize((100, 100))

		# Calculate the position to place the foreground image at the bottom left with a 10px margin
		fg_position = (10, 250 - 100 - 10)

		# Paste the foreground image onto the new image
		new_image.paste(foreground_image, fg_position, foreground_image.convert("RGBA"))

		# Save the new image as a PNG file
		if not exists(directory):
			makedirs(directory)
		new_image.save(f"{directory}/{filename}.png")

	def convert_urls_to_images(self, urls):
		images = []
		for url in urls:
			try:
				image_binary = self._fetch_image_as_binary(url)
				image = Image.open(image_binary)
				images.append(image)
			except Exception as e:
				print(f"Failed to process image from {url}: {e}")
		return images

	def _fetch_image_as_binary(self, url):
		response = requests.get(url)
		response.raise_for_status()
		return BytesIO(response.content)
