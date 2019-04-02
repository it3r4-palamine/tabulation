from web_admin.models.common_model import CommonModel
from web_admin.models.question import Question, QuestionChoices
from web_admin.models.exercise import ExerciseQuestion
from utils import dict_types
from django.db import models


class StudentAnswer(CommonModel):

    student           = models.ForeignKey("User", on_delete=models.CASCADE)
    session           = models.ForeignKey("Session", on_delete=models.CASCADE, blank=True, null=True)
    session_exercise  = models.ForeignKey("SessionExercise", on_delete=models.CASCADE, blank=True, null=True)
    exercise_question = models.ForeignKey(ExerciseQuestion, on_delete=models.CASCADE, blank=True, null=True)
    question          = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer            = models.ForeignKey(QuestionChoices, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table = "student_answers"

    def get_dict(self, dict_type=dict_types.DEFAULT):
        instance = dict()

        if dict_type == dict_types.DEFAULT:
            instance["student"] = self.student.get_dict()
            instance["question"] = self.question.get_dict()
            instance["answer"] = self.answer.get_dict()

        if dict_type == dict_types.CUSTOM:
            instance = self.answer.get_dict()

        return instance