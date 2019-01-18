from django.db import models
from django.utils import timezone
from ..models.settings import *
from ..models.transaction_types import *
from ..models.user import *
from ..models.company import *
from ..models.payment import *
from ..models.assessments import *
from ..models.session import *
from ..models.timeslot import TimeSlot
from ..views.common import *
from utils.dict_types import *
from django.db.models import Count, Sum, Avg,Min,Q,F,Func
from datetime import timedelta

class Enrollment(models.Model):
    user 				= models.ForeignKey("User")
    timeslot            = models.ForeignKey("TimeSlot", null=True, blank=True)
    company_rename 		= models.ForeignKey("Company_rename", blank=True, null=True)
    school 				= models.ForeignKey("School", blank=True,null=True,related_name="school_enrolled")
    enrollment_type 	= models.ForeignKey("EnrollmentType", blank=True, null=True)
    code 				= models.CharField(max_length=100,blank=True,null=True,unique=True)
    is_active 			= models.BooleanField(default=True)
    is_deleted 			= models.BooleanField(default=False)
    session_credits 	= models.DurationField(blank=True, null=True)
    session_start_date 	= models.DateField(blank=True,null=True)    
    session_end_date  	= models.DateField(blank=True,null=True)
    enrollment_date 	= models.DateField(blank=True,null=True)
    company 			= models.ForeignKey("Company")

    class Meta:
        app_label = "systech_account"
        db_table  = "enrollments"
        ordering  = ["id"]

    def get_details(self):

        instance 					= {}
        instance["enrollment_id"] 	= self.id
        instance["program_id"] 		= self.program.id
        instance["student_id"] 		= self.student.id

        return instance

    def get_dict(self, dict_type = DEFAULT):
        try:
            instance = {}

            if dict_type == DEFAULT:
                instance['id'] 						= self.id
                instance['code'] 					= self.code
                instance['school']                  = self.school.get_dict() if self.school else None
                instance['user'] 					= self.user.get_dict()
                instance['user_id'] 				= self.user.id
                instance['company_rename'] 			= self.company_rename.get_dict(dict_type=DEVICE) if self.company_rename else None
                instance['session_credits_seconds'] = self.session_credits.total_seconds() if self.session_credits else 0
                instance['session_start_date'] 		= self.session_start_date
                instance['session_end_date']        = self.session_end_date
                instance['enrollment_date'] 		= self.enrollment_date
                instance['timeslot']                = self.timeslot.get_dict() if self.timeslot else None
                instance['is_expire'] 				= False if self.session_end_date and self.session_end_date >= datetime.now().date() else True

                time_consumed 	= self.get_total_session_time()
                time_remaining 	= self.get_remaining_credit()

                instance["total_session_time"] = format_time_consumed(time_consumed.total_seconds()) if time_consumed else None

                if time_remaining and time_remaining < 0:
                    instance["total_seconds_left"] 	= time_remaining
                    instance["total_time_left"] 	= "-" + format_time_consumed(abs(time_remaining))
                elif time_remaining > 0:
                    instance['total_time_left'] = format_time_consumed(time_remaining)

                return instance

            if dict_type == DEVICE:
                instance['id']                       = self.id
                instance['code']                     = self.code
                instance['program']                  = self.company_rename.get_dict(dict_type=DEVICE) if self.company_rename else None
                instance['session_start_date']       = self.session_start_date
                instance['session_end_date']         = self.session_end_date
                instance['timeslot']                 = self.timeslot.get_dict(dict_type=DEVICE) if self.timeslot else None
                instance['special_reservations']     = []
                instance['session_credits_duration'] = self.session_credits.total_seconds() if self.session_credits else 0
                instance["session_credits_consumed"] = self.get_total_session_time()
 
                return instance
            else:

                instance['id'] 							= self.id
                instance['code'] 						= self.code
                instance['user'] 						= self.user.get_dict()
                instance['school'] 					    = self.school.get_dict() if self.school else None
                instance['company_rename'] 				= self.company_rename.get_dict() if self.company_rename else None
                instance['session_credits'] 			= str(self.session_credits)
                instance['session_credits_seconds'] 	= self.session_credits.total_seconds() if self.session_credits else 0
                instance['session_start_date'] 			= self.session_start_date
                instance['session_end_date'] 			= self.session_end_date
                instance['enrollment_date'] 			= format_date_from_db(self.enrollment_date)
                instance['is_expire'] 					= False if self.session_end_date and self.session_end_date >= datetime.now().date() else True
                instance['total_time_left_seconds'] 	= 0
                instance['timeslot']                    = self.timeslot.get_dict() if self.timeslot else None
                time_consumed 	= self.get_total_session_time()
                time_remaining 	= self.get_remaining_credit()

                instance["total_session_time"] = format_time_consumed(time_consumed.total_seconds()) if time_consumed else None
                instance['is_running'] = True
                if time_remaining and time_remaining < 0:
                    instance['is_running'] = False
                    instance["total_time_left"] = "-" + format_time_consumed(abs(time_remaining))
                elif time_remaining > 0:
                    instance['total_time_left'] = format_time_consumed(time_remaining)
                    instance['total_time_left_seconds'] = time_remaining

            return instance
        except Exception as e:
            print e

    def get_payments(self):
        payments = Payment.objects.filter(enrollment=self.id,is_deleted=False).values()

        for payment in payments:
            payment["payment_date"] = format_date_from_db(payment["payment_date"])

        return payments

    def get_code(self):
        return self.code if self.code else None

    def get_dict_as_program(self):

        instance = {}
        instance['id'] = self.company_rename.id
        instance['program_id'] = self.company_rename.id
        instance['enrollment_id'] = self.id
        instance['name'] = self.company_rename.name
        instance["remaining_credit"] = format_time_consumed(self.get_remaining_credit())

        return instance

    def get_total_session_time(self):

        session_filters = {
            "company_assessment__company_rename__pk" : self.company_rename.id,
            "company_assessment__consultant__pk" : self.user.id,
            "is_deleted" : False
        }

        student_session_filters = {
            "student_id" : self.user.id,
            "enrollment_id" : self.pk,
            "is_deleted" : False
        }

        sessions = Assessment_session.objects.filter(**session_filters).aggregate(total_time_consumed=models.Sum(ExpressionWrapper(F('time_end') - F('time_start'),output_field=DurationField())))
        sessions2 = StudentSession.objects.filter(**student_session_filters).aggregate(total_time_consumed=models.Sum(ExpressionWrapper(F('session_timeout') - F('session_timein'),output_field=DurationField())))

        assessments_session = sessions.get("total_time_consumed", timedelta(seconds=0))
        evaluation_session = sessions2.get("total_time_consumed", timedelta(seconds=0))

        if not assessments_session:
            assessments_session = timedelta(seconds=0)

        if not evaluation_session:
            evaluation_session = timedelta(seconds=0)

        total = assessments_session + evaluation_session

        if total:
            return total
        else:
            return timedelta(seconds=0)

    def get_remaining_credit(self):

        # Get all sessions and computes total time consumed
        # returns remaining credit as Seconds (Float Type)

        total_time_consumed = self.get_total_session_time()

        if self.session_credits and total_time_consumed:
            time_left = self.session_credits - total_time_consumed
            return time_left.total_seconds()
        elif self.session_credits:
            return self.session_credits.total_seconds()


class EnrollmentType(models.Model): 
    name 		= models.CharField(max_length=50, blank=True, null=True) 
    code 		= models.CharField(max_length=50, blank=True, null=True) 
    is_active 	= models.BooleanField(default=True) 
    is_deleted 	= models.BooleanField(default=False) 
    company 	= models.ForeignKey("Company")
 
    class Meta: 
        app_label = "systech_account" 
        db_table  = "enrollment_types" 
        ordering  = ["id"]