from utils import dict_types
from web_admin.models.common_model import *
from utils.response_handler import raise_error


class ExerciseQuestion(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise    = models.ForeignKey("Exercise", on_delete=models.CASCADE, blank=True, null=True)
    question    = models.ForeignKey("Question", on_delete=models.CASCADE)
    is_deleted  = models.BooleanField(default=False)

    class Meta:
        app_label = "web_admin"
        db_table = "exercise_questions"

    def __str__(self):
        return self.question.name

    def get_dict(self, dict_type=dict_types.DEFAULT):
        try:
            instance = dict()

            if dict_type == dict_types.DEFAULT:
                instance["uuid"]     = self.uuid
                instance["exercise"] = self.exercise.name
                instance["question"] = self.question.get_dict() if self.question else None

            if dict_type == dict_types.QUESTION_ONLY:
                instance                      = self.question.get_dict(dict_type=dict_types.QUESTION_ONLY) if self.question else None
                instance["exercise_question"] = self.pk

            return instance
        except Exception as e:
            raise_error(e)






