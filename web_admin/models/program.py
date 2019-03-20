from web_admin.models.common_model import CommonModel
from web_admin.models.session import Session
from django.db import models


class Course(CommonModel):

    price = models.DecimalField(default=0, blank=True, null=True, decimal_places=2, max_digits=7)

    class Meta:
        app_label = "web_admin"
        db_table = "course"

    def __str__(self):
        return self.name

    def get_dict(self):
        instance = dict()

        instance["uuid"]    = self.uuid
        instance["name"]    = self.name
        instance["company"] = self.company.id

        return instance


class Program(CommonModel):

    price = models.DecimalField(default=0, blank=True, null=True, decimal_places=2, max_digits=7)

    class Meta:
        app_label = "web_admin"
        db_table = "program"

    def __str__(self):
        return self.name

    def get_dict(self):
        instance = dict()

        instance["uuid"]        = self.uuid
        instance["name"]        = self.name
        instance["description"] = self.description

        return instance


class ProgramSession(CommonModel):

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table = "program_sessions"

    def __str__(self):
        return self.name

    def get_dict(self):
        instance = dict()

        instance["uuid"]    = self.pk
        instance["program"] = self.program.pk
        instance["session"] = self.session.get_dict() if self.session else None

        return instance