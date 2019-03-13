from datetime import datetime,timedelta
from django.utils.timezone import localtime

def format_dates(data):
	fields = [
		'date_of_birth',
		'session_date',
		'enrollment_date',
		'session_end_date',
		'session_start_date',
		'payment_date'
	]

	for value in data.iteritems():
		for field in fields:
			if value[0] == field and value[1]:
				data[field] = format_date(value[1])

	return data
	
def format_times(data):
	try:
		fields = [
			'session_timein',
			'session_timeout'
		]

		for value in data.items():
			for field in fields:
				if value[0] == field:
					data[field] = format_time(value[1])

		return data
	except Exception as e:
		print(e)
		return None
		
def format_time(time):
	try:
		return datetime.strptime(time, '%H:%M:%S').strftime('%H:%M:%S')
	except Exception as e:
		return None

# Test
