from rest_framework import serializers
from web_admin.models.session import Session, SessionExercise


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