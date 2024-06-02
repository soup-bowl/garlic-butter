import sys
from argparse import ArgumentParser
from os import walk, getcwd
from os.path import basename, normpath, join
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

def main():
	parser = ArgumentParser(description="Generates artwork for SBC-type game consoles.")
	parser.add_argument(
		'path',
		nargs='?',
		default=getcwd(),
		help='The path to process. Defaults to the current directory.'
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
		for file in files:
			print(f"- Processing {file} in {root}")

			file_path = join(root, file)
			detected = game.detect_game(file_path, game_dir)

			if detected is not None:
				image.create_image(game.generate_variants(detected[0]), f"{root}/Imgs", game.remove_ext(file))
