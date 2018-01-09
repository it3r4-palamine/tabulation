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
from systech_account.forms.assessments import *
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
			'findingsList': [],
			'effectsList': [],
			'generalQuestionList': [],
			'relatedQuestionList': [],
			'choiceList': [],
			'answerList': [],
		}
		transactionTypeIdList = []
		questionList = []
		findingsList = []
		effectsList = []
		answerList = []
		generalQuestionList = []
		relatedQuestionList = []
		imageAnswerList = []
		uploadedQuestionList = []

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

		choiceFields = ['id', 'value', 'question', 'is_answer', 'required_document_image', 'follow_up_required']
		questionsIds = []
		hasRelated = False
		for question in questionQs:
			# Choices
			findingsList = []
			effectsList = []
			choiceList = Choice.objects.filter(question=question.id, is_active=True).values(*choiceFields)
			response["choiceList"] = response["choiceList"] + list(choiceList)

			findings = Assessment_finding.objects.filter(question=question.id,is_active=True)
			effects = Assessment_effect.objects.filter(question=question.id,is_active=True)
			for finding in findings:
				find = finding.get_dict(True)
				findingsList.append(find)
			for effect in effects:
				eff = effect.get_dict(True)
				effectsList.append(eff)

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
			uploadedQuestionList.append(question.pk)

			questionsList = question.get_dict(True)
			questionsList['findings'] = findingsList
			questionsList['effects'] = effectsList
			questionList.append(questionsList)

		if hasRelated:
			for related_question in related_questions.related_questions:
				if related_question not in questionsIds:
					otherQuestion = Assessment_question.objects.get(id=related_question,is_active=True)
					questionList.append(otherQuestion.get_dict(True))

		# related_questions = Related_question.objects.filter(is_active=True)
		# for related_question in related_questions:
		# 	for ids in related_question.related_questions:
		# 		try:
		# 			questions = Assessment_question.objects.get(id=ids,is_active=True)
		# 		except Assessment_question.DoesNotExist:
		# 			continue

		# 		row = {}
		# 		row['related_question_id'] = related_question.pk
		# 		row['question_id'] = ids

		# 		relatedQuestionList.append(row) 
		assessmentIds = []
		for assessment in assessmentQs:
			assessmentIds.append(assessment.pk)
			response["assessmentList"].append(assessment.get_dict(True))

			answersQs = Assessment_answer.objects.filter(company_assessment=assessment.pk, question__is_active=True, is_deleted=False)
			for answers in answersQs:
				row = answers.get_dict(True)
				answerList.append(row)

		# print(assessmentIds)
		# print(transactionTypeIdList)

		image_answers = Assessment_upload_answer.objects.filter(is_deleted=False,question__in=uploadedQuestionList,transaction_type__in=transactionTypeIdList,company_assessment__in=assessmentIds)
		for score in image_answers:
			imageAnswerList.append(score.get_dict())

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

		response["questionList"] = questionList
		# response["effectsList"] = effectsList
		# response["findingsList"] = findingsList
		response["generalQuestionList"] = generalQuestionList
		response["relatedQuestionList"] = relatedQuestionList
		response["answerList"] = answerList
		response["imageAnswerList"] = imageAnswerList
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
			
			# if len(questions) == len(assessment["answerArr"]):
			# 	assessmentInstance.is_complete = True
			assessmentInstance.is_complete = assessment['is_complete']
			if assessment['credits_left']:
				assessmentInstance.credits_left = timedelta(seconds=assessment['credits_left'])
			
			assessmentInstance.save()

			for t_type in assessment['t_types']:
				datus = {
					'transaction_type' : t_type['transactionType'],
					'company_assessment' : t_type['assessment'],
					'is_active' : True,
					# 'score' : t_type['score'],
				}


				if 'score' in t_type:
					# datus['score'] = t_type['score']
					
					if 'scores' in t_type and t_type['scores']:
						for score in t_type['scores']:
							datus['question'] = score['id']
							datus['score'] = score['score']
							datus['uploaded_question'] = True

							try:
								instance = Assessment_score.objects.get(company_assessment=t_type['assessment'],transaction_type=t_type['transactionType'],is_active=True,question=score['id'],uploaded_question=True)
								assessment_score_form = Assessment_score_form(datus, instance=instance)
							except Assessment_score.DoesNotExist:
								assessment_score_form = Assessment_score_form(datus)

							if assessment_score_form.is_valid():
								assessment_score_form.save()
							else: Response(assessment_score_form.errors,status=status.HTTP_400_BAD_REQUEST)
					else:
						datus['score'] = t_type['score']
						datus['uploaded_question'] = False
						try:
							instance = Assessment_score.objects.get(company_assessment=t_type['assessment'],transaction_type=t_type['transactionType'],is_active=True,uploaded_question=False)
							assessment_score_form = Assessment_score_form(datus, instance=instance)
						except Assessment_score.DoesNotExist:
							assessment_score_form = Assessment_score_form(datus)

						if assessment_score_form.is_valid():
							assessment_score_form.save()
						else: Response(assessment_score_form.errors,status=status.HTTP_400_BAD_REQUEST)

			sessionsQs = Assessment_session.objects.filter(company_assessment=assessmentInstance.id)
			for sessionsQ in sessionsQs:
				sessionsQ.is_deleted = True
				sessionsQ.save()

			for session in assessment['session']:
				sessions = {
					'company_assessment' : session['assessment_id'],
					'date' : session['date'],
					'time_start' : session['time_start'],
					'time_end' : session['time_end'],
				}

				session_form = Assessment_session_form(sessions)
				if session_form.is_valid():
					session_form.save()
				else: Response(session_form.errors,status=status.HTTP_400_BAD_REQUEST)

			answersQs = Assessment_answer.objects.filter(company_assessment=assessmentInstance.id)
			for answersQ in answersQs:
				answersQ.is_deleted = True
				answersQ.save()
			# if answersQs.exists():
				# answersQs.delete()

			imageAnswersQs = Assessment_upload_answer.objects.filter(company_assessment=assessmentInstance.id)
			for imageAnswersQ in imageAnswersQs:
				imageAnswersQ.is_deleted = True
				imageAnswersQ.save()

			# Save Assessment Answers
			arrayAns = []
			for answer in assessment["answerArr"]:
				if 'answers' in answer:
					for ans in answer['answers']:
						answerObj = {}
						answerObj['is_active'] = True
						answerObj['item_no'] = ans['item_no']
						answerObj['answer'] = ans['answer_text'] if 'answer_text' in ans else None
						answerObj['question'] = ans['question']
						answerObj['company_assessment'] = answer['company_assessment']
						answerObj['transaction_type'] = answer['transaction_type']

						if answerObj not in arrayAns:
							arrayAns.append(answerObj)

							answer_form = Assessment_upload_answer_form(answerObj)

					# cprint(arrayAns)
							if answer_form.is_valid():
								answer_form.save()
				if 'uploaded_question' not in answer:
					serializer = AnswerSerializer(data=answer)
					if serializer.is_valid():
						serializer.save()
					else: Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return Response("Syncing Success")