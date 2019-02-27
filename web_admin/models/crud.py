from django.db import models
from django.db.models import Count, Sum, Avg,Min,Q,F,Func

class Record(models.Model):
	name       = models.CharField(max_length=200)

	class Meta:
		app_label = "web_admin"
		db_table  = "record"

	def as_dict(self):
		return {"id" : self.pk,"name" : self.name,}