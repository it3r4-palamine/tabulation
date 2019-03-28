from web_admin.models.common_model import CommonModel
from web_admin.models.question import Question, QuestionChoices
from django.db import models
from web_admin.models.exercise import ExerciseQuestion


class StudentAnswer(CommonModel):

    student           = models.ForeignKey("User", on_delete=models.CASCADE)
    exercise_question = models.ForeignKey(ExerciseQuestion, on_delete=models.CASCADE, blank=True, null=True)
    question          = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer            = models.ForeignKey(QuestionChoices, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table = "student_answers"

    def get_dict(self):
        instance = dict()

        instance["student"]  = self.student.get_dict()
        instance["question"] = self.question.get_dict()
        instance["answer"]   = self.answer.get_dict()

        return instance