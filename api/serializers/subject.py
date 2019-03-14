from rest_framework import serializers
from utils import error_messages
from web_admin.models.subject import Subject
from utils.response_handler import raise_error


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name',
                  'description',
                  'company',
                  )

    @staticmethod
    def check_name_exists(name, company):
        try:
            Subject.objects.get(name=name, company=company, is_deleted=False)
            raise_error(error_messages.NAME_EXIST)
        except Subject.DoesNotExist:
            pass

    def to_internal_value(self, data):
        name    = data.get("name")
        company = data.get("company")
        self.check_name_exists(name, company)

        return super(SubjectSerializer, self).to_internal_value(data)


