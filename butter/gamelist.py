import os
import zipfile
import datetime
from pathlib import Path
import requests
from appdirs import user_data_dir

class GamelistLoader:
	def __init__(self, cache_duration_days=30):
		self.url = "https://soupbowl.io/rgs/gameart.txt.zip"
		self.cache_duration_days = cache_duration_days
		self.cache_dir = Path(user_data_dir("garlic-butter", "soupbowl"))
		self.cache_file = self.cache_dir / "gameart.txt"
		self.cache_dir.mkdir(parents=True, exist_ok=True)

	def download_file(self, dest_path):
		response = requests.get(self.url)
		response.raise_for_status()
		with open(dest_path, 'wb') as f:
			f.write(response.content)

	def extract_zip(self, zip_path, extract_to):
		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(extract_to)

	def load_lines_from_file(self, file_path):
		with open(file_path, 'r') as f:
			lines = f.readlines()

		return [line.strip() for line in lines]

	def cache_is_valid(self):
		if not self.cache_file.exists():
			return False
		file_age = datetime.datetime.now() - datetime.datetime.fromtimestamp(self.cache_file.stat().st_mtime)

		return file_age.days <= self.cache_duration_days

	def load_data(self):
		cache_valid = self.cache_is_valid()

		if not cache_valid:
			zip_path = self.cache_dir / "gameart.txt.zip"
			print("Downloading new data...")
			self.download_file(zip_path)
			print("Extracting data...")
			self.extract_zip(zip_path, self.cache_dir)
			os.remove(zip_path)

		print("Loading data into memory...")
		lines = self.load_lines_from_file(self.cache_file)
		print("Data loaded successfully.")

		return lines
