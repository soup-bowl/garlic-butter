from posixpath import splitext
import sys
from os import walk, rename
from os.path import basename, normpath, join
import PIL

from butter.cli_utils import get_args, get_user_choice
from butter.game import check_for_existing, detect_game, generate_variants, remove_ext
from butter.game_list import GamelistLoader
from butter.game_art import create_image
from butter.utils import get_config

def main():
	args = get_args()
	if args is None:
		sys.exit(1)

	conf = get_config("butter/global.yaml")
	possibles = GamelistLoader().load_data()

	for root, dirs, files in walk(args.path):
		game_dir = basename(normpath(root))

		for file in files:
			file_ext = splitext(file)[1].lower()
			if file_ext not in conf['include']['filetypes']:
				continue

			print(f"- Processing {file} in {root}")

			file_path = join(root, file)

			detected = detect_game(file_path, game_dir, possibles, conf)

			directory = f"../info/catalogue/{detected['muos']}/box" if args.muos is True else 'Imgs' 

			check = check_for_existing(f"{root}/{directory}/{remove_ext(file)}.png", args.replace)
			if check:
				continue

			if detected['results'] is not None and len(detected['results']) > 0:
				selected = None
				if args.interactive:
					selected = get_user_choice(detected['results'])

				try:
					create_image(
						generate_variants(detected['results'][selected] if selected is not None else detected['results'][0]),
						f"{root}/{directory}",
						remove_ext(file)
					)
				except PIL.UnidentifiedImageError:
					print("An image error occurred while processing.")
			else:
				print("No results found.")
