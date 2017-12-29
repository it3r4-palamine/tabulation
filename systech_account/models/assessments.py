from django.db import models
from ..models.multiple_choice import *
# from ..models.company_assessment import *
from django.contrib.postgres.fields import ArrayField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from django.conf import settings
from datetime import *

import base64

class Assessment_question(models.Model):
	value               = models.CharField(max_length=200,blank=True,null=True)
	is_active           = models.BooleanField(default=1)
	transaction_type    = models.ForeignKey("Transaction_type",null=True,blank=True)
	is_multiple 	    = models.BooleanField(default=0)
	is_document         = models.BooleanField(default=0)
	parent_question     = models.ForeignKey("Assessment_question",null=True,blank=True)
	# parent_question		= models.ForeignKey("Assessment_question", null=True, blank=True)
	has_follow_up		= models.BooleanField(default=0)
	code                = models.CharField(max_length=200,blank=True,null=True)
	is_import   	    = models.BooleanField(default=0)
	has_multiple_answer = models.BooleanField(default=0)
	is_general			= models.BooleanField(default=0)
	transaction_types	= ArrayField(models.IntegerField("Transaction_type"),blank=True,null=True)
	company 			= models.ForeignKey("Company",blank=True,null=True)
	answer_type			= models.CharField(max_length=200,blank=True,null=True)
	has_related			= models.BooleanField(default=0)
	uploaded_question	= models.BooleanField(default=0)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_questions"


	def get_dict(self, forAPI=False):
		assessment_question = {
			"id": self.pk,
			"code": self.code,
			"value": self.value,
			"is_multiple": self.is_multiple,
			"is_document": self.is_document,
			"has_multiple_answer" : self.has_multiple_answer,
			"is_general" : self.is_general,
			"has_follow_up" : self.has_follow_up,
			"code_value" : self.code + ": " + self.value,
			"answer_type" : self.answer_type,
			"has_related" : self.has_related,
			"uploaded_question" : self.uploaded_question,
		}
		if self.parent_question:
			if forAPI:
				assessment_question["parent_question"] = self.parent_question.id
			else:
				assessment_question["parent_question"] = {
					'id' : self.parent_question.id,
					'code' : self.parent_question.code,
					'value' : self.parent_question.value,
					'code_value' :  self.parent_question.code + ": " + self.parent_question.value,
				}

		else:
			assessment_question["parent_question"] = None

		if self.has_related:
			related_questions = Related_question.objects.filter(related_questions__overlap=[self.pk],is_active=True)
			for related_question in related_questions:
				assessment_question['related_question'] = related_question.pk
			# print(related_question)
		
		if self.uploaded_question:
			imagesQ = []
			answersQ = []
			images = Assessment_image.objects.filter(question=self.pk,is_active=True)
			for image in images:
				imageList = image.get_dict()
				image = open('systech_account/static/uploads/%s'%(image.image), 'rb')
				image_read = image.read()
				# image_64_encode = base64.encodestring(image_read)
				image_64_encode = base64.standard_b64encode(image_read)
				# image_64_encode = base64.b64encode(image_read)
				imageList['converted_image'] = image_64_encode
				imagesQ.append(imageList)

			answers = Assessment_image_answer.objects.filter(question=self.pk,is_active=True).order_by("item_no")
			for answer in answers:
				answerList = answer.get_dict()
				answersQ.append(answerList)

			assessment_question['answers'] = answersQ
			assessment_question['images'] = imagesQ

		# Transaction Types
		if self.is_general:
			transaction_types = []
			for transaction_type_id in self.transaction_types:
				# try:
				# 	transaction_type = Transaction_type.objects.get(id=transaction_type_id, is_active=True)
				# except Transaction_type.DoesNotExist:
				# 	continue

				# transaction_type = transaction_type.id if forAPI else transaction_type.get_dict()
				# print(transaction_type)
				transaction_types.append(transaction_type_id)
			assessment_question['transaction_types'] = transaction_types
		else:
			assessment_question["transaction_type"] = self.transaction_type.id if forAPI else self.transaction_type.get_dict() if self.transaction_type else None

		if not forAPI:
			assessment_question["is_active"] = self.is_active
			assessment_question["is_import"] = self.is_import

		return assessment_question


class Assessment_effect(models.Model):
	question  = models.ForeignKey("Assessment_question")
	value     = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	is_import = models.BooleanField(default=0)
	company   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_effects"

	def get_dict(self,forAPI=False):
		return {
			"id" : self.pk,
			"value" : self.value,
			"question" : self.question.pk if forAPI else self.question.get_dict(),
			"is_active" : self.is_active,
			"is_import" : self.is_import,
		}

