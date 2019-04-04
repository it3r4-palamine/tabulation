from utils import dict_types
from web_admin.models import StudentAnswer
from web_admin.models.common_model import CommonModel
from web_admin.models.session import Session, SessionExercise
from django.db import models


class Program(CommonModel):

    price = models.DecimalField(default=0, blank=True, null=True, decimal_places=2, max_digits=7)

    class Meta:
        app_label = "web_admin"
        db_table = "program"

    def __str__(self):
        return self.name

    def get_dict(self):
        instance = dict()

        instance["uuid"]             = self.uuid
        instance["name"]             = self.name
        instance["description"]      = self.description
        instance["program_sessions"] = self.get_program_sessions()

        return instance

    def get_program_sessions(self):
        records = []
        query_set = ProgramSession.objects.filter(program=self.pk,is_deleted=False)

        for qs in query_set:
            records.append(qs.get_dict())

        return records


class ProgramSession(CommonModel):

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table = "program_sessions"

    def __str__(self):
        return self.name

    def get_dict(self, dict_type=dict_types.DEFAULT):
        instance = dict()

        if dict_type == dict_types.DEFAULT:
            # Will be used in mobile
            instance["uuid"]      = self.pk
            instance["program"]   = self.program.pk
            instance["session"]   = self.session.get_dict() if self.session else None
            instance["exercises"] = self.get_session_exercises()

        if dict_type == dict_types.AS_SESSION:
            instance = self.session.get_dict(dict_type=dict_types.STUDENT_PORTAL) if self.session else None

        return instance

    def get_session_exercises(self):
        records = []
        query_set = SessionExercise.objects.filter(session=self.session.pk)

        for qs in query_set:

            row = qs.get_dict()

            if StudentAnswer.objects.filter(session_exercise=qs.pk).exists():
                row["has_answered"] = True
                row["score"] = qs.get_exercise_score()

            records.append(row)

        return records
