from django.contrib import admin
from systech_account.models import *


# Register your models here.
admin.site.register(User)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(QuestionChoices)


