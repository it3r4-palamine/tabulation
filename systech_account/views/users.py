from ..forms.transaction_types import *
from ..models.transaction_types import *
from ..forms.user_form import *
from ..models.user import *
from ..views.common import *
from datetime import *
import requests


def users(request):
	return render(request, 'users/users.html')

def create_dialog(request):
	return render(request, 'users/dialogs/create_dialog.html')

def change_pass_dialog(request):
	return render(request, 'users/dialogs/change_pass_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']
		records = User.objects.filter(**filters).order_by("id")
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]
		data = []
		for record in records:
			row = {}
			row['id'] = record.pk
			row['email'] = record.email
			row['fullname'] = record.fullname
			row['is_active'] = record.is_active
			row['is_admin'] = record.is_admin
			row['password'] = record.password
			row['is_edit'] = record.is_edit
			if record.user_type:
				row['user_type'] = record.user_type.get_dict()
			data.append(row)
		results['data'] = data
		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = req_data(request,True)
		if 'user_type' not in postdata:
			return error("User Type is required.")
		postdata['user_type'] = postdata['user_type']['id']
		try:
			instance = User.objects.get(id=postdata.get('id',None))
			user_type = CustomUserChangeForm(postdata,instance=instance)
		except User.DoesNotExist:
			user_type = CustomUserCreationForm(postdata)

		if user_type.is_valid():
			user_type.save()
			return HttpResponse("Successfully saved.",status=200)
		else:
			return HttpResponse(user_type.errors,status=400)
	except Exception as err:
		return HttpResponse(err,status=400)

def delete(request,id = None):
	try:
		try:
			record = User.objects.get(pk=id)
			record.delete()
			record.save()
			return success("Successfully deleted.")
		except User.DoesNotExist:
			raise_error("User doesn't exist.")
	except Exception as e:
		return HttpResponse(e,status=400)

def read_user_types(request):
	try:
		data = req_data(request,True)
		records = User_type.objects.filter(company=data['company'],is_active=True).values("id","name","is_active").order_by("id")
		return success_list(records)
	except Exception as e:
		return HttpResponse(e,status=400)

def change_password(request):
	try:
		data = req_data(request)
		instance = User.objects.get(id=data.get('id',None))
		data['is_active'] = True

		user_form = SetPasswordForm(data,instance=instance)
		if user_form.is_valid():
			new_password = user_form.cleaned_data['password2']
			instance.set_password(new_password)
			instance.save()
			
			return success("Password has been reset.")

		else:
			return error(user_form.errors)

		if request.method == "POST":
			try:
				user_data = req_data(request)
				user_data['is_active'] = True
				user_form = CustomUserChangeForm(data=user_data, instance=request.user)
				if user_form.is_valid():
					user_form.save()
					return success("Account editing success!")
				else:
					print(user_form.errors)
					return error(user_form.errors)
			except Exception, e:
				return error(e)
		else: return error("Invalid request method")
	except Exception as e:
		return HttpResponse(e,status=400)

def read_user_credits(request):
	try:
		datus = req_data(request,True)
		results = {'data':[]}
		data = []
		user_credits = User_credit.objects.filter(program_id=datus['company_rename']['program_id'],user=datus['consultant']['id'])
		for user_credit in user_credits:
			row = user_credit.get_dict()
			data.append(row)
		results['data'] = data
		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e,status=400)

def get_intelex_students(request):
	try:
		datus = req_data(request,True)
		url = 'http://192.168.1.69:8000/api/read_enrolled_students/'
		headers = {'content-type': 'application/json'}
		data = {"complete_detail": True}
		result = requests.post(url, data=json.dumps(data), headers=headers)
		result.encoding = 'ISO-8859-1'
		records = result.json()

		for record in records["records"]:
			cprint(record)
			student = record.pop("student", None)
			first_name = student.get("first_name", "student_")
			last_name = student.get("last_name", "code")
			username = '%s%s' % (first_name.lower(), last_name.lower()) 
			username = username.replace(" ", "")
			

			email_add = username + "@gmail.com"
			user_id = None
			user_exists = User.objects.filter(email__iexact=email_add,is_active=True).first()
			if user_exists:
				user_id = user_exists.pk

				for credits in record['enrollments']:
					session_credits = credits["session_credits"]
					user_credits = {
						'user' : user_id,
						'enrollment_id' : credits['enrollment_id'],
						'program_id' : credits['program_id'],
						'session_start_date' : datetime.strptime(credits['session_start_date'], '%Y-%m-%d').date(),
						'session_end_date' : datetime.strptime(credits['session_end_date'], '%Y-%m-%d').date(),
						# 'session_credits' : credits['session_credits']
					}
					user_credits["session_credits"]  = timedelta(seconds=credits['session_credits'])
					try:
						instance = User_credit.objects.get(enrollment_id=credits['enrollment_id'])
						user_credits_form = User_credit_form(user_credits,instance=instance)
					except User_credit.DoesNotExist:
						user_credits_form = User_credit_form(user_credits)

					if user_credits_form.is_valid():
						user_credits_form.save()
					else:
						print user_credits_form
				continue
			else:
				student_user = User_type.objects.filter(is_active=True,company=datus['company'],name="Student").first()
				if student_user:
					student['user_type'] = student_user.pk
				else:
					return error("No Student user type. Please go to User Types Settings.")
				student["email"] = email_add
				student["fullname"] = student["full_name"]
				student["user_intelex_id"] = student["id"]
				student["password1"] = username
				student["password2"] = username
				student["is_intelex"] = True
				student["is_active"] = True
				# student["session_credits"] = timedelta(milliseconds=record["session_credits"])
				student["company"] = get_current_company(request)

				print student

				user_type = StudentUserForm(student)

				if user_type.is_valid():
					print "test"
					user_account = user_type.save()
					user_id = user_account.pk
					for credits in record['enrollments']:
						session_credits = credits["session_credits"]
						user_credits = {
							'user' : user_id,
							'enrollment_id' : credits['enrollment_id'],
							'program_id' : credits['program_id'],
							'session_start_date' : datetime.strptime(credits['session_start_date'], '%Y-%m-%d').date(),
							'session_end_date' : datetime.strptime(credits['session_end_date'], '%Y-%m-%d').date(),
							# 'session_credits' : credits['session_credits']
						}
						user_credits["session_credits"]  = timedelta(seconds=credits['session_credits'])
						try:
							instance = User_credit.objects.get(enrollment_id=credits['enrollment_id'])
							user_credits_form = User_credit_form(user_credits,instance=instance)
						except User_credit.DoesNotExist:
							user_credits_form = User_credit_form(user_credits)

						if user_credits_form.is_valid():
							user_credits_form.save()
						else:
							print user_credits_form
				else:
					print user_type
		return HttpResponse("Successfully saved.", status=200)
	except Exception as e:
		print e
		return HttpResponse(e,status=400)