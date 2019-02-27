from django.db import models
from django.utils import timezone
from user import *

class UserLogs(models.Model):

    user = models.ForeignKey("User",blank=True,null=True)
    date_login = models.DateField(blank=False,null=False,default=timezone.now)
    device = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = "web_admin"
        db_table = "user_logs"

