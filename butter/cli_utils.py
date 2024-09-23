from argparse import ArgumentParser
from os import getcwd
from urllib.parse import unquote, urlparse


def get_args():
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
	parser.add_argument(
		'--muos', '-m',
		action='store_true',
		help='Use MuOS artwork catalogue format'
	)

	try:
		return parser.parse_args()
	except SystemExit as e:
		if e.code != 0:
			parser.print_help()
		return None

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
