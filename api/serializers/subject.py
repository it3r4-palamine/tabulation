from rest_framework import serializers
from web_admin.models.subject import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name',
                  'description',
                  'company',
                  )