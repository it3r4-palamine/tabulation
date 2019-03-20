from rest_framework import serializers
from web_admin.models.program import Program, ProgramSession


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('name',
                  'description',
                  'price',
                  'company',
                  )


class ProgramSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramSession
        fields = (
            'program',
            'session',
        )