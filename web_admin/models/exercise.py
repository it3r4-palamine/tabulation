from web_admin.models.common_model import *
from utils.response_handler import raise_error


class ExerciseQuestion(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise    = models.ForeignKey("Transaction_type", on_delete=models.CASCADE, blank=True, null=True)
    question    = models.ForeignKey("Question", on_delete=models.CASCADE)
    is_deleted  = models.BooleanField(default=False)

    class Meta:
        app_label = "web_admin"
        db_table = "exercise_questions"

    def __str__(self):
        return self.question.name

    def get_dict(self):
        try:
            instance = dict()

            instance["uuid"]     = self.uuid
            instance["exercise"] = self.exercise.name
            instance["question"] = self.question.get_dict() if self.question else None

            return instance
        except Exception as e:
            raise_error(e)






