from .common_model import *
from utils import dict_types

class Question(CommonModel):

	question_type = models.ForeignKey("QuestionType", null=True, blank=True)

	class Meta:
		app_label = "systech_account"
		db_table = "questions"

	def get_dict(self):
		instance = {}

		instance["uuid"] = str(self.pk)
		instance["name"] = self.name

		return instance

class QuestionChoices(CommonModel):

	question  	= models.ForeignKey("Question")
	is_correct 	= models.BooleanField(default=False)

	class Meta:
		app_label = "systech_account"
		db_table = "question_choices"

	def get_dict(self):
		instance = {}

		instance["name"]       = self.name
		instance["question"]   = str(self.question.pk)
		instance["is_correct"] = self.is_correct

		return instance

class QuestionType(CommonModel):

	class Meta:
		app_label = "systech_account"
		db_table = "question_type"

	def get_dict(self):
		instance = {}

		instance["name"] = self.name
		instance["description"] = self.description

		return instance