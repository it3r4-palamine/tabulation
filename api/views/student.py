from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.response_handler import *
from utils.dict_types import *
from web_admin.models import User

class StudentInfo(APIView):

	def post(self,request):
		try:
			data = extract_json_data(request)


			student = { 
				"code" : "00001",
				"first_name" : "Vince",
				"middle_name" : "Mendiola",
				"session_credits_balance" : "86400",				
				"time_slots" : [
					{
						"day" : "M",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
					{
						"day" : "W",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
					{
						"day" : "F",
						"time_start" : "14:00",
						"time_end" : "15:00"
					},
				]
			}

			student2 = { 
				"code" : "00002",
				"first_name" : "Alde",
				"middle_name" : "Sabido",
				"session_credits_balance" : "18000",
				"time_slots" : [
					{
						"day" : "T",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
					{
						"day" : "TH",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
					{
						"day" : "F",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
				]
			}

			student3 = { 
				"code" : "00003",
				"first_name" : "Joshua",
				"middle_name" : "Salise",
				"session_credits_balance" : "3600",
				"time_slots" : [
					{
						"day" : "T",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
					{
						"day" : "TH",
						"time_start" : "14:00",
						"time_end" : "15:00"
					},
					{
						"day" : "S",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
				]
			}

			student4 = { 
				"code" : "00004",
				"first_name" : "Al Ryan",
				"middle_name" : "Acain",
				"session_credits_balance" : "0",
				"time_slots" : [
					{
						"day" : "W",
						"time_start" : "13:00",
						"time_end" : "14:00"
					},
				]
			}

			student5 = { 
				"code" : "00005",
				"first_name" : "Dhan Martin",
				"middle_name" : "Barbarona",
				"session_credits_balance" : "7200",
				"time_slots" : [],
				"special_reservations": [
					{
					"day" : "W",
					"time_start" : "15:00",
					"time_end" : "16:00" }
				]
			}

			student6 = { 
				"code" : "00006",
				"first_name" : "Barbie",
				"middle_name" : "Babida",
				"session_credits_balance" : "14400",
				"time_slots" : [
					{
						"day" : "F",
						"time_start" : "12:00",
						"time_end" : "14:00"
					},
				]
			}

			student7 = { 
				"code" : "00007",
				"first_name" : "Catherine Jean",
				"middle_name" : "Nocete",
				"session_credits_balance" : "28000",
				"time_slots" : [
					{
						"day" : "W",
						"time_start" : "12:00",
						"time_end" : "14:00"
					},
					{
						"day" : "M",
						"time_start" : "12:00",
						"time_end" : "14:00"
					},
					{
						"day" : "F",
						"time_start" : "12:00",
						"time_end" : "14:00"
					},
				],
				"special_reservations": [{
					"day" : "W",
					"time_start" : "15:00",
					"time_end" : "16:00"}
				]
			}



			if not "code" in data:
				array_student = []

				array_student.append(student)
				array_student.append(student2)
				array_student.append(student3)
				array_student.append(student4)
				array_student.append(student5)
				array_student.append(student6)
				array_student.append(student7)

				return Response(array_student)

			if data["code"] == "00001":
				return Response(student)

			if data["code"] == "00002":
				return Response(student2)

			if data["code"] == "00003":
				return Response(student3)

			if data["code"] == "00004":
				return Response(student4)

			if data["code"] == "00005":
				return Response(student5)

			if data["code"] == "00006":
				return Response(student6)

			if data["code"] == "00007":
				return Response(student7)
			else:
				return Response("Student not found")


		except Exception as e:
			print(e)
			return Response("ERROR")


@api_view(["POST"])
def get_students(request):
	try:
		results = {}
		records = []

		users = User.objects.filter(is_active=True,user_type=1)

		for user in users:
			records.append(user.get_dict(dict_type=DEVICE))

		results["records"] = records

		return success_response(results)
	except Exception as e:
		return error_http_response(str(e))


@api_view(["POST"])
def get_student(request):
	try:
		data = extract_json_data(request)
		results = {}
		records = []

		users = User.objects.filter(is_active=True, pk=data["student_id"])

		for user in users:
			row = user.get_dict(dict_type=DEVICE)
			row["enrolled_programs"] = user.get_active_enrolled_programs()
			records.append(row)

		results["records"] = records

		return success_response(results)
	except Exception as e:
		return error_http_response(str(e))

@api_view(["POST"])
def get_students_with_information(request):
    try:
        results = {}
        records = []

        users = User.objects.filter(is_active=True,user_type=1)

        for user in users:
        	row = user.get_dict(dict_type=DEVICE)
        	row["enrolled_programs"] = user.get_active_enrolled_programs()

        	if row["enrolled_programs"]:
        		records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_http_response(str(e))

@api_view(["POST"])
def save_student_time_logs(request):
	try:	
		data = req_data(request)

		return success_response("Success")
	except Exception as e:
		return error_http_response(str(e))


