from .serializers import *

from django.db.models import *

# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# Base64
class GetBase64Photo(APIView):

    def post(self, request):
        try:
            assessmentImage = Assessment_image.objects.filter(question=21, is_active=True).first()

            image = open('systech_account/static/uploads/%s' % (assessmentImage.image), 'rb')
            image_read = image.read()
            image_64_encode = base64.standard_b64encode(image_read)

            data = {}
            data['image'] = image_64_encode

            return Response(data)

        except Exception as e:
            print(e)
            return Response(str(e), status=500)


# Actual File
class GetPhoto(APIView):

    def post(self, request):
        try:
            assessmentImage = Assessment_image.objects.filter(question=21, is_active=True).first()
            image = open('systech_account/static/uploads/%s' % (assessmentImage.image), 'rb')

            return HttpResponse(image, content_type="image/png")

        except Exception as e:
            print(e)
            return Response(str(e), status=500)


# Final
class GetQuestionPhoto(APIView):

    def post(self, request):
        data = req_data(request, True)
        image = open('systech_account/%s' % (data['imageLocation']), 'rb')
        # assessmentImage = Assessment_image.objects.filter(question=21, is_active=True).first()
        # image = open('systech_account/static/uploads/%s'%(assessmentImage.image), 'rb')

        return HttpResponse(image, content_type="image/png")
    # try:
    # assessmentImage = Assessment_image.objects.filter(question=21, is_active=True).first()

    # except Exception as e:
    #   	print(e)
    #   	return Response(str(e), status = 500)


# Get Answer Image photos
class GetAnswerImagePhoto(APIView):

    def post(self, request):
        data = req_data(request, True)
        image = open('systech_account/static/uploads/assessment/document_images/%s' % (data['imageLocation']), 'rb')

        return HttpResponse(image, content_type="image/png")


