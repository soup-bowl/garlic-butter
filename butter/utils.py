import sys
from yaml import YAMLError, safe_load


def get_config(file):
	with open(file) as stream:
		try:
			conf = safe_load(stream)
		except YAMLError:
			sys.exit(2)

	return conf
