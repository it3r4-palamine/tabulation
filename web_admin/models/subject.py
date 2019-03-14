from .common_model import *
from utils import dict_types


class Subject(CommonModel):

	class Meta:
		app_label = "web_admin"
		db_table = "subjects"

	def __str__(self):
		return self.name

	def get_dict(self, dict_type = dict_types.DEFAULT):
		instance = dict()

		if dict_type == dict_types.DEFAULT:
			instance["uuid"] 		= str(self.uuid)
			instance["name"] 		= self.name
			instance["description"] = self.description
			instance["company"]		= self.company.id if self.company else None

		return instance


