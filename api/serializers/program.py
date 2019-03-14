from rest_framework import serializers
from web_admin.models.program import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('name',
                  'description',
                  'price',
                  'company',
                  )