from rest_framework import serializers
from web_admin.models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name',
                  'description',
                  'price',
                  'company'
                  )