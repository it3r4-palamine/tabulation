from .common_model import *
from utils import dict_types


class Question(CommonModel):

	subject       = models.ForeignKey("Subject", null=True, blank=True, on_delete=models.CASCADE)
	question_type = models.ForeignKey("QuestionType", null=True, blank=True, on_delete=models.CASCADE)
	default_image = models.ImageField(null=True, blank=True, default=None)

	class Meta:
		app_label = "web_admin"
		db_table = "questions"

	def __str__(self):
		return self.name

	def get_dict(self, dict_type=dict_types.DEFAULT):
		instance = dict()

		if dict_type == dict_types.DEFAULT:

			instance["uuid"] 		  = str(self.pk)
			instance["name"] 		  = self.name
			instance["default_image"] = str(self.default_image) if len(str(self.default_image)) > 1 else None
			instance["subject"]       = self.subject.get_dict() if self.subject else None
			instance["question_type"] = self.question_type.get_dict() if self.question_type else None

		if dict_type == dict_types.QUESTION_ONLY:

			instance["uuid"] 			 = str(self.pk)
			instance["name"] 			 = self.name
			instance["default_image"]    = str(self.default_image) if len(str(self.default_image)) > 1 else None
			instance["question_choices"] = self.get_question_choices(dict_type)

		if dict_type == dict_types.QUESTION_W_ANSWER:

			instance["uuid"] = str(self.pk)
			instance["name"] = self.name
			instance["question_choices"] = self.get_question_choices(dict_types.DEFAULT)

		return instance

	def get_question_choices(self,dict_type):
		records = []

		query_set = QuestionChoices.objects.filter(question=self.pk)

		for qs in query_set:
			records.append(qs.get_dict(dict_type=dict_type))

		return records


class QuestionChoices(CommonModel):

	question  	= models.ForeignKey("Question", on_delete=models.CASCADE)
	is_correct 	= models.BooleanField(default=False)

	class Meta:
		app_label = "web_admin"
		db_table = "question_choices"

	def __str__(self):
		return self.name

	def get_dict(self, dict_type=dict_types.DEFAULT):
		instance = dict()

		if dict_type == dict_types.DEFAULT:
			instance["uuid"]	   = str(self.pk)
			instance["name"]       = self.name
			instance["question"]   = str(self.question.pk)
			instance["is_correct"] = self.is_correct

		if dict_type == dict_types.QUESTION_ONLY:
			instance["uuid"] = str(self.pk)
			instance["name"] = self.name
			instance["question"] = str(self.question.pk)

		return instance


class QuestionType(CommonModel):

	class Meta:
		app_label = "web_admin"
		db_table = "question_type"

	def get_dict(self):
		instance = dict()

		instance["uuid"] = str(self.pk)
		instance["name"] = self.name
		instance["description"] = self.description

		return instance