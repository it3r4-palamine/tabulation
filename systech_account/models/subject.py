from .common_model import *
from utils import dict_types

class Subject(CommonModel):

	class Meta:
		app_label = "systech_account"
		db_table = "subjects"

	def __str__(self):
		return self.name

	def get_dict(self):

		instance = {}

		instance["name"] = self.name
		instance["description"] = self.description

		return instance


