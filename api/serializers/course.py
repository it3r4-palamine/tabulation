from rest_framework import serializers
from web_admin.models.course import Course, CourseProgram


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name',
                  'description',
                  'price',
                  'company'
                  )


class CourseProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseProgram
        fields = (
            'course',
            'program',
        )