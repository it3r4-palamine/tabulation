import base64
import os
import sys
from datetime import *

from django.contrib.postgres.fields import ArrayField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from ..models.multiple_choice import *


class Assessment_question(models.Model):
	value               = models.CharField(max_length=200, blank=True,null=True)
	is_active           = models.BooleanField(default=1)
	transaction_type    = models.ForeignKey("Transaction_type" ,null=True, blank=True, on_delete=models.CASCADE)
	is_multiple 	    = models.BooleanField(default=0)
	is_document         = models.BooleanField(default=0)
	parent_question     = models.ForeignKey("Assessment_question", null=True, blank=True, on_delete=models.CASCADE)
	has_follow_up		= models.BooleanField(default=0)
	code                = models.CharField(max_length=200, blank=True,null=True)
	is_import   	    = models.BooleanField(default=0)
	has_multiple_answer = models.BooleanField(default=0)
	is_general			= models.BooleanField(default=0)
	transaction_types	= ArrayField(models.IntegerField("Transaction_type"), blank=True, null=True)
	company 			= models.ForeignKey("Company", blank=True,null=True, on_delete=models.CASCADE)
	answer_type			= models.CharField(max_length=200, blank=True,null=True)
	has_related			= models.BooleanField(default=0)
	uploaded_question	= models.BooleanField(default=0)
	timer 				= models.DurationField(blank=True,null=True)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_questions"


	def get_dict(self, forAPI=False, imagesArr=None, isV2=False, is_local=False):
		try:
			assessment_question = {
				"id"				  	: self.pk,
				"code"	  			  	: self.code,
				"value"				  	: self.value,
				"is_multiple"		  	: self.is_multiple,
				"is_document"		  	: self.is_document,
				"has_multiple_answer" 	: self.has_multiple_answer,
				"is_general" 		  	: self.is_general,
				"has_follow_up" 	  	: self.has_follow_up,
				"code_value" 		  	: self.code + ": " + self.value,
				"answer_type" 		  	: self.answer_type,
				"has_related" 		  	: self.has_related,
				"uploaded_question"   	: self.uploaded_question,
				"timer"				  	: self.timer.total_seconds() if self.timer else None,
				"answers"			  	: [],
				"images"			  	: [],
				"transaction_type"	  	: None,
				"parent_question"	  	: self.parent_question
			}
			
			# Worksheet image
			if self.uploaded_question:
				imagesQ 	= []
				answersQ 	= []

				# For YIAS Android or Web
				if isV2 or not forAPI:
					images = Assessment_image.objects.filter(question=self.pk, is_active=True).order_by("order")
				else:
					ids = []
					if imagesArr:
						for excludeImages in imagesArr:
							ids.append(excludeImages['id'])

					# Get new images and convert to base64
					images = Assessment_image.objects.filter(question=self.pk, is_active=True).exclude(pk__in=ids).order_by("order")
					
				
				for image in images:
					assessmentImageDict = image.get_dict(True) if is_local else image.get_dict(isV2)

					if isV2:
						assessmentImageDict['questionId'] = assessment_question['id']
					elif not isV2 and forAPI:
						image = open('web_admin/static/uploads/%s'%(image.image), 'rb')
						image_read = image.read()
						image_64_encode = base64.standard_b64encode(image_read)
						assessmentImageDict['converted_image'] = image_64_encode
						assessmentImageDict['question'] = assessment_question['id']
					
					imagesQ.append(assessmentImageDict)

				# Convert old images to base64
				if imagesArr:
					for importImage in imagesArr:
						old_image 			= {}
						old_image['id'] 	= importImage['id']
						old_image['image'] 	= importImage['image']

						get_image 		= open('web_admin%s'%(importImage['image']), 'rb')
						get_image_read 	= get_image.read()

						get_image_64 					= base64.standard_b64encode(get_image_read)
						old_image['converted_image'] 	= get_image_64
						imagesQ.append(old_image)

				assessment_question['images'] = imagesQ

				# Get worksheet answers
				answers = Assessment_image_answer.objects.filter(question=self.pk, is_active=True).order_by("item_no")
				for answer in answers:
					answerDict = answer.get_dict()
					answersQ.append(answerDict)


				assessment_question['answers'] = answersQ

			if is_local:
				assessment_question["transaction_type"] = self.transaction_type.pk
				assessment_question["timer"] = self.timer
			else:
				assessment_question["transaction_type"] = self.transaction_type.id if forAPI else self.transaction_type.get_dict() if self.transaction_type else None

			if not forAPI:
				assessment_question["is_active"] = self.is_active
				assessment_question["is_import"] = self.is_import

			return assessment_question
			
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

			print(e)
			print(fname)
			print(sys.exc_traceback.tb_lineno)

			raise ValueError(e)


