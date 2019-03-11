from django.db import models
from django.utils import timezone


class UserLogs(models.Model):

    user = models.ForeignKey("User",blank=True,null=True, on_delete=models.CASCADE)
    date_login = models.DateField(blank=False,null=False,default=timezone.now)
    device = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = "web_admin"
        db_table = "user_logs"