# GET/UPDATE DATA
class GetData(APIView):

    def post(self, request, *args, **kwargs):

        if 'isMobile' in request.data:
            print "werk werk"

        print request.META.get('HTTP_MOBILE')

        if 'isV2' in request.data and request.data['isV2']:
            isV2 = request.data['isV2']
        else:
            isV2 = False

        response = {
            'userId'	 		: request.user.id,
			'consultantNe'	 : request.user.fullname,
			'is_edit'			 : request.user.is_edit, 
			'assessmentLt'	 : [],
			'questionL'		 : [],
			'generalQuestionList': [],
			'relatedQuestionList': [],
			'choiceL'		 : [],
			'symbolL'		 : [],
			'imageAnswerLt'	 : [],
			'answerImageLt'	 : [],
			'answerL'		 : [],
			'findingsL'		 : [],
			'effectsL'		 : [],
			'generalQuestionList': [],
			'relatedQuestionList': []
        ,
		}

		transactionTypeIdList
        = []
		que List 		  = []
		quest List 		  = []
		s ist 			  = []
		imageA rList 	  = []
		answer eList 	  = []
		fin List 		  = []
		ef List 		  = []

		#
        sion 1
		a rList 			= []
		generalQuestion
        t = []
		relatedQuestionList = []

		existing_images = request \

        .data

		today = dat \
        me.today()
		date_now = today.strftime( \

        '%Y-%m-%d')

		assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True, date_to__gte=da
            te_now  ).order_by("id") ### commented the old code bcoz pwd na mg generate maski wala pa na compl
         ang assessment
		# assessmentQs = Company_assessment.objects.filter(consultant=request.user.id, is_active=True, is_generated=False, date
        __gte=date_now)
		# assessmentQs = Company_assessment.objects.filter(consultant=request.user.i

        s_active=True)

		# Get all transaction types of loaded assessm
        s(assessmentQs)
		transactionTypeArrsQs = assessmentQs.values_list('transaction

        e', flat=True)

		for transactionTypeArr in tran \
            ionTypeArrsQs:
			for transactionTypeId in t \
                ctionTypeArr:
				if transactionTypeId not in tran \
                    nTypeIdList:
					transactionTypeIdList.append(

        transactionTypeId)

		# Load questions
		# filters = (Q(transaction_type__in = transactionTypeIdList) | Q(transaction_types__contains = transactionTypeIdList
        & Q(is_active=True)
		filters = (Q(transaction_type__in = tra
            nsactionTypeIdList) | Q(trnaction_types__overlap = transactionTypeIdList)
        ) & Q(is_active=True)
		questionQs = Assessment_question.objects.filter( \

        filters).order_by('id')

		choiceFields = ['id', 'value', 'question', 'is_answer', 'required_documen
        mage', 'follow_up
        quired']
		questio

        s = []
		hasRelated = False

		for question in \
            questionQs:
			# Choices
			choiceList = Choice.objects.filter(question=question.id, is_
            ve=True).values(*choiceFields)
			response["choiceList"] = response[ \

            "choiceList"
            ] + list(choi
            st)

			# Findings
			findingsList = []
			findings = Assessment_finding.objects.f \
            r(question=question.id,
                is_active=True)
			for finding in \
                findings:
				find = finding. \

            ge \
            ct(True)
				fin
            sList.append(find)
			
			# Effects
			effectsList = []
			effects = Assessment_ \
            ct.objects.filter(question=
                question.id, is_active=True
                )
			for effect in \

            effects:
				eff
                = effect.get_dict(True)
				effectsList.append(eff)

			if not isV2:
				if question.has_related:
					ques
                    Q = question.get_dict(True)
					questionsIds.append(questionsRQ['id'])
					related _questions = Re \
                    question.objects.get(id \

                =questionsRQ[
                'related_question'],is_active
                    =True)
					hasRelated = True

				# General
                        ns
				if question.is_general: \
                            for transaction_type in \
                            question.transaction_types:
						ge
                        es

            st.append({
							"q
            ion": question.id,
							"transaction_type": transaction_type,
						})


			# Get qu
                n images
			imagesArr = None
			if 'data' \
                    in existing_images and len(exist
                        ges['data']) > 0:
				for image \

            in existing_images['data']:
					if image['question'] == question.id:
						imagesArr = image['
            es']

			questionDict = question.get_dict( \

            True, imagesArr, isV2)

			qu
            onDict['findings'] = findingsList

        questionDict[
            'effects'] = \
                effectsList

			questionIdList.append(question.pk)
			questionList.
                    append(questionDict)

		if not isV2: \
                        if hasRelated:
				for related_question in related_questions.relat ed_questions:
					if
                        related_question not in questionsIds:

            otherQuestion = Assessment_question.objects.get(id=related_question,is_active
            =True)
						questionList.append(other
                ion.get_dict(True))

			related_questions = Re \
                    question. \
                        objects.filter(is_active=True)
			for related_ question in rel \
                    uestions:
				for ids in related_question. \
                        relate \

                    ions:
					try
                    :
						questions = Assessment_question.objects. \
                    get(id=ids,is_active=True

                    )
					except Assessment \

        stion.DoesNotExist:
						continue

					row = {}
					row['related_questio
            '] = related_question.pk
					row['
            tion_id'] = ids

					relatedQuestionList.append(row)

		# Get ass

            nt ids
		asses
            tIds = []
		for assessment in assessmentQs:
			assessmentIds.append(assessment.pk)
			response["assessme
                                                         tList"].append(as
            ment.get_dict(True, isV2))

			# if not isV2:
			answersQs = \
                Assess \
                    nswer.objects.filter(company_assessment=
                    assessment.pk, questi
                s_active=
                    True, is_deleted=False

        )
			for
        answers in answersQs:
				row = answers.get_dict(True)
				if isV2:
					row['answer'] = row['text_an
                                                                wer']
					imageAnswerList.append( \
                                                                row)
				else:
					answerList.append(row)

		# Get score
		image_answers = Asse \
        ent_upload_answer.objects.f \
            r(is_deleted=False, question__in=questio

        ist, question__uploaded_question=True, transaction_type__in=transactio nTypeIdList, company_assessm
                                                               ent__in=assessmentIds)
		for score in image_answers:
			imageAnswerList.append(s
        e.get_dict())

		answer_images = A \
            sment_answer_image.objects.filter(is_active=True,qu

        on__in=quest
            dList,company_assessment__in=assessmentIds,transaction_type__in=tra
            tionTypeIdList)
		for answer_image in answ \
                ages:
			answerImageList.append(answer_image.g
                    t(True))

		if not isV2:
			related_questions = Related_quest ion.objects.filter( \
                    is_active=True)
			for related_question in \
                        re \

                    uestions: \
                    for ids in related_question.related_questions:
                    try:
						question = Assessment_ \

                    n.objects.get(id=ids,is_active=True

        )
					except \
        Assessment_question.DoesNotExist:
						continue
        row = {}
					row['related_
            tion_id'] = related_question.pk
					row['question_id'] = question. \

        pk

					relatedQuestionList.append( \
        row)

		# Get math symbols
		symbols
        = Math_symbol.objects.filter(is_active=True)
		for symbol in symbols:
			row_symbol = symbol. \
        get_dict()
			symbolList.append(row_symbol)


		response["questionList"] = questionList
		re
                                                                         ponse["symbolList"] = symbolList
		r

        nse["imageAn
            List"] = imageAnswerList
		response["answerImageList"] =
            answerImageList
		response["lessonUpdateActivities"] = To_dos_topic.objects.filter(company=

        request.user.company, is_active=True).values('id', 'name')

		if not isV2:
			response["generalQuestionList"] = gener \

    uestionList
			response["relatedQuestionL
        "] = \
            relatedQuesti \
            st
			response["answerList"] = answerList

		return Response(response)


# SYNCIN
                ASSESSMENTS, ANSWERS, SCORE
                 QUESTION TIME
class SyncAssessments(APIView):

	def post \
                (self,
                request, *args, **kwargs):
		try:

            print "Gogoy"
			print request.data['data']

                if 'isV2' in request.data and request.data['isV2']:
				isV2 = request.data['isV2']
				completedAsse

                s = request.data['data']
			else:
				isV2= False
				completedAssessments = request. \
                        data

			for assessment in co \
                    dAssessments \
                        :

				# Update Assessment Status
                    assessmentInstance = Company_assessment. \

                objects.get(id=assessment["id"])

				if assessment['sync'] ==

                False:
					if
                assessmentInstance.is_synced == \
                    False:
						assessmentInstance.is_synced = False
					else:
						assessm
                stance.
                    is_synced = True
				else:
					a
                        ntInstance.is_synced = True

				assessmentInstance.is_complete = assessment['is_complete'

                ]

				# Credi

                t
				if assessment['credits_left']:
                    assessmen
                        ce.credits_left =timedelta(seconds=assessment[
                        'credits_left'])else:
					if assessment['c
                        left'] == 0:
                    assessme

                    nce.credits_left = timedelta( \
                    seconds=assessment['credits_left'])
				

				assessmentInstance.save()

				for
                            t_type in assessment['t_types']:
					datus = {
						'transaction_type' : t_type['transactionType'],
						'company_assessment' : t_type['assessment'],
                            'is_active' : True,
					}

					#

                            ' in t_type:
					if 'scores' in t_type and t_type['scores']:
						for score in t_type['scor
                                                                        es']:
							datus['question'] = score['id'
                                                                        ]
							datus[ 'score'] = score['sco
                                                                        re']
							# datus['up
                                estion'] = False if 'not_uploaded_question' in score else True
							datus[
                            'uploaded_question'] = True

							try:
								instance = Assessment_score.objects.get(comp

                            sment=t_type['assessment'],transaction_type=
                                t_type['transactionType'],
                                is_active=True,question=score['id'],uploaded_question=True)
								assessment_score_form = Assessmen \

                    _form(datus, instance=instance)
							except
                        Assessment_score.DoesNotExist:
								assessment_score_form = Assessme \
                        e_form(datus \
                            )

							if assessment_score_form.is_valid():
								assessment_score_
                                                                    form.save()
							else: Response(assessmen
                                                                    t_score_form.er rors,status=status.HTTP_
                            REQUEST)

					elif 'score' in t_type and t_type['score']:
						datus['score'
                        ] = t_type['score']
						datus[
                            'uploaded_question'] = False
						try:
							instance =

                        Assessment_score.objects.get(
                            company_assessment=t_type['a
                        nt'],
                            transaction_type=t_type['transactionTy pe'],is_active=True,uploaded_question=

                False)
							assessment_score_form = Assessment_score_form(datus, instance=instance)
						except Ass \

                t_score.DoesNotExist:
                    assessment_score_form = Assessment \
                    _form(datus)

						if assessment_score_form.is_valid():
                    assessment_score_form.save()
						else
                        : Response(assessment_score_form.errors,status=status.HTTP_400_BAD_REQUEST)

				s
                            essionsQs = \
                        Assessment_session.objects.filter(company_assessment=assessmentInstance.id,is_deleted=False
                    )

				for sessionsQ in sessionsQs:
					s
                    sQ.is_deleted = \
                        True
					sessionQ.save()

				for session in \
                        assesment['session']:
					if
                        'time_nd' not in session:
                        time_end_final = (datetime.strptime(str(session['time_start']), '%H:%M:%S')) + timedelta(minutes=10)
						time_end_final = (datetime.strptime(str(time_end_final
                        ),'%Y-%m-%d %H:%M:%S').time
                        ())
					ele:
						time_end_final = session[ \
                        'timeend']
					sessions = {
						'company_assessment' : session[

                    'assessment_id'],
						'date' : session['date'],
						'time_start' :
                    session['time_start'],
                        # 'time_end' : sess
                    ime_e
                        d'] if 'time_end' in session  else (datetime.strptime(str(session

                _start']), '%H:%M:%S')) + timedelta(minutes=10),
						'time_end' : time_end_final,
                'transaction_type' : session[
                    'transactionType'],
                    'question' : session['

                on'] if 'question' in session else None
					}

					session_form = Assessment_session_form(sessio
                                                                         ns)
					if sessi \

                m.is_valid():
						session_form.save()
					else: Response(session_form.errors
                    ,status=status.

                HTTP_400_BAD_REQUEST)
                answersQs = Asse \
                t_answer.objects.filter(company_assessment=

                    assessmen
                    nce.id)
				for answersQ in a \
                    Qs:
					answersQ.is_deleted = True
					answersQ.save()
                    imageAnswersQs = Assessment_upload_answer.objects.filter(company
                    sment=assess
                        tance.id,is_deleted=False)

				for imageAnswersQ in imageAnswersQs:
					imageAnswersQ.is_deleted = True
                                imageAnswersQ.save()

				# Save Assessment Answers
				arrayAns = []
				for answer in assessment["answerArr"]:

					answerObj
                    = {}
					answerObj['is_active'] = True
					answerObj
                        ['company_assessment'] = answer['company_assessment']
					answerObj['transaction_type'] = answer['transaction_type']
					if not isV2:
						if
                        'answers' in answer:
							for ans in answer['answers']:
								answerObj['item_no'] = a \
                            ns['item_no']
								answerObj['answer'] = ans[ \
                        'answer_text'] if 'answer_text' in ans else None
								answerObj['question'] = ans['question']
					else:
                        answerObj['item_no'] = answer['item_no']

                    # cprint(answer['answer_text'].en
                        tf-8').strip());
						# c

                        llib.unquote(answer['answer_text'].encode('utf-8').str

                        code('utf8'));
						answerObj[
                            'answer'] = urllib. \

                    unquote( \
                        answer['answer_text'].encode('utf-8')
                            .strip()).decode( \
                            'utf8') if
                            'answer_text' in answer else None
						# answerObj['answer'] = urllib.unquote(answer['answer_text'])
                            'utf8') if 'answer_text' in answer else None
						answerObj[
                            'question'] = answer['question']

					if \
                            answerObj not in arrayAns:
						arrayAns.append( \

                            answerObj)
                                answer_form = Assessment_upload_answer_form( \
                            answerObj)

						if answer_form. \
                                is_valid():
							answer_form.save()

					if isV2:
						if not answer['uploaded_question']:
							answerNormal = {}
							choiceArr = []
                            answerNormal['is_active'] = True
							answerNormal['c
                            ssessment'] =
                                answer['company_assessment']

                    answerNormal[
                        'transaction_type'] = answer['trans
                            ype']
							answerNormal['upload
                                on'] = False
							a
                                al['question'] = answer['question']

							if 'choice' in answer:
								choiceArr.append( \
                            answer['choice'])
                                elif 'answer_text' in \
                            answer:
								answerNormal['text_answer'] = answer['

            r_text']

							an
        rNormal['choice'] = ch \
            Arr

							serializer = AnswerSerializer(data
            =answerNormal)
							if serializer.is_valid():

            serializer.save()
							else: 
								raise_error(json.dumps(serializer.
            errors))

					else:
						if'ploa \


d_question' not in answer:
							if 'uploaded_document' in answer:
								answer['choice'] = \
        []
								answer['uploaded
            stion'] = True

							s
            lizer = AnswerSerializer(data=answer)
							if serializer. \
            is_valid():
								serializer.save()
							else: 
								raise_error(json.dumps(s
            lizer.errors))

			return Response({})
		except Exception as e:
			exc_type, \

            exc_obj, exc_tb \
            = sys.exc_info()
			fname =
            os.path.split(exc_tb.tb_frame.
            f_code.co_filename)[1]

			cprint(e)
			cprint(fname)
			cprint(sys.exc_traceback.tb_lineno
            )
			return HttpResponse(e, status = 400)

class F \
            pload(APIView):
	# parser_classes
            ileUploadParser,)

	def put(self, request):
		try:
            files = request.FILES
			file_obj =
            files['file']
			company_assessment =

            request.data['company_assessment']
			transactio
            pe = request.data['transa
                _type']
			item_no =
            request. \
                data['item_no']
			question = request.data \

            ['question']
            is_active = request.data['is_a
            e']

			image_F = {}
			ima
        F['image'] = file_obj
            image_F["file
            "] = file_obj
			image_F["filelocation"] = file_obj


imageAnswer = {}
			imageAnswer[

    'image'] = file_obj
        imageAnswer
            ['company_asses
            t'] = company_assessment
			imageAnswer['
            tion'] = question
			imageAnswer['transaction_type'] = transaction_type

            imageAnswer['item_no'] = item_no
			imageAnswer['is_active'] = is_active

			s

            izer = AnswerImageSerializer( \
            data=imageAnswer)
			if serializer.is_valid():
				serializer.save()
			else:

            raise_error(json.dumps(serializer.errors))


			print file_obj
        	# do some stuff with uploaded file
			return

                Response(status=204)
		except
                Exception as e:
			print str(e)
			return Response( \

                    "imo mama kai " + str(e),status=500)
		


class LessonUpdate(APIView)
                    :

	def post(self, request):
		try:
			data = request.data
			lessonUpdateHeader = data['lessonUpdate']
			lessonUpdateDetails = lessonUpdateHeader.pop("lessonUpdat

                    s", None)

			if not lessonUpdateDetails: Response
                        ("No lesson update details",
                    status=400)

			# Save lesson update header
			lessonUpdateHeaderSerializer = LessonUpdat \

                rSerializer(data=le
            Updat
                r)

			if lessonUpdateHeaderSerializer.is_valid():
				lessonUpdateHe

        Saved = lessonUpdateHe \
            Serializer.save()

				# Save Lesson update details
				for lessonUpdateDetail in lessonUpdateDetails:
					
					lessonUpdateDetail['lesson_update_header'] = lessonUpdateHeaderSaved.pk
					lessonUpdateDetail['to_dos_topic'] = lessonUpdateDetail['lessonUpdateActivity']

					lessonUpdateDetailSerializer = LessonUpdateDetailSerializer(data=lessonUpdateDetail)

					if lessonUpdateDetailSerializer.is_valid():
						lessonUpdateDetailSerializer.save()
					else: 
						return Response(json.dumps(lessonUpdateDetailSerializer.errors), status=400)

				return Response({})
			else: 
				Response(json.dumps(lessonUpdateHeaderSerializer.errors), status=400)

		except Exception as e:
			return Response(str(e), status=500)
