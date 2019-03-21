from rest_framework import serializers
from web_admin.models.enrollment import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ('course',
                  'user',
                  'company',
                  )