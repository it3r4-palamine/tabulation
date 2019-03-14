from rest_framework import serializers
from web_admin.models.session import Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('name',
                  'description',
                  'price',
                  'company',
                  )