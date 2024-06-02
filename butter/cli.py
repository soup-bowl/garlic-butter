from argparse import ArgumentParser
from os import walk, getcwd
from os.path import basename, normpath, join
from yaml import safe_load, YAMLError

from butter.game import Game
from butter.gamelist import GamelistLoader

def get_config(file):
	with open(file) as stream:
		try:
			conf = safe_load(stream)
		except YAMLError as exc:
			exit(2)

	return conf

def main():
	parser = ArgumentParser(description="Generates artwork for SBC-type game consoles.")
	parser.add_argument(
		'path',
		nargs='?',
		default=getcwd(),
		help='The path to process. Defaults to the current directory.'
	)
	parser.add_argument('--type', type=str, help='Your console')

	try:
		args = parser.parse_args()
	except SystemExit as e:
		if e.code != 0:
			parser.print_help()
		exit(1)

	# aaa
	conf = get_config("butter/global.yaml")
	possibles = GamelistLoader().load_data()
	game = Game(possibles, conf)

	for root, dirs, files in walk(args.path):
		dir = basename(normpath(root))
		for file in files:
			file_path = join(root, file)
			game.detect_game(file_path, dir)

	print(f"Hello")
