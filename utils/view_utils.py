import re

def remove_non_numeric_str(string):
	return re.sub("[^0-9]", "", string)