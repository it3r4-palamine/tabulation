from django.contrib import admin
from web_admin.models import *


# Register your models here.
admin.site.register(User)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(QuestionChoices)
admin.site.register(Company)
admin.site.register(StudentAnswer)


