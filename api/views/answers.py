from api.serializers import *

from django.db.models import *

# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser


from systech_account.views.common import *

# MODELS
from systech_account.models.company_assessment import *
from systech_account.models.assessments import *
from systech_account.forms.assessments import *
from systech_account.models.multiple_choice import *

from datetime import datetime, timedelta

from PIL import Image

import sys, traceback, os
import urllib


class GetAnswers(APIView):

	def get(self,request, question_id = None):
		
		try:
			print("Bit")
			if not int(question_id) > 0:
				raise ValueError("Invalid Parameter")

			answers = Assessment_upload_answer.objects.filter(is_deleted=False, question=question_id, question__uploaded_question=True, transaction_type__in=transactionTypeIdList, company_assessment__in=assessmentIds)

			return Response("Success")
		except Exception as e:
			return Response(str(e), status = 500)

class GetQuestionList(APIView):

	def get(self,request):
		try:
			if 'isV2' in request.data and request.data['isV2']:
				isV2 = request.data['isV2']
			else:
				isV2= False

			response = {
				'userId'	 		 : request.user.id,
				'consultantName'	 : request.user.fullname,
				'is_edit'			 : request.user.is_edit, 
				'assessmentList'	 : [],
				'questionList'		 : [],
				'generalQuestionList': [],
				'relatedQuestionList': [],
				'choiceList'		 : [],
				'symbolList'		 : [],
				'imageAnswerList'	 : [],
				'answerImageList'	 : [],
				'answerList'		 : [],
				'findingsList'		 : [],
				'effectsList'		 : [],
				'generalQuestionList': [],
				'relatedQuestionList': [],
			}

			transactionTypeIdList = []
			questionList 		  = []
			questionIdList 		  = []
			symbolList 			  = []
			imageAnswerList 	  = []
			answerImageList 	  = []
			findingsList 		  = []
			effectsList 		  = []

			# Version 1
			answerList 			= []
			generalQuestionList = []
			relatedQuestionList = []

			existing_images = request.data

			today = datetime.today()
			date_now = today.strftime('%Y-%m-%d')

			assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True, date_to__gte=date_now).order_by("id") ### commented the old code bcoz pwd na mg generate maski wala pa na complete ang assessment
			# assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True, is_generated=False, date_to__gte=date_now)
			# assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True)

			# Get all transaction types of loaded assessments(assessmentQs)
			transactionTypeArrsQs = assessmentQs.values_list('transaction_type', flat=True)

			for transactionTypeArr in transactionTypeArrsQs:
				for transactionTypeId in transactionTypeArr:
					if transactionTypeId not in transactionTypeIdList:
						transactionTypeIdList.append(transactionTypeId)

			# Load questions
			# filters = (Q(transaction_type__in = transactionTypeIdList) | Q(transaction_types__contains = transactionTypeIdList)) & Q(is_active=True)
			filters = (Q(transaction_type__in = transactionTypeIdList) | Q(transaction_types__overlap = transactionTypeIdList)) & Q(is_active=True)
			questionQs = Assessment_question.objects.filter(filters).order_by('id')

			choiceFields = ['id', 'value', 'question', 'is_answer', 'required_document_image', 'follow_up_required']
			questionsIds = []
			hasRelated = False

			for question in questionQs:			
				# Choices
				choiceList = Choice.objects.filter(question=question.id, is_active=True).values(*choiceFields)
				response["choiceList"] = response["choiceList"] + list(choiceList)

				# Findings
				findingsList = []
				findings = Assessment_finding.objects.filter(question=question.id, is_active=True)
				for finding in findings:
					find = finding.get_dict(True)
					findingsList.append(find)
				
				# Effects
				effectsList = []
				effects = Assessment_effect.objects.filter(question=question.id, is_active=True)
				for effect in effects:
					eff = effect.get_dict(True)
					effectsList.append(eff)

				if not isV2:
					if question.has_related:
						questionsRQ = question.get_dict(True)
						questionsIds.append(questionsRQ['id'])
						related_questions = Related_question.objects.get(id=questionsRQ['related_question'],is_active=True)
						hasRelated = True

					# General Questions
					if question.is_general:
						for transaction_type in question.transaction_types:
							generalQuestionList.append({
								"question": question.id,
								"transaction_type": transaction_type,
							})


				# Get question images
				imagesArr = None
				if 'data' in existing_images and len(existing_images['data']) > 0:
					for image in existing_images['data']:
						if image['question'] == question.id:
							imagesArr = image['images']

				questionDict = question.get_dict(True, imagesArr, isV2)

				questionDict['findings'] = findingsList
				questionDict['effects'] = effectsList

				questionIdList.append(question.pk)
				questionList.append(questionDict)

			if not isV2:
				if hasRelated:
					for related_question in related_questions.related_questions:
						if related_question not in questionsIds:
							otherQuestion = Assessment_question.objects.get(id=related_question,is_active=True)
							questionList.append(otherQuestion.get_dict(True))

				related_questions = Related_question.objects.filter(is_active=True)
				for related_question in related_questions:
					for ids in related_question.related_questions:
						try:
							questions = Assessment_question.objects.get(id=ids,is_active=True)
						except Assessment_question.DoesNotExist:
							continue

						row = {}
						row['related_question_id'] = related_question.pk
						row['question_id'] = ids

						relatedQuestionList.append(row)

			# Get assessment ids
			assessmentIds = []
			for assessment in assessmentQs:
				assessmentIds.append(assessment.pk)
				response["assessmentList"].append(assessment.get_dict(True, isV2))

				# if not isV2:
				answersQs = Assessment_answer.objects.filter(company_assessment=assessment.pk, question__is_active=True, is_deleted=False)
				for answers in answersQs:
					row = answers.get_dict(True)
					if isV2:
						row['answer'] = row['text_answer']
						imageAnswerList.append(row)
					else:
						answerList.append(row)

			# Get score
			image_answers = Assessment_upload_answer.objects.filter(is_deleted=False, question__in=questionIdList, question__uploaded_question=True, transaction_type__in=transactionTypeIdList, company_assessment__in=assessmentIds)
			for score in image_answers:
				imageAnswerList.append(score.get_dict())

			answer_images = Assessment_answer_image.objects.filter(is_active=True,question__in=questionIdList,company_assessment__in=assessmentIds,transaction_type__in=transactionTypeIdList)
			for answer_image in answer_images:
				answerImageList.append(answer_image.get_dict(True))

			if not isV2:
				related_questions = Related_question.objects.filter(is_active=True)
				for related_question in related_questions:
					for ids in related_question.related_questions:
						try:
							question = Assessment_question.objects.get(id=ids,is_active=True)
						except Assessment_question.DoesNotExist:
							continue

						row = {}
						row['related_question_id'] = related_question.pk
						row['question_id'] = question.pk

						relatedQuestionList.append(row)

			# Get math symbols
			symbols = Math_symbol.objects.filter(is_active=True)
			for symbol in symbols:
				row_symbol = symbol.get_dict()
				symbolList.append(row_symbol)


			response["questionList"] = questionList
			response["symbolList"] = symbolList
			response["imageAnswerList"] = imageAnswerList
			response["answerImageList"] = answerImageList
			response["lessonUpdateActivities"] = To_dos_topic.objects.filter(company=request.user.company, is_active=True).values('id', 'name')

			if not isV2:
				response["generalQuestionList"] = generalQuestionList
				response["relatedQuestionList"] = relatedQuestionList
				response["answerList"] = answerList

			return Response(response)
		except Exception as e:
			return Response(str(e), status = 500)



		
		