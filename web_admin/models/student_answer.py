from common_model import *
from session import SessionExercise
from question import Question, QuestionChoices
from user import User


class StudentAnswer(CommonModel):

    student  = models.ForeignKey(User)
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