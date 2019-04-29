from django.db.models import Q

from utils import dict_types
from web_admin.models.common_model import *
from utils.response_handler import raise_error


class Exercise(models.Model):

    name               = models.CharField(max_length=200, blank=True, null=True)
    transaction_code   = models.CharField(max_length=200, blank=True, null=True)
    exercise_id        = models.IntegerField(blank=True, null=True)
    program_id         = models.IntegerField(blank=True, null=True)
    set_no             = models.IntegerField(blank=True, null=True)
    total_items        = models.IntegerField(blank=True, null=True)
    is_active          = models.BooleanField(default=True)
    is_intelex         = models.BooleanField(default=False)
    is_post_test       = models.BooleanField(default=False)
    is_assessment_test = models.BooleanField(default=False)
    course             = models.ForeignKey("Course", blank=True, null=True, on_delete=models.CASCADE)
    company            = models.ForeignKey("Company", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table = "transaction_types"

    def get_dict(self, dict_type=dict_types.DEFAULT, isV2=False):
        instance = {}

        if dict_type == dict_types.MINIMAL:
            instance['id']                 = self.pk
            instance['name']               = self.name
            instance['transaction_code']   = self.transaction_code
            instance['is_post_test']       = self.is_post_test
            instance['is_assessment_test'] = self.is_assessment_test
        elif isV2:
            instance['transactionTypeId']   = self.pk
            instance['transactionTypeName'] = self.name
        else:
            instance['id']                  = self.pk
            instance['name']                = self.name
            instance['transaction_code']    = self.transaction_code
            instance['is_active']           = self.is_active
            instance['exercise_id']         = self.exercise_id
            instance['program_id']          = self.program_id
            instance['set_no']              = self.set_no
            instance['total_items']         = self.total_items
            instance['is_intelex']          = self.is_intelex
            instance['is_post_test']        = self.is_post_test
            instance['is_assessment_test']  = self.is_assessment_test
            instance['course']              = self.course.get_dict() if self.course else None
            instance['company']             = self.company.pk

        return instance

    def get_question_count(self):
        return ExerciseQuestion.objects.filter(exercise=self.id, is_deleted=False).count()

    def get_scores(self, is_assessment_test=False, enrollment_id=None):
        total_score = 0

        if is_assessment_test:
            q_filters = Q(enrollment=enrollment_id, session=None, program=None,session_exercise=None)

        from web_admin.models import StudentAnswer
        query_set = StudentAnswer.objects.filter(q_filters)

        if len(query_set) == 0:
            return None

        for qs in query_set:
            if qs.answer.is_correct:
                total_score += 1

        return str(total_score) + "/" + str(query_set.count())


class ExerciseQuestion(models.Model):

    uuid       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise   = models.ForeignKey("Exercise", on_delete=models.CASCADE, blank=True, null=True)
    question   = models.ForeignKey("Question", on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "web_admin"
        db_table = "exercise_questions"

    def __str__(self):
        return self.question.name

    def get_dict(self, dict_type=dict_types.DEFAULT):
        try:
            instance = dict()

            if dict_type == dict_types.DEFAULT:
                instance["uuid"] = self.uuid
                instance["exercise"] = self.exercise.name
                instance["question"] = self.question.get_dict() if self.question else None

            if dict_type == dict_types.QUESTION_ONLY:
                instance = self.question.get_dict(dict_type=dict_types.QUESTION_ONLY) if self.question else None
                instance["exercise_question"] = self.pk

            if dict_type == dict_types.QUESTION_W_ANSWER:
                instance = self.question.get_dict(dict_type=dict_types.QUESTION_W_ANSWER) if self.question else None

            return instance
        except Exception as e:
            raise_error(e)
