from rest_framework import serializers
from web_admin.models.session import Session, SessionExercise, SessionVideo


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('name',
                  'description',
                  'company',
                  )


class SessionExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionExercise
        fields = (
            'session',
            'exercise',
        )


class SessionVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionVideo
        fields = (
            'session',
            'video_url',
        )