class Assessment_effect(models.Model):
	question  = models.ForeignKey("Assessment_question", on_delete=models.CASCADE)
	value     = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	is_import = models.BooleanField(default=0)
	company   = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_effects"

	def get_dict(self,forAPI=False):
		return {
			"id" 		: self.pk,
			"value" 	: self.value,
			"question"  : self.question.pk if forAPI else self.question.get_dict(),
			"is_active" : self.is_active,
			"is_import" : self.is_import,
		}


class Assessment_recommendation(models.Model):

	value     = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	is_import = models.BooleanField(default=0)
	company   = models.ForeignKey("Company",blank=True,null=True ,on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_recommendations"

	def get_dict(self):
		return {
			"id" 		: self.pk,
			"value" 	: self.value,
			"is_active" : self.is_active,
			"is_import" : self.is_import,
		}


class Assessment_answer(models.Model):

	question           = models.ForeignKey("Assessment_question" ,on_delete=models.CASCADE)
	company_assessment = models.ForeignKey("Company_assessment", on_delete=models.CASCADE)
	choice             = ArrayField(models.IntegerField("Choice"),blank=True,null=True)
	text_answer        = models.CharField(max_length=200,null=True,blank=True)
	document_image	   = ProcessedImageField(upload_to='assessment/document_images/',
									   processors=[ResizeToFit(1000,1000)],
									   format='PNG',
									   options = {'quality': 100},
									   blank=True,
									   null=True)
	transaction_type   = models.ForeignKey("Transaction_type",blank=True,null=True ,on_delete=models.CASCADE)
	company 		   = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)
	created_on 		   = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	is_deleted		   = models.BooleanField(default=0)
	uploaded_question  = models.BooleanField(default=0)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_answers"

	def get_dict(self,forAPI = False):
		assessment_answers = {
			"id" 		  : self.pk,
			"text_answer" : self.text_answer,
			# "document_image" : self.document_image if self.document_image else None
		}

		if not forAPI:
			assessment_answers['question'] = self.question.get_dict()
			assessment_answers['company_assessment'] = self.company_assessment.get_dict()
		else:
			assessment_answers['question'] = self.question.pk
			assessment_answers['transaction_type'] = self.transaction_type.pk if self.transaction_type else None
			assessment_answers['company_assessment'] = self.company_assessment.pk

			if self.document_image:
				image = open("web_admin/static/uploads/%s"%(self.document_image), 'rb')
				image_read = image.read()
				image_64_encode = base64.standard_b64encode(image_read)
				assessment_answers['converted_image'] = image_64_encode
			else:
				assessment_answers['converted_image'] = None

		choice = None
		if self.choice:
			# API
			if forAPI:
				if self.question.has_multiple_answer:
					choice = self.choice
				else: choice = self.choice[0]

			# WEB
			else: 
				if len(self.choice) > 0:
					choice = []
					for choices in self.choice:
						try:
							choice_instance = Choice.objects.get(id=choices,is_active=True)
						except Choice.DoesNotExist:
							continue

						choice.append(choice_instance.get_dict())
				else:
					try:
						choice_instance = Choice.objects.get(id=self.choice[0],is_active=True)
					except Choice.DoesNotExist:
						# continue
						cprint("err")

					choice = choice_instance.get_dict()

		assessment_answers['choice'] = choice

		return assessment_answers

