from django.db import models
from utils.date_handler import *
from utils.response_handler import *
from utils.dict_types import * 

class TimeSlot(models.Model):

	student = models.ForeignKey("User", null=True, blank=True)
	description = models.CharField(max_length=100,null=True,blank=True)

	time_start = models.TimeField(blank=True, null=True, default=None)
	time_end = models.TimeField(blank=True, null=True, default=None)

	has_sunday = models.BooleanField(default=False)
	has_monday = models.BooleanField(default=False)
	has_tuesday = models.BooleanField(default=False)
	has_wednesday = models.BooleanField(default=False)
	has_thursday = models.BooleanField(default=False)
	has_friday = models.BooleanField(default=False)
	has_saturday = models.BooleanField(default=False)

	date_start = models.DateField(blank=True,null=True)
	date_end = models.DateField(blank=True,null=True)         

	is_current = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		app_label = "web_admin"
		db_table  = "timeslots"
		ordering  = ["id"]

	def generate_days(self):

		days_arrays = []

		if self.has_saturday:
				days_arrays.append("SAT")

		if self.has_sunday:
			days_arrays.append("SUN")

		if self.has_monday:
			days_arrays.append("MON")

		if self.has_tuesday:
			days_arrays.append("TUE")

		if self.has_wednesday:
			days_arrays.append("WED")

		if self.has_thursday:
			days_arrays.append("THU")

		if self.has_friday:
			days_arrays.append("FRI")

		return days_arrays

	def get_dict(self, dict_type = DEFAULT):

		instance = {}

		if dict_type == DEFAULT:

			instance["id"] = self.pk
			instance["description"] = self.description
			instance["student"] = self.student.get_dict() if self.student else None
			instance["time_start"] = str(convert_24_12(self.time_start))
			instance["time_end"] = str(convert_24_12(self.time_end))
			instance["has_sunday"] = self.has_sunday
			instance["has_monday"] = self.has_monday
			instance["has_tuesday"] = self.has_tuesday
			instance["has_wednesday"] = self.has_wednesday
			instance["has_thursday"] = self.has_thursday
			instance["has_friday"] = self.has_friday
			instance["has_saturday"] = self.has_saturday
			instance["days"] = self.generate_days()

		if dict_type == DEVICE:

			days_arrays = []

			instance["id"] = self.pk
			instance["description"] = self.description
			instance["time_start"] = str(convert_24_12(self.time_start))
			instance["time_end"] = str(convert_24_12(self.time_end))
			instance["has_sunday"] = self.has_sunday
			instance["has_monday"] = self.has_monday
			instance["has_tuesday"] = self.has_tuesday
			instance["has_wednesday"] = self.has_wednesday
			instance["has_thursday"] = self.has_thursday
			instance["has_friday"] = self.has_friday
			instance["has_saturday"] = self.has_saturday

			if self.has_saturday:
				days_arrays.append("SAT")

			if self.has_sunday:
				days_arrays.append("SUN")

			if self.has_monday:
				days_arrays.append("MON")

			if self.has_tuesday:
				days_arrays.append("TUE")

			if self.has_wednesday:
				days_arrays.append("WED")

			if self.has_thursday:
				days_arrays.append("THU")

			if self.has_friday:
				days_arrays.append("FRI")

			instance["days"] = days_arrays



		return instance
