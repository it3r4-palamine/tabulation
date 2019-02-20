from .common_model import *
from utils import dict_types

class Question(CommonModel):

	class Meta:
		app_label = "systech_account"
		db_table = "questions"