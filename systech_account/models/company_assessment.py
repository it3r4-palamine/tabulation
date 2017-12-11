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
	consultant       = models.ForeignKey("User",blank=True,null=True)
	is_generated     = models.BooleanField(default=0)
	company_rename	 = models.ForeignKey("Company_rename",blank=True,null=True)


	class Meta:
		app_label = "systech_account"
		db_table  = "company_assessment"


	def get_dict(self, forAPI=False):
		company_assessment = {
			"id": self.pk,
			"reference_no": self.reference_no,
			"is_complete": self.is_complete,
			"date_from": self.date_from,
			"date_to": self.date_to,
			"consultant": self.consultant.id if forAPI else self.consultant.get_dict(),
			# "transaction_type": [],
		}

		# Assessment transaction types
		transaction_type_list = []

		if self.transaction_type:
			for transaction_type_id in self.transaction_type:
				try:
					transaction_type_instance = Transaction_type.objects.get(id=transaction_type_id)

					if not transaction_type_instance.is_active: continue
					t_type = transaction_type_instance.get_dict()
					score = str2model("Assessment_score").objects.filter(company_assessment=self.pk,is_active=True,transaction_type=transaction_type_id).first()
					if score:
						t_type['score'] = score.score
					transaction_type_list.append(t_type)
					
				except Transaction_type.DoesNotExist:
					continue


		if forAPI:
			company_assessment["company_name"] = self.company.name
			company_assessment["company_rename_name"] = self.company_rename.name
			company_assessment["consultant_fullname"] = self.consultant.fullname
			company_assessment["transaction_type_arr"] = transaction_type_list
			company_assessment["is_synced"] = self.is_synced
		else:
			company_assessment["is_active"] = self.is_active
			company_assessment["company"] = self.company.get_dict()
			company_assessment["company_rename"] = self.company_rename.get_dict() if self.company_rename else None
			company_assessment["transaction_type"] = transaction_type_list
			company_assessment["is_synced"] = self.is_synced

		return company_assessment