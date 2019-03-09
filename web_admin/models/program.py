from common_model import *


class Course(CommonModel):

    class Meta:
        app_label = "web_admin"
        db_table = "course"


class Program(CommonModel):

    class Meta:
        app_label = "web_admin"
        db_table = "company"