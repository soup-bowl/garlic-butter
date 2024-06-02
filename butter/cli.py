import sys
from argparse import ArgumentParser
from os import walk, getcwd
from os.path import basename, normpath, join
from urllib.parse import unquote, urlparse
from yaml import safe_load, YAMLError

from butter.game import Game
from butter.gamelist import GamelistLoader
from butter.gameart import GameArtwork

def get_config(file):
	with open(file) as stream:
		try:
			conf = safe_load(stream)
		except YAMLError:
			sys.exit(2)

	return conf

def get_user_choice(options, default=0):
	def process_url(url):
		parsed_url = urlparse(url)
		path = parsed_url.path

		parts = path.split('/')
		relevant_parts = parts[-3:-1]
		filename = parts[-1]

		file_without_extension = filename.rsplit('.', 1)[0]

		unencoded_parts = [unquote(part) for part in relevant_parts]
		unencoded_filename = unquote(file_without_extension)

		return unencoded_parts[0], unencoded_filename

	print("Please choose an option from the list below:\n")
	for i, option in enumerate(options):
		disp = process_url(option)
		print(f" [{i}]: {disp[0]}\n        {disp[1]}")

	choice = input(f"\nEnter the number of your choice [{default}]: ").strip()

	if not choice:
		return default

	try:
		choice = int(choice)
		if 0 <= choice < len(options):
			return choice

		print(f"Invalid choice. Please enter a number between 0 and {len(options) - 1}.")
		return get_user_choice(options, default)
	except ValueError:
		print("Invalid input. Please enter a valid number.")
		return get_user_choice(options, default)

def main():
	parser = ArgumentParser(description="Generates artwork for SBC-type game consoles.")
	parser.add_argument(
		'path',
		nargs='?',
		default=getcwd(),
		help='The path to process. Defaults to the current directory'
	)
	parser.add_argument(
		'--interactive', '-i',
		action='store_true',
		help='Ask for decisions, otherwise nearest is chosen'
	)
	parser.add_argument(
		'--replace', '-r',
		action='store_true',
		help='Replaces all, ignoring existing generations'
	)

	try:
		args = parser.parse_args()
	except SystemExit as e:
		if e.code != 0:
			parser.print_help()
		sys.exit(1)

	# aaa
	conf = get_config("butter/global.yaml")
	possibles = GamelistLoader().load_data()
	game = Game(possibles, conf)
	image = GameArtwork()

	for root, dirs, files in walk(args.path):
		game_dir = basename(normpath(root))

		if game_dir == 'Imgs':
			continue

		for file in files:
			print(f"- Processing {file} in {root}")

			file_path = join(root, file)

			check = game.check_for_existing(f"{root}/Imgs/{game.remove_ext(file)}.png", args.replace)
			if check:
				continue

			detected = game.detect_game(file_path, game_dir)

			if detected is not None and len(detected) > 0:
				selected = None
				if args.interactive:
					selected = get_user_choice(detected)

				image.create_image(
					game.generate_variants(detected[selected] if selected is not None else detected[0]),
					f"{root}/Imgs",
					game.remove_ext(file)
				)
			else:
				print("No results found.")
