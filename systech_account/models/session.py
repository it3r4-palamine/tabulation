from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models import ExpressionWrapper, DurationField
from utils.date_handler import *
from utils.response_handler import *

class StudentSession(models.Model):
    
    student = models.ForeignKey("User")
    program = models.ForeignKey("Company_rename")
    evaluated_by  = models.ForeignKey("User",blank=True,null=True, related_name="evaluated_by")
    enrollment = models.ForeignKey("Enrollment",blank=True,null=True,related_name="enrollment")    
    code = models.CharField(max_length=100, blank=True, null=True)
    session_date = models.DateField(blank=False, null=False, default=timezone.now)
    session_timein = models.TimeField(blank=True, null=True, default=None)
    session_timeout = models.TimeField(blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "systech_account"
        db_table  = "student_session"
        ordering  = ["id"]

    def __str__(self):
        return self.code + " " + str(self.session_timein) + " - " + str(self.session_timeout)


    def get_dict(self, complete_instance = False, return_type = 0):
        
        instance = {}
        
        if not complete_instance and return_type == 0:
            instance['id'] = self.id
            instance['code'] = self.code if self.code else ""
            instance['student_full_name'] = self.student.fullname
            instance["enrollment_id"] = self.enrollment.id
            instance['program_name'] = self.program.name
            instance['comments'] = self.comments
            instance['session_date'] = str(self.session_date)
            instance['session_timein'] = str(convert_24_12(self.session_timein))
            instance['session_timeout'] = str(convert_24_12(self.session_timeout))

            return instance

        if not complete_instance and return_type == MOBILE_API:
            instance['id'] = self.id
            instance['code'] = self.code if self.code else ""
            instance['program_name'] = self.program.name
            instance['session_date'] = str(self.session_date)
            instance['session_timein'] = str(convert_24_12(self.session_timein))
            instance['session_timeout'] = str(convert_24_12(self.session_timeout))
            instance['exercise_count'] = self.get_exercise_count()
            instance["student_obj"] = {"full_name" : self.student.fullname }

            return instance


        # instance['id'] = self.id
        # instance['code'] = self.code if self.code else ""
        # instance['student_full_name'] = self.student.fullname
        # instance['program_name'] = self.program.name
        # instance['session_date'] = str(self.session_date)
        # instance['session_timein'] = str(convert_24_12(self.session_timein))
        # instance['session_timeout'] = str(convert_24_12(self.session_timeout))
        # instance['time_in'] = time_to_datetime(self.session_timein,True)
        # instance['total_session_time'] = self.format_total_time(self.get_total_session_time())
        # instance['total_session_time_seconds'] = float(self.get_total_session_time().total_seconds())
        # instance['comments'] = self.comments

        if complete_instance:

            instance["id"] = self.id
            instance["code"] = self.code
            instance["enrollment"] = self.enrollment.id
            instance['student'] = self.student.get_dict()
            instance["session_date"] = str(self.session_date)
            instance['session_timein'] = str(convert_24_12(self.session_timein))
            instance['session_timeout'] = str(convert_24_12(self.session_timeout))
            instance['comments'] = self.comments

            if self.enrollment:
                instance['program'] = self.enrollment.get_dict_as_program()
            else:
                instance['program'] = self.program.get_dict()

            if self.evaluated_by:
                instance['evaluated_by'] = self.evaluated_by.get_dict()
                
            instance['session_exercises'] = self.get_exercises()

        return instance

    def clean(self):

        if self.id is None:
            if StudentSession.objects.filter(code=self.code).exists():
                raise ValueError("Code " + self.code + " already exists.")

        return self

    def get_code(self):
        return self.code if self.code else None

    def get_total_session_time(self):
        if self.session_timein == None or self.session_timeout == None:
            d = timedelta(microseconds=0,seconds=0)
            return d

        dt1 = time_to_datetime(self.session_timein)
        dt2 = time_to_datetime(self.session_timeout)

        return dt2 - dt1

    def format_total_time(self,total_time):

        if total_time is None:
            return "Incomplete Logs"

        m, s = divmod(float(total_time.total_seconds()), 60)
        h, m = divmod(m, 60)

        return "%d:%02d:%02d" % (h, m, s)

    def get_exercises(self):
        results = []

        exercises = SessionExercise.objects.filter(session = self.id)

        for exercise in exercises:
            results.append(exercise.get_dict(complete_instance=True))

        return results

    def get_exercise_count(self):

        exercise_count = SessionExercise.objects.filter(session = self.id, is_deleted = False).count()

        return exercise_count




class SessionExercise(models.Model):
    
    session = models.ForeignKey("StudentSession", blank=True, null=True,related_name="student_session")
    exercise = models.ForeignKey("Transaction_type", blank=True, null=True)
    score = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    trainer_note = models.ForeignKey("TrainerNote", blank=True, null=True)    
    facilitated_by = models.ForeignKey("User", blank=True, null=True)    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "systech_account"
        db_table  = "session_exercise"
        ordering  = ["id"]


    def get_dict(self,complete_instance=False):
        try:
            instance = {}
            instance['id'] = self.id
            instance['score'] = self.score
            instance['exercise'] = self.exercise
            
            if self.exercise:
                instance['code'] = self.exercise.transaction_code
                instance['set_no'] = self.exercise.set_no
                instance['exercise_name'] = self.exercise.name
                instance['total_items'] = self.exercise.total_items
                instance['percentage'] = self.get_score_percentage()

            if self.trainer_note:
                instance["trainer_note"] = self.trainer_note.get_dict()
            # if self.trainer_note:
                # instance['note'] = self.trainer_note.name
            if self.facilitated_by:
                instance['facilitated_by'] = self.facilitated_by.first_name

            if complete_instance:
                if self.exercise:
                    instance['exercise'] = self.exercise.get_dict()
                    instance['exercise_set_no'] = { "set_no": self.exercise.set_no, "total_items": self.exercise.total_items }

                # if self.trainer_note:
                    # instance['trainer_note'] = self.trainer_note.get_dict()

                if self.facilitated_by:
                    instance['facilitated_by'] = self.facilitated_by.get_dict()

            print(instance)

            return instance
        except Exception as e:
            print e
            return None

    def get_score_percentage(self):

        if self.score is None:
            self.score = 0

        if self.exercise.total_items is None:
            return 0

        return (self.score * 100) / self.exercise.total_items


