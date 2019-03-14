from rest_framework import serializers
from web_admin.models.program import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name',
                  'description',
                  'price',
                  'company'
                  )