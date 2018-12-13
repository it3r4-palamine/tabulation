import re
import decimal


def remove_non_numeric_str(string):
	return re.sub("[^0-9]", "", string)

def obj_decimal_to_float(objs):
	try:
		for key,value in objs.items():
			if isinstance(objs[key], decimal.Decimal):
				objs[key] = float(objs[key])

		return objs
	except Exception as e:
		raise ValueError(e)