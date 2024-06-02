from os.path import splitext, basename
from urllib.parse import quote

class Game():
	def __init__(self, possibles, conf):
		self.possibles = possibles
		self.conf = conf

	def detect_game(self, file, folder):
		filename = splitext(basename(file))[0]
		device = self.conf['alias'].get(folder, folder)
		device_string = self.conf['consoles'].get(device)

		print(f"File: {filename}, Device: {device_string}")

		result = [s for s in self.possibles if all(sub in s for sub in [quote(filename), quote(device_string)])]

		print(result[0] if result is not None else "Blank!")

		return result
