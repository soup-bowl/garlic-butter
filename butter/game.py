from os.path import splitext, basename
from urllib.parse import quote

class Game():
	def __init__(self, possibles, conf):
		self.possibles = possibles
		self.conf = conf
	
	def remove_ext(self, filename):
		return splitext(basename(filename))[0]

	def detect_game(self, file, folder):
		filename = splitext(basename(file))[0]
		device = self.conf['alias'].get(folder, folder)
		device_string = self.conf['consoles'].get(device)

		print(f"File: {filename}, Device: {device_string}")

		result = [s for s in self.possibles if all(sub in s for sub in [quote(filename), quote(device_string)])]

		print(result[0] if result is not None else "Blank!")

		return result

	def generate_variants(self, url):
		variants = ["Named_Boxarts", "Named_Snaps", "Named_Titles"]
		
		current_variant = None
		for variant in variants:
			if variant in url:
				current_variant = variant
				break
		
		modified_urls = []
		if current_variant:
			for variant in variants:
				modified_url = url.replace(current_variant, variant)
				modified_urls.append(modified_url)
		else:
			modified_urls.append(url)
		
		return modified_urls
