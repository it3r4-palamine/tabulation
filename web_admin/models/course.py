from web_admin.models.common_model import CommonModel
from web_admin.models.program import Program
from django.db import models


class Course(CommonModel):

    price = models.DecimalField(default=0, blank=True, null=True, decimal_places=2, max_digits=7)

    class Meta:
        app_label = "web_admin"
        db_table = "course"

    def __str__(self):
        return self.name

    def get_dict(self):
        instance        = dict()
        course_programs = []

        instance["uuid"]        = self.uuid
        instance["name"]        = self.name
        instance["description"] = self.description
        instance["company"]     = self.company.id if self.company else None

        query_set = CourseProgram.objects.filter(course=self.pk, is_deleted=False)

        for qs in query_set:
            row = qs.get_dict()
            course_programs.append(row)

        instance["course_programs"] = course_programs

        return instance


class CourseProgram(CommonModel):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table = "course_programs"

    def __str__(self):
        return self.name

    def get_dict(self):
        instance = dict()

        instance["uuid"]    = self.pk
        instance["course"]  = self.course.pk
        instance["program"] = self.program.get_dict() if self.program else None

        return instance