class Assessment_finding(models.Model):
	question  = models.ForeignKey("Assessment_question", on_delete=models.CASCADE)
	value     = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	is_import = models.BooleanField(default=0)
	company   = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_findings"

	def get_dict(self,forAPI=False):
		return {
			"id" 		: self.pk,
			"value" 	: self.value,
			"question"  : self.question.pk if forAPI else self.question.get_dict(),
			"is_active" : self.is_active,
			"is_import" : self.is_import,
		}


class Generated_assessment_recommendation(models.Model):

	company_assessment = models.ForeignKey("Company_assessment", on_delete=models.CASCADE)
	recommendations    = ArrayField(models.IntegerField("Assessment_recommendation"),blank=True,null=True)
	company 		   = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "generated_assessment_recommendations"


class Related_question(models.Model):

	related_questions = ArrayField(models.IntegerField("Assessment_question"), blank=True, null=True)
	is_active 		  = models.BooleanField(default=1)
	is_import 		  = models.BooleanField(default=0)
	company 		  = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "related_questions"

	def get_dict(self):
		related_questions = {
			'id' 		: self.pk,
			'is_active' : self.is_active
		}

		questions = []
		for related_question in self.related_questions:
			try:
				question = Assessment_question.objects.get(id=related_question,is_active=True)
			except Assessment_question.DoesNotExist:
				continue

			question = question.get_dict()
			questions.append(question)

		related_questions['related_questions'] = questions

		return related_questions 


class Assessment_score(models.Model):

	company_assessment = models.ForeignKey("Company_assessment", on_delete=models.CASCADE)
	transaction_type   = models.ForeignKey("Transaction_type", on_delete=models.CASCADE)
	is_active 		   = models.BooleanField(default=1)
	score 			   = models.IntegerField(blank=True, null=True)
	question 		   = models.ForeignKey("Assessment_question",blank=True,null=True, on_delete=models.CASCADE)
	uploaded_question  = models.BooleanField(default=0)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_scores"

	def get_dict(self):
		return {
			'score' 			 : self.score,
			'transaction_type' 	 : self.transaction_type.get_dict(),
			'company_assessment' : self.company_assessment.get_dict(),
			'question' 			 : self.question.pk,
			'uploaded_question'  : self.uploaded_question,
		}


class Assessment_session(models.Model):

	company_assessment = models.ForeignKey("Company_assessment", on_delete=models.CASCADE)
	date 			   = models.DateField(blank=True,null=True)
	time_start		   = models.TimeField(auto_now=False, auto_now_add=False, blank = True, null = True)
	time_end		   = models.TimeField(auto_now=False, auto_now_add=False, blank = True, null = True)
	is_deleted 		   = models.BooleanField(default=0)
	transaction_type   = models.ForeignKey("Transaction_type",blank=True,null=True, on_delete=models.CASCADE)
	question 		   = models.ForeignKey("Assessment_question",blank=True,null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_sessions"

	def get_dict(self):
		return {
			'date' 			   : datetime.strptime(str(self.date), '%Y-%m-%d').date(),
			'time_start' 	   : self.time_start.strftime("%H:%M:%S"),
			'time_end' 		   : self.time_end.strftime("%H:%M:%S") if self.time_end else None,
			'transaction_type' : self.transaction_type.pk if self.transaction_type else None,
			'question' 		   : self.question.pk if self.question else None,
		}

class Assessment_image(models.Model):
	question  = models.ForeignKey("Assessment_question", on_delete=models.CASCADE)
	is_active = models.BooleanField(default=1)
	image 	  = ProcessedImageField(upload_to='assessment/questions/',
								   processors=[ResizeToFit(1000,1000)],
								   format='PNG',
								   options = {'quality': 100},
								   blank=True,
								   null=True)
	company   = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)
	order 	  = models.IntegerField(blank=True,null=True)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_images"


	def get_dict(self, isV2=False):
		questionImage = {
			"id" 		: self.pk,
			"question"	: self.question.pk,
			"order"		: self.order,
			"is_active"	: self.is_active,
		}

		# Image
		logo = ""

		if self.image == "" or self.image == None:
			logo = ""
		else:
			logo = "/static/uploads/"+str(self.image)

		questionImage['image'] = logo


		if isV2:
			imageList = logo.rsplit('/', 1)
			questionImage['imageName'] = imageList[1]

		return questionImage