class Assessment_recommendation(models.Model):
	value     = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	is_import = models.BooleanField(default=0)
	company   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_recommendations"

	def get_dict(self):
		return {
			"id" : self.pk,
			"value" : self.value,
			"is_active" : self.is_active,
			"is_import" : self.is_import,
		}

class Assessment_answer(models.Model):
	question           = models.ForeignKey("Assessment_question")
	company_assessment = models.ForeignKey("Company_assessment")
	choice             = ArrayField(models.IntegerField("Choice"),blank=True,null=True)
	text_answer        = models.CharField(max_length=200,null=True,blank=True)
	document_image	   = models.ImageField(upload_to='assessment/document_images/', blank=True, null=True)
	transaction_type   = models.ForeignKey("Transaction_type",blank=True,null=True)
	company 		   = models.ForeignKey("Company",blank=True,null=True)
	created_on 		   = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	is_deleted		   = models.BooleanField(default=0)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_answers"

	def get_dict(self,forAPI = False):
		assessment_answers = {
			"id" : self.pk,
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
	question  = models.ForeignKey("Assessment_question")
	value     = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	is_import = models.BooleanField(default=0)
	company   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_findings"

	def get_dict(self,forAPI=False):
		return {
			"id" : self.pk,
			"value" : self.value,
			"question" : self.question.pk if forAPI else self.question.get_dict(),
			"is_active" : self.is_active,
			"is_import" : self.is_import,
		}

class Generated_assessment_recommendation(models.Model):
	company_assessment = models.ForeignKey("Company_assessment")
	recommendations    = ArrayField(models.IntegerField("Assessment_recommendation"),blank=True,null=True)
	company 		   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "generated_assessment_recommendations"

class Related_question(models.Model):
	related_questions = ArrayField(models.IntegerField("Assessment_question"),blank=True,null=True)
	is_active 		  = models.BooleanField(default=1)
	is_import 		  = models.BooleanField(default=0)
	company 		  = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "related_questions"

	def get_dict(self):
		related_questions = {
			'id' : self.pk,
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
	company_assessment = models.ForeignKey("Company_assessment")
	transaction_type   = models.ForeignKey("Transaction_type")
	is_active 		   = models.BooleanField(default=1)
	score 			   = models.IntegerField(blank=True, null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_scores"

	def get_dict(self):
		return {
			'score' : self.score,
			'transaction_type' : self.transaction_type.get_dict(),
			'company_assessment' : self.company_assessment.get_dict(),
		}

class Assessment_session(models.Model):
	company_assessment = models.ForeignKey("Company_assessment")
	date 			   = models.DateField(blank=True,null=True)
	time_start		   = models.TimeField(auto_now=False, auto_now_add=False, blank = True, null = True)
	time_end		   = models.TimeField(auto_now=False, auto_now_add=False, blank = True, null = True)
	is_deleted 		   = models.BooleanField(default=0)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_sessions"

	def get_dict(self):
		return {
			'date' : datetime.strptime(str(self.date), '%Y-%m-%d').date(),
			'time_start' : self.time_start.strftime("%H:%M:%S"),
			'time_end' : self.time_end.strftime("%H:%M:%S"),
		}

class Assessment_image(models.Model):
	question  = models.ForeignKey("Assessment_question")
	is_active = models.BooleanField(default=1)
	image 	  = ProcessedImageField(upload_to='assessment/questions/',
								   processors=[ResizeToFit(618,400)],
								   format='PNG',
								   options = {'quality': 80},
								   blank=True,
								   null=True)
	company   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_images"

	def get_dict(self):
		logo = ""
		if self.image == "" or self.image == None:
			logo = ""
		else:
			logo = "/static/uploads/"+str(self.image)

		return {
			'image' : logo,
			'id' : self.pk
		}

class Assessment_image_answer(models.Model):
	question  = models.ForeignKey("Assessment_question")
	is_active = models.BooleanField(default=1)
	item_no   = models.IntegerField(blank=True, null=True)
	answer    = models.CharField(max_length=200,blank=True,null=True)
	company   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "assessment_image_answers"

	def get_dict(self):
		return {
			'id' : self.pk,
			'question' : self.question.pk,
			'item_no' : self.item_no,
			'answer' : self.answer,
		}