from os import walk
from posixpath import splitext
import sys
from os.path import basename, normpath, join
from yaml import YAMLError, safe_load


def get_config(file):
	with open(file) as stream:
		try:
			conf = safe_load(stream)
		except YAMLError:
			sys.exit(2)

	return conf