class Assessment_image_answer(models.Model):
	question  = models.ForeignKey("Assessment_question", on_delete=models.CASCADE)
	is_active = models.BooleanField(default=1)
	item_no   = models.IntegerField(blank=True, null=True)
	answer    = models.CharField(max_length=200,blank=True,null=True)
	company   = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_image_answers"

	def get_dict(self):
		row = {
			'id' 	   : self.pk,
			'question' : self.question.pk,
			'item_no'  : self.item_no,
			'is_active': self.is_active,
		}

		# Answer
		multiple_image_answer_qs = Multiple_image_answer.objects.filter(image_answer=self.pk, is_active=True)
		multiple_image_answer_list = []

		for _multiple_image_answer in multiple_image_answer_qs:
			multiple_image_answer = _multiple_image_answer.get_dict(True)
			multiple_image_answer_list.append(multiple_image_answer)

		row['answer'] = multiple_image_answer_list


		return row

class Multiple_image_answer(models.Model):
	image_answer = models.ForeignKey("Assessment_image_answer", on_delete=models.CASCADE)
	name 		 = models.CharField(max_length=200,blank=True,null=True)
	is_active 	 = models.BooleanField(default=1)

	class Meta:
		app_label = "web_admin"
		db_table  = "multiple_image_answers"


	def get_dict(self, isV2=False):
		return {
			'id' 			: self.pk,
			'name' 			: self.name,
			'is_active' 	: self.is_active,
			'image_answer' 	: self.image_answer.pk,
		}


class Assessment_upload_answer(models.Model):
	question 		   = models.ForeignKey("Assessment_question", on_delete=models.CASCADE)
	is_active 		   = models.BooleanField(default=1)
	item_no 		   = models.IntegerField(blank=True,null=True)
	answer 			   = models.CharField(max_length=200,blank=True,null=True)
	answer_syntax	   = models.CharField(max_length=200,blank=True,null=True)
	transaction_type   = models.ForeignKey("Transaction_type", on_delete=models.CASCADE)
	company_assessment = models.ForeignKey("Company_assessment", on_delete=models.CASCADE)
	is_deleted 		   = models.BooleanField(default=0)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_upload_answers"

	def get_dict(self):
		return {
			'id' 				 : self.pk,
			'answer' 			 : self.answer,
			'answer_syntax'		 : self.answer_syntax,
			'item_no' 			 : self.item_no,
			'question' 			 : self.question.pk,
			'transaction_type' 	 : self.transaction_type.pk,
			'company_assessment' : self.company_assessment.pk,
		}

class Assessment_answer_image(models.Model):
	question 		   = models.ForeignKey("Assessment_question", on_delete=models.CASCADE)
	company_assessment = models.ForeignKey("Company_assessment", on_delete=models.CASCADE)
	transaction_type   = models.ForeignKey("Transaction_type", on_delete=models.CASCADE)
	image 			   = ProcessedImageField(upload_to='assessment/document_images/',
						   processors=[ResizeToFit(1000,1000)],
						   format='PNG',
						   options = {'quality': 100},
						   blank=True,
						   null=True)
	item_no 		   = models.IntegerField(blank=True,null=True)
	is_active 		   = models.BooleanField(default=1)
	is_sync			   = models.BooleanField(default=1)

	class Meta:
		app_label = "web_admin"
		db_table  = "assessment_answer_images"

	def get_dict(self, isV2=False):
		answerImage = {
			'id' 				 : self.pk,
			'company_assessment' : self.company_assessment.pk,
			'transaction_type'   : self.transaction_type.pk,
			'question' 			 : self.question.pk,
			'item_no' 			 : self.item_no,
			'is_active' 		 : self.is_active,
			'is_sync'			 : self.is_sync
		}

		if isV2:
			logo = "/static/uploads/"+str(self.image)
			imageList = logo.rsplit('/', 1)
			answerImage['answer_image'] = imageList[1]
		else:
			answerImage['image'] = "/static/uploads/"+str(self.image),

		return answerImage

	def get_image(self):
		return "/static/uploads/"+str(self.image)