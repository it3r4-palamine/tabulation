from web_admin.models import CommonModel, SessionExercise, Question, QuestionChoices
from django.db import models


class StudentAnswer(CommonModel):

    student  = models.ForeignKey("User", on_delete=models.CASCADE)
    exercise = models.ForeignKey(SessionExercise)
    question = models.ForeignKey(Question)
    answer   = models.ForeignKey(QuestionChoices)

    class Meta:
        app_label = "web_admin"
        db_table = "student_answers"

    def get_dict(self):
        instance = dict()

        instance["student"]  = self.student.get_dict()
        instance["exercise"] = self.exercise.get_dict()
        instance["question"] = self.question.get_dict()
        instance["answer"]   = self.answer.get_dict()