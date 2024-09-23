from os.path import splitext, basename, exists
from urllib.parse import quote

def remove_ext(filename):
	return splitext(basename(filename))[0]

def check_for_existing(filepath, replace):
	if not replace and exists(filepath):
		print("Artwork already exists.")
		return True

	return False

def detect_game(file, folder, possibles, conf):
	filename = remove_ext(file)
	device = conf['alias'].get(folder, folder)
	device_entry = conf['consoles'].get(device)

	if device_entry is None or 'retroarch' not in device_entry:
		return None

	device_string = device_entry['retroarch']

	result = [s for s in possibles if all(sub in s for sub in [quote(filename), quote(device_string)])]

	return {
		"results": result,
		"muos": device_entry['muos']
	}

def generate_variants(url):
	variants = ["Named_Boxarts", "Named_Snaps", "Named_Titles"]

	current_variant = None
	for variant in variants:
		if variant in url:
			current_variant = variant
			break

	modified_urls = {}
	if current_variant:
		for variant in variants:
			modified_url = url.replace(current_variant, variant)
			modified_urls[variant] = modified_url
	else:
		for variant in variants:
			modified_urls[variant] = url

	return modified_urls
