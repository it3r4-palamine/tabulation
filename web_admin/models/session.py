from __future__ import unicode_literals

from utils import dict_types
from web_admin.models.student_answer import StudentAnswer
from web_admin.models.common_model import *
from web_admin.models.exercise import Exercise
from utils.response_handler import *
from utils.date_handler import *
from django.utils import timezone


class Session(CommonModel):

    company = models.ForeignKey("Company", on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table  = "sessions"

    def __str__(self):
        return self.name

    def get_dict(self, dict_type=dict_types.DEFAULT, enrollment_id=None, program_id=None):
        instance = dict()

        if dict_type == dict_types.DEFAULT:

            instance["uuid"]              = self.uuid
            instance["name"]              = self.name
            instance["description"]       = self.description
            instance["company"]           = self.company.id
            instance["session_exercises"] = self.get_session_exercises(enrollment_id, program_id)

        if dict_type == dict_types.STUDENT_PORTAL:

            instance["uuid"] = self.uuid
            instance["name"] = self.name
            instance["description"] = self.description
            instance["company"] = self.company.id
            instance["session_exercises"] = self.get_session_exercises(enrollment_id, program_id)
            instance["session_progress"]  = self.get_answered_exercises(enrollment_id, program_id, as_percentage=True)

        return instance

    def get_answered_exercises(self, enrollment_id, program_id, as_percentage=False):
        query_set = SessionExercise.objects.filter(session=self.pk,is_deleted=False)

        count_exercises_answered = 0
        count_exercises          = query_set.count()

        for qs in query_set:
            if StudentAnswer.objects.filter(enrollment=enrollment_id, program_id=program_id, session_exercise=qs.pk).exists():
                count_exercises_answered += 1

        if as_percentage:
            return count_exercises_answered * (100/count_exercises)

        return count_exercises_answered, count_exercises

    def get_session_exercises(self, enrollment_id, program_id):
        records = []
        query_set = SessionExercise.objects.filter(session=self.pk, is_deleted=False)

        for qs in query_set:

            row = qs.get_dict()

            if StudentAnswer.objects.filter(enrollment=enrollment_id, program_id=program_id, session_exercise=qs.pk).exists():
                row["has_answered"] = True
                row["score"] = qs.get_scores()

            records.append(row)

        return records


class SessionExercise(CommonModel):

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table  = "session_exercises"

    def get_dict(self):
        instance = dict()

        instance["uuid"]     = self.uuid
        instance["session"]  = self.session.pk
        instance["exercise"] = self.exercise.get_dict(dict_type=dict_types.MINIMAL) if self.exercise else None

        return instance

    def get_scores(self):
        total_score = 0
        q_filters = Q(session_exercise=self.pk)

        query_set = StudentAnswer.objects.filter(q_filters)

        for qs in query_set:
            if qs.answer.is_correct:
                total_score += 1

        return str(total_score) + "/" + str(query_set.count())


class SessionVideo(models.Model):

    session    = models.ForeignKey("Session", on_delete=models.CASCADE)
    video_url  = models.TextField()
    is_active  = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "web_admin"
        db_table = "session_videos"

    def get_dict(self):
        instance = dict()
        instance["video_url"] = self.video_url
        return instance


class StudentSession(models.Model):
    
    student         = models.ForeignKey("User", on_delete=models.CASCADE)
    program         = models.ForeignKey("Company_rename", on_delete=models.CASCADE)
    evaluated_by    = models.ForeignKey("User", blank=True, null=True, related_name="evaluated_by", on_delete=models.CASCADE)
    enrollment      = models.ForeignKey("Enrollment", blank=True, null=True, related_name="enrollment", on_delete=models.CASCADE)
    code            = models.CharField(max_length=100, blank=True, null=True)
    session_date    = models.DateField(blank=False, null=False, default=timezone.now)
    session_timein  = models.TimeField(blank=True, null=True, default=None)
    session_timeout = models.TimeField(blank=True, null=True, default=None)
    comments        = models.TextField(blank=True, null=True)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(default=False)
    company         = models.ForeignKey("Company", default=2, on_delete=models.CASCADE)

    class Meta:
        app_label = "web_admin"
        db_table  = "student_session"
        ordering  = ["id"]

    def __str__(self):
        return self.code + " " + str(self.session_timein) + " - " + str(self.session_timeout)

    def get_dict(self, complete_instance=False, return_type=0):
        
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

        exercises = StudentSessionExercise.objects.filter(session = self.id)

        for exercise in exercises:
            results.append(exercise.get_dict(complete_instance=True))

        return results

    def get_exercise_count(self):

        exercise_count = StudentSessionExercise.objects.filter(session = self.id, is_deleted = False).count()

        return exercise_count


class StudentSessionExercise(models.Model):
    
    session = models.ForeignKey("StudentSession", blank=True, null=True,related_name="student_session", on_delete=models.CASCADE)
    exercise = models.ForeignKey("Exercise", blank=True, null=True, on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    trainer_note = models.ForeignKey("TrainerNote", blank=True, null=True, on_delete=models.CASCADE)
    facilitated_by = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "web_admin"
        db_table  = "student_session_exercise"
        ordering  = ["id"]

    def get_dict(self, complete_instance=False):
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

            return instance
        except Exception as e:
            return None

    def get_score_percentage(self):

        if self.score is None:
            self.score = 0

        if self.exercise.total_items is None:
            return 0

        return (self.score * 100) / self.exercise.total_items


