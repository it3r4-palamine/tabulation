from django.db import models
# from ..models.assessments import *
from ..models.transaction_types import *
from ..models.company import *
from ..models.user import *
from ..views.common import *

class Company_assessment(models.Model):
	date_from        = models.DateField(blank=True,null=True)
	date_to          = models.DateField(blank=True,null=True)
	is_active        = models.BooleanField(default=1)
	transaction_type = ArrayField(models.IntegerField("Transaction_type"),blank=True,null=True)
	company          = models.ForeignKey("Company")
	is_synced        = models.BooleanField(default=0)
	is_complete      = models.BooleanField(default=0)
	reference_no     = models.CharField(max_length=200,blank=True,null=True,unique=True)
	consultant       = models.ForeignKey("User",blank=True,null=True,related_name="consultant")
	is_generated     = models.BooleanField(default=0)
	company_rename	 = models.ForeignKey("Company_rename",blank=True,null=True)
	session_credits	 = models.DurationField(blank=True, null=True)
	credits_left	 = models.DurationField(blank=True, null=True)
	facilitator      = models.ForeignKey("User",blank=True,null=True,related_name="facilitator")


	class Meta:
		app_label = "systech_account"
		db_table  = "company_assessment"


	def get_dict(self, forAPI=False):
		company_assessment = {
			"id"			 : self.pk,
			"reference_no"	 : self.reference_no,
			"is_complete"	 : self.is_complete,
			"date_from"		 : self.date_from,
			"date_to" 		 : self.date_to,
			"session_credits": self.session_credits.total_seconds() if self.session_credits else None,
			"credits_left"	 : self.credits_left.total_seconds() if self.credits_left else None,
			"consultant" 	 : self.consultant.id if forAPI else self.consultant.get_dict(),
			# "transaction_type": [],
		}

		# Assessment transaction types
		transaction_type_list = []
		sessions_list = []

		if self.transaction_type:
			for transaction_type_id in self.transaction_type:
				try:
					transaction_type_instance = Transaction_type.objects.get(id=transaction_type_id)

					if not transaction_type_instance.is_active: continue
					t_type = transaction_type_instance.get_dict()
					score = str2model("Assessment_score").objects.filter(company_assessment=self.pk,is_active=True,transaction_type=transaction_type_id)
					if score:
						scores = []
						for questionScore in score:
							if questionScore.uploaded_question:
								row = {}
								row['id'] = questionScore.question.pk
								row['score'] = questionScore.score

								scores.append(row)

								t_type['scores'] = scores
							else: t_type['score'] = questionScore.score
					transaction_type_list.append(t_type)
					
				except Transaction_type.DoesNotExist:
					continue

		sessions = str2model("Assessment_session").objects.filter(is_deleted=False,company_assessment=self.pk,time_end__isnull=False)
		for session in sessions:
			rowSession = session.get_dict()
			if forAPI:
				rowSession['assessment_id'] = session.company_assessment.pk
				sessions_list.append(rowSession)
			else:
				sessions_list.append(rowSession)

		if forAPI:
			company_assessment["company_name"] 		   = self.company.name
			company_assessment["company_rename_name"]  = self.company_rename.name
			company_assessment["consultant_fullname"]  = self.consultant.fullname
			company_assessment["transaction_type_arr"] = transaction_type_list
			company_assessment["is_synced"] 		   = self.is_synced
			company_assessment["sessions"] 			   = sessions_list
		else:
			company_assessment["is_active"] 	   = self.is_active
			company_assessment["company"] 		   = self.company.get_dict()
			company_assessment["company_rename"]   = self.company_rename.get_dict() if self.company_rename else None
			company_assessment["transaction_type"] = transaction_type_list
			company_assessment["is_synced"]   	   = self.is_synced
			company_assessment["facilitator"] 	   = self.facilitator.get_dict() if self.facilitator else None
			# company_assessment["sessions"] = json.dumps(sessions_list)
			company_assessment["sessions"]	  	   = sessions_list

		return company_assessment