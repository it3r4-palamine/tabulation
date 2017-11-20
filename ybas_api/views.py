from .serializers import *
# DJANGO
from django.db.models import *
# from django.db.models import Count
# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# MODELS
from systech_account.models.company_assessment import *
from systech_account.models.assessments import *
from systech_account.models.multiple_choice import *

from datetime import datetime, timedelta


# GET/UPDATE DATA
class GetData(APIView):
	def post(self, request, *args, **kwargs):
		response = {
			'consultantName': request.user.fullname,
			'is_edit': request.user.is_edit, 
			'assessmentList': [],
			'questionList': [],
			'generalQuestionList': [],
			'choiceList': [],
			'answerList': [],
		}
		transactionTypeIdList = []
		questionList = []
		answerList = []
		generalQuestionList = []

		i = datetime.today()
		date_now = i.strftime('%Y-%m-%d')
		assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True, is_generated=False, date_to__gte=date_now)
		# assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True)

		transactionTypeArrsQs = assessmentQs.values_list('transaction_type', flat=True)

		for transactionTypeArr in transactionTypeArrsQs:
			for transactionTypeId in transactionTypeArr:
				if transactionTypeId not in transactionTypeIdList:
					transactionTypeIdList.append(transactionTypeId)

		# filters = (Q(transaction_type__in = transactionTypeIdList) | Q(transaction_types__contains = transactionTypeIdList)) & Q(is_active=True)
		filters = (Q(transaction_type__in = transactionTypeIdList) | Q(transaction_types__overlap = transactionTypeIdList)) & Q(is_active=True)
		questionQs = Assessment_question.objects.filter(filters).order_by('id')

		choiceFields = ['id', 'value', 'question', 'is_answer']

		for question in questionQs:
			# Choices
			choiceList = Choice.objects.filter(question=question.id, is_active=True).values(*choiceFields)
			response["choiceList"] = response["choiceList"] + list(choiceList)

			# General Questions
			if question.is_general:
				for transaction_type in question.transaction_types:
					generalQuestionList.append({
						"question": question.id,
						"transaction_type": transaction_type,
					})

			questionList.append(question.get_dict(True))

		for assessment in assessmentQs:
			response["assessmentList"].append(assessment.get_dict(True))

			answersQs = Assessment_answer.objects.filter(company_assessment=assessment.pk, question__is_active=True)
			for answers in answersQs:
				row = answers.get_dict(True)
				answerList.append(row)

		response["questionList"] = questionList
		response["generalQuestionList"] = generalQuestionList
		response["answerList"] = answerList
		return Response(response)


# SYNC COMPLETED ASSESSMENTS AND ANSWERS
class SyncAssessments(APIView):
	def post(self, request, *args, **kwargs):
		completedAssessments = request.data

		for assessment in completedAssessments:
			# Save Assessment Complete Status
			assessmentInstance = Company_assessment.objects.get(id=assessment["id"])
			# assessmentInstance.is_complete = True
			if assessment['sync'] == False:
				if assessmentInstance.is_synced == False:
					assessmentInstance.is_synced = False
				else:
					assessmentInstance.is_synced = True
			else:
				assessmentInstance.is_synced = True

			# assessmentInstance.is_synced = assessment['sync'] if assessmentInstance.is_synced == False else True
			for types in assessmentInstance.transaction_type:
				questions = Assessment_question.objects.filter(Q(is_active=True,transaction_type=types) | Q(is_active=True,transaction_types__overlap=[types]))
			
			if len(questions) == len(assessment["answerArr"]):
				assessmentInstance.is_complete = True
			
			assessmentInstance.save()

			answersQs = Assessment_answer.objects.filter(company_assessment=assessmentInstance.id)
			if answersQs.exists():
				answersQs.delete()

			# Save Assessment Answers
			for answer in assessment["answerArr"]:
				serializer = AnswerSerializer(data=answer)
				if serializer.is_valid():
					serializer.save()
				else: Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return Response("Syncing Success")