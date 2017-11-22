from django.shortcuts import render, get_object_or_404,redirect
from django.utils.dateparse import parse_date
from django.db import models
from math import ceil,floor
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from random import randint
from datetime import datetime,timedelta,date
from copy import copy
import math,json,time,datetime as idatetime,copy as icopy,decimal,ast,csv,os,copy,re
from django.core import serializers
from operator import itemgetter
from decimal import Decimal
from time import mktime
from django.utils.termcolors import colorize
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str
from django.conf import settings
from collections import OrderedDict
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict
from django.apps import apps

from ..models.settings import *


def post_data(request):
	post_params = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}
	return post_params

class DecimalEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return float("%.14f" % obj)

		if isinstance(obj, idatetime.date):
			if isinstance(obj, datetime):
				return str(obj.date())
			else:
				return str(obj)

		return json.JSONEncoder.default(self, obj)

'''
	colored print in terminal
	str_to_print = The string that you want to print
	fg = color of the text (optional) (default to red)
	bg = background color of the text (optional) (default to white)
'''
def cprint(str_to_print, fg = "white", bg = "blue"):
	print(colorize(str_to_print, fg=fg, bg=bg))

def eprint(string, fg="white", bg="blue"):
	print ("======================================")
	print (colorize(string, fg=fg, bg=bg))
	print ("======================================")

def dprint(string):
	print ("======================================")
	print (string)
	print ("======================================")

'''
	Gets the current date and return depends on what format you want to return
'''

def current_date(to_return = None):
	if to_return == 'month':
		return datetime.today().month
	elif to_return == 'year':
		return datetime.today().year
	elif to_return == 'day':
		return datetime.today().day
	else:
		return datetime.today().date()


	
'''
	just call this function for testing stopper
	instead of calling raise ValueError('test'), just use raise_error() function
'''
def raise_error(msg = "Testing Stopper"):
	raise ValueError(msg)

# def success_list(listt):
# 	listt = listt if listt else []
# 	return HttpResponse(json_encode(listt), status = 200)

def success_obj(listt):
	listt = listt if listt else {}
	return HttpResponse(json_encode(listt), status = 200)

def success(to_return = "Successfully saved."):
	return HttpResponse(to_return, status = 200)

# def json_encode(listt):
# 	return json.dumps(list(listt))

def json_encode(var_list,use_list_function = True):
	if use_list_function:
		var_list = list(var_list)

	return json.dumps(var_list, cls = DecimalEncoder)

def success_list(to_return_list, to_list = True):
	if to_list:
		to_return_list = to_return_list if to_return_list else []
		to_return_list = list_dates_to_str(to_return_list)
	else:
		to_return_list = to_return_list if to_return_list else {}
		to_return_list = obj_dates_to_str(to_return_list)

	to_return_list = json_encode(to_return_list,to_list)

	return HttpResponse(to_return_list, status = 200, content_type="application/json")

def obj_dates_to_str(objs,remove_time = False):
	try:
		# for key,value in objs.items():
		# 	if isinstance(objs[key], idatetime.date):
		# 		if isinstance(objs[key], idatetime.date):
		# 			objs[key] = datetime.strptime(str(objs[key]), '%Y-%m-%d').date()
		# 		else:
		# 			objs[key] = str(objs[key])

		# objs = obj_decimal_to_float(objs)
		return objs
	except Exception as e:
		raise ValueError(e)

def list_dates_to_str(lists):
	results = []
	for value in lists:
		results.append(obj_dates_to_str(value))
	return results

def req_data(request,has_company = False, common_filter = False):
	post_params = json.loads(request.body.decode("utf-8"),parse_float=decimal.Decimal) if request.body.decode("utf-8") else {}
	if has_company:
		post_params["company"] = get_current_company(request)

	if common_filter:
		post_params["is_deleted"] = False



	return post_params

def get_current_company(request,company_obj = False):
	company = request.session.get('company_id',None)
	if company_obj:
		company = str_to_model("Company").objects.get(pk = company)
		# try:
		# 	company_settings = Company_settings.objects.get(company = company.pk)
		# except Company_settings.DoesNotExist:
		# 	raise e
	return company 

def get_display_terms(request):
	company = request.session.get('company_id',None)
	# display_terms = str_to_model("Display_setting").objects.filter(company=company).values("id","company_assessments","questions","transaction_types")
	try:
		display_terms = str_to_model("Display_setting").objects.get(company=company)
	except Display_setting.DoesNotExist:
		display_terms = None

	return display_terms

def error(to_return = "Something went wrong. Please contact your administrator"):
	return HttpResponse(to_return, status = 400)

def clean_string(strr,remove_delimeters = []): #remove spaces and delimeters
	strr = strr.strip()
	strr = ' '.join(strr.split())
	for delimeter in remove_delimeters:
		strr = strr.replace(delimeter,"")

	return strr

def list_to_string(arr,separator=","):
	return separator.join(map(str, arr))

def pagination(request):
	return render(request, 'common/pagination.html')

def generate_pagination(pagination_data,records):
	page = pagination_data["current_page"] - 1
	page_size = pagination_data["limit"]
	total_records = records.count()
	total_pages   = ceil(float(total_records) / page_size)
	starting = page * page_size 
	ending = page_size + starting
	dictt = {
		"total_records" : total_records,
		"total_pages" : total_pages,
		"starting" : starting,
		"ending" : ending,
	}
	return dictt

def str_to_model(model_str):
	model = apps.get_model(app_label='systech_account', model_name=model_str)
	return model