from posixpath import splitext
import sys
from os import walk
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

		if game_dir == 'Imgs':
			continue

		for file in files:
			file_ext = splitext(file)[1].lower()
			if file_ext not in conf['include']['filetypes']:
				continue

			print(f"- Processing {file} in {root}")

			file_path = join(root, file)

			check = check_for_existing(f"{root}/Imgs/{remove_ext(file)}.png", args.replace)
			if check:
				continue

			detected = detect_game(file_path, game_dir, possibles, conf)

			if detected is not None and len(detected) > 0:
				selected = None
				if args.interactive:
					selected = get_user_choice(detected)

				try:
					create_image(
						generate_variants(detected[selected] if selected is not None else detected[0]),
						f"{root}/Imgs",
						remove_ext(file)
					)
				except PIL.UnidentifiedImageError:
					print("An image error occurred while processing.")
			else:
				print("No results found.")
