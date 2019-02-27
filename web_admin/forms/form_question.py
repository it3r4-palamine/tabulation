from django import forms
from ..models.question import Question, QuestionChoices

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('name',
				  )

class QuestionChoiceForm(forms.ModelForm):

    class Meta:
        model = QuestionChoices
        fields = ('name',
                  'is_correct',
                  'question',
              )