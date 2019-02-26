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

# MODELS
from systech_account.models.company_assessment import *
from systech_account.models.assessments import *
from systech_account.models.multiple_choice import *

# FORMS
from systech_account.forms.assessments import *
from systech_account.forms.user_form import *

# OTHERS
from api.serializers import *
from django.db.models import *
from systech_account.views.common import *
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
        try:
            request_data = request.data
            serializer = self.serializer_class(data=request_data, context={'request': request})
            
            if not serializer.is_valid():
                print serializer.errors
                if serializer.errors.get("non_field_errors", None) and serializer.errors["non_field_errors"][0] == "Unable to log in with provided credentials.":
                    return Response("Invalid Username/Password", status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            if not request_data.get("from_yias_local", None):
                # Create log of mobile app usages
                userlog = {
                    "user" : user.id,
                    "device" : request_data.get("device", "Android")
                }

                user_log_form = UserLogForm(userlog)
                if user_log_form.is_valid(): user_log_form.save()
            else:
                message = ""
                if not user.is_active: message = "Account Inactive. Please activate your account."
                if not user.is_admin or not user.user_type or user.user_type.pk != 3: message = "Invalid account.."
                if message: return Response(message, status=status.HTTP_400_BAD_REQUEST)

            return Response({ 'token': token.key })

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print_error(filename, "ObtainAuthToken", e, sys.exc_traceback.tb_lineno)
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_company_and_user_types(APIView):
    def post(self, request, *args, **kwargs):
        try:
            company = request.user.company.get_dict()
            user_types_qs = User_type.objects.filter(company=company["id"], is_active=True).values()

            response_data = {
                "company": company,
                "user_types": user_types_qs,
                "user": request.user.get_dict(True),
            }

            return Response(response_data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print_error(filename, "Get_company_and_user_types", e, sys.exc_traceback.tb_lineno)
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Base64
class GetBase64Photo(APIView):

    def post(self, request):
        try:
            print("here")
            assessmentImage = Assessment_image.objects.filter(question=21, is_active=True).first()

            image = open('systech_account/static/uploads/%s'%(assessmentImage.image), 'rb')
            image_read = image.read()
            image_64_encode = base64.standard_b64encode(image_read)

            data = {}
            data['image'] = image_64_encode

            return Response(data)

        except Exception as e:
            print(e)
            return Response(str(e), status = 500)

# Actual File
class GetPhoto(APIView):

    def post(self, request):
        try:
            assessmentImage = Assessment_image.objects.filter(question=21, is_active=True).first()
            image = open('systech_account/static/uploads/%s'%(assessmentImage.image), 'rb')

            return HttpResponse(image, content_type="image/png")

        except Exception as e:
            print(e)
            return Response(str(e), status = 500)

# Final
class GetQuestionPhoto(APIView):

    def post(self, request):
        data = req_data(request, True)

        path = os.path.join(settings.STATIC_ROOT, data["imageLocation"][8:])

        if os.path.exists(path):
            image = open(path, 'rb')
            return HttpResponse(image, content_type="image/png")
        else:
            return Response("File does not exists", status=status.HTTP_404_NOT_FOUND)
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
        image = open('systech_account/static/uploads/assessment/document_images/%s'%(data['imageLocation']), 'rb')

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


# SYNCING OF ASSESSMENTS, ANSWERS, SCORES AND QUESTION TIME
class SyncAssessments(APIView):

    def post(self, request, *args, **kwargs):
        try:
            if 'isV2' in request.data and request.data['isV2']:
                isV2 = request.data['isV2']
                completedAssessments = request.data['data']
            else:
                isV2= False
                completedAssessments = request.data

            for assessment in completedAssessments:

                # Update Assessment Status
                assessmentInstance = Company_assessment.objects.get(id=assessment["id"])

                if assessment['sync'] == False:
                    if assessmentInstance.is_synced == False:
                        assessmentInstance.is_synced = False
                    else:
                        assessmentInstance.is_synced = True
                else:
                    assessmentInstance.is_synced = True

                assessmentInstance.is_complete = assessment['is_complete']

                # Credits Left
                if assessment['credits_left']:
                    assessmentInstance.credits_left = timedelta(seconds=assessment['credits_left'])
                else:
                    if assessment['credits_left'] == 0:
                        assessmentInstance.credits_left = timedelta(seconds=assessment['credits_left'])


                assessmentInstance.save()

                for t_type in assessment['t_types']:
                    datus = {
                        'transaction_type' : t_type['transactionType'],
                        'company_assessment' : t_type['assessment'],
                        'is_active' : True,
                    }

                    # if 'score' in t_type:
                    if 'scores' in t_type and t_type['scores']:
                        for score in t_type['scores']:
                            datus['question'] = score['id']
                            datus['score'] = score['score']
                            # datus['uploaded_question'] = False if 'not_uploaded_question' in score else True
                            datus['uploaded_question'] = True

                            try:
                                instance = Assessment_score.objects.get(company_assessment=t_type['assessment'],transaction_type=t_type['transactionType'],is_active=True,question=score['id'],uploaded_question=True)
                                assessment_score_form = Assessment_score_form(datus, instance=instance)
                            except Assessment_score.DoesNotExist:
                                assessment_score_form = Assessment_score_form(datus)

                            if assessment_score_form.is_valid():
                                assessment_score_form.save()
                            else: Response(assessment_score_form.errors,status=status.HTTP_400_BAD_REQUEST)

                    elif 'score' in t_type and t_type['score']:
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

                sessionsQs = Assessment_session.objects.filter(company_assessment=assessmentInstance.id,is_deleted=False)

                for sessionsQ in sessionsQs:
                    sessionsQ.is_deleted = True
                    sessionsQ.save()

                for session in assessment['session']:
                    if 'time_end' not in session:
                        time_end_final = (datetime.strptime(str(session['time_start']), '%H:%M:%S')) + timedelta(minutes=10)
                        time_end_final = (datetime.strptime(str(time_end_final), '%Y-%m-%d %H:%M:%S').time())
                    else:
                        time_end_final = session['time_end']
                    sessions = {
                        'company_assessment' : session['assessment_id'],
                        'date' : session['date'],
                        'time_start' : session['time_start'],
                        # 'time_end' : session['time_end'] if 'time_end' in session else (datetime.strptime(str(session['time_start']), '%H:%M:%S')) + timedelta(minutes=10),
                        'time_end' : time_end_final,
                        'transaction_type' : session['transactionType'],
                        'question' : session['question'] if 'question' in session else None
                    }

                    session_form = Assessment_session_form(sessions)
                    if session_form.is_valid():
                        session_form.save()
                    else: Response(session_form.errors,status=status.HTTP_400_BAD_REQUEST)

                answersQs = Assessment_answer.objects.filter(company_assessment=assessmentInstance.id)
                for answersQ in answersQs:
                    answersQ.is_deleted = True
                    answersQ.save()

                imageAnswersQs = Assessment_upload_answer.objects.filter(company_assessment=assessmentInstance.id,is_deleted=False)

                for imageAnswersQ in imageAnswersQs:
                    imageAnswersQ.is_deleted = True
                    imageAnswersQ.save()

                # Save Assessment Answers
                arrayAns = []
                for answer in assessment["answerArr"]:

                    answerObj = {}
                    answerObj['is_active'] = True
                    answerObj['company_assessment'] = answer['company_assessment']
                    answerObj['transaction_type'] = answer['transaction_type']
                    if not isV2:
                        if 'answers' in answer:
                            for ans in answer['answers']:
                                answerObj['item_no'] = ans['item_no']
                                answerObj['answer'] = ans['answer_text'] if 'answer_text' in ans else None
                                answerObj['question'] = ans['question']
                    else:
                        answerObj['item_no'] = answer['item_no']
                        # cprint(answer['answer_text'].encode('utf-8').strip());
                        # cprint(urllib.unquote(answer['answer_text'].encode('utf-8').strip()).decode('utf8'));
                        answerObj['answer'] = urllib.unquote(answer['answer_text'].encode('utf-8').strip()).decode('utf8') if 'answer_text' in answer else None
                        # answerObj['answer'] = urllib.unquote(answer['answer_text']).decode('utf8') if 'answer_text' in answer else None
                        answerObj['question'] = answer['question']

                    if answerObj not in arrayAns:
                        arrayAns.append(answerObj)

                        answer_form = Assessment_upload_answer_form(answerObj)

                        if answer_form.is_valid():
                            answer_form.save()

                    if isV2:
                        if not answer['uploaded_question']:
                            answerNormal = {}
                            choiceArr = []
                            answerNormal['is_active'] = True
                            answerNormal['company_assessment'] = answer['company_assessment']
                            answerNormal['transaction_type'] = answer['transaction_type']
                            answerNormal['uploaded_question'] = False
                            answerNormal['question'] = answer['question']

                            if 'choice' in answer:
                                choiceArr.append(answer['choice'])
                            elif 'answer_text' in answer:
                                answerNormal['text_answer'] = answer['answer_text']

                            answerNormal['choice'] = choiceArr

                            serializer = AnswerSerializer(data=answerNormal)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                raise_error(json.dumps(serializer.errors))

                    else:
                        if 'uploaded_question' not in answer:
                            if 'uploaded_document' in answer:
                                answer['choice'] = []
                                answer['uploaded_question'] = True

                            serializer = AnswerSerializer(data=answer)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                raise_error(json.dumps(serializer.errors))

            return Response({})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(e)
            print(fname)
            print(sys.exc_traceback.tb_lineno)
            return HttpResponse(e, status = 400)

class FileUpload(APIView):
    # parser_classes = (FileUploadParser,)

    def put(self, request):
        try:
            files = request.FILES
            file_obj = files['file']
            company_assessment = request.data['company_assessment']
            transaction_type = request.data['transaction_type']
            item_no = request.data['item_no']
            question = request.data['question']
            is_active = request.data['is_active']

            image_F = {}
            image_F['image'] = file_obj
            image_F["filename"] = file_obj
            image_F["filelocation"] = file_obj

            imageAnswer = {}
            imageAnswer['image'] = file_obj
            imageAnswer['company_assessment'] = company_assessment
            imageAnswer['question'] = question
            imageAnswer['transaction_type'] = transaction_type
            imageAnswer['item_no'] = item_no
            imageAnswer['is_active'] = is_active

            serializer = AnswerImageSerializer(data=imageAnswer)
            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(json.dumps(serializer.errors))


            print file_obj
            # do some stuff with uploaded file
            return Response(status=204)
        except Exception as e:
            print str(e)
            return Response("" + str(e),status=500)


class FileUploadIOS(APIView):

    def post(self, request):
        try:
            data = request.data
            data = data['data']

            for answerImage in data:
                serializer = AnswerImageIOSSerializer(data=answerImage)
                if serializer.is_valid():
                    serializer.save()
                else: Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({})
        except Exception as e:
            return Response(str(e),status=500)



class LessonUpdate(APIView):

    def post(self, request):
        try:
            data = request.data
            lessonUpdateHeader = data['lessonUpdate']
            lessonUpdateDetails = lessonUpdateHeader.pop("lessonUpdateDetails", None)

            if not lessonUpdateDetails: Response("No lesson update details", status=400)

            # Save lesson update header
            lessonUpdateHeaderSerializer = LessonUpdateHeaderSerializer(data=lessonUpdateHeader)

            if lessonUpdateHeaderSerializer.is_valid():
                lessonUpdateHeaderSaved = lessonUpdateHeaderSerializer.save()

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