from io import BytesIO
from os.path import exists
from os import makedirs
import requests
from PIL import Image
from PIL.Image import Resampling

def create_image(image_urls, directory, filename):
	new_image = Image.new("RGBA", (250, 250), (255, 255, 255, 0))

	if "Named_Snaps" not in image_urls and "Named_Boxarts" not in image_urls:
		print("The required images are not present.")
		return False

	# Load the images from binary data
	background_image = convert_url_to_image(image_urls["Named_Snaps"])
	foreground_image = convert_url_to_image(image_urls["Named_Boxarts"])

	if (background_image is None or foreground_image is None):
		return False

	# Create a new image with dimensions 250x250 with a transparent background
	new_image = Image.new("RGBA", (250, 250), (255, 255, 255, 0))

	# Calculate the position to center the background image slightly offset to the top
	bg_width, bg_height = background_image.size
	bg_position = ((250 - bg_width) // 2, (250 - bg_height) // 2 - 10)

	# Paste the background image onto the new image
	new_image.paste(background_image, bg_position, background_image.convert("RGBA"))

	# Resize the foreground image while maintaining its aspect ratio
	fg_width = 100
	fg_height = int((fg_width / foreground_image.width) * foreground_image.height)
	foreground_image = foreground_image.resize((fg_width, fg_height), Resampling.LANCZOS)

	# Calculate the position to place the foreground image at the bottom left with a 10px margin
	fg_position = (10, 250 - fg_height - 10)

	# Paste the foreground image onto the new image
	new_image.paste(foreground_image, fg_position, foreground_image.convert("RGBA"))

	# Save the new image as a PNG file
	if not exists(directory):
		makedirs(directory)
	new_image.save(f"{directory}/{filename}.png")

	return True

def convert_url_to_image(url):
	def fetch_image_as_binary(url):
		response = requests.get(url, timeout=10)
		response.raise_for_status()
		return BytesIO(response.content)

	try:
		image_binary = fetch_image_as_binary(url)
		image = Image.open(image_binary)
		return image
	except requests.exceptions.RequestException as e:
		print(f"Failed to process image:\n {e}")

	return None
