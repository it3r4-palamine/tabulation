from rest_framework.response import Response
from django.http.response import HttpResponse
from django.db.models import Count, Sum, Avg,Min,Q,F,Func
import json
import ast
import decimal
from datetime import *
import sys, traceback, os

from utils import error_messages


def raise_error(msg = "Testing Stopper"):
    raise ValueError(msg)


def convert_24_12(time,get_object=False):
    if time is None:
        return ""

    results = {}
    epoch = datetime.utcfromtimestamp(0)
    converted_time = datetime.strptime(str(time), "%H:%M:%S")

    if get_object:
        converted_datetime = datetime.combine(DUMMYDATE,time)
        results["time"] = time.strftime("%I:%M %p")
        results["total_seconds"] = (converted_datetime - epoch).total_seconds() * 1000.0
        results["datetime"] = converted_datetime
        return results

    return converted_time


def filter_obj_to_q(obj,or_q = ()):
    q_filters = Q()
    for value in obj.items():
        if value[0] in or_q:
            q_filters |= Q((value[0],value[1]))
        else:
            q_filters &= Q((value[0],value[1]))

    return q_filters


def convert_date_key(filters,key):
    converted = {}
    for value in filters.items():
        if "date_from" in value:
            converted[key] = value[1]
        elif "date_to" in value:
            converted[key] = value[1]
        else:
            converted[value[0]] = value[1]

    return converted


def get_current_company(request):
    return request.user.company if request.user.company else None


def get_current_user(request):
    # Returns User/Student
    return request.user.id if request.user else None


def get_data(request):
    return json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}


def extract_json_data(request):
    post_params = json.loads(request.body.decode("utf-8"), parse_float=round_off_req_data) if request.body.decode(
        "utf-8") else {}
    return post_params


def extract_get_parameters(data):
    return ast.literal_eval(data)


def round_off_req_data(s):
    amount = decimal.Decimal(str(round(float(s), 2)))
    return amount


def success_response(response_data = error_messages.SUCCESS):
    return Response(response_data, status=200)


def error_response(response_data, show_line=False):

    if show_line:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    return Response(response_data, status=400)


def error_http_response(response_data,show_line=False):

    if show_line:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    return HttpResponse(content=response_data, status=400)


def error_response_with_email(request, exception, response_value="Something Went Wrong", show_line=False, email=True):
    if show_line:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    if email:
        send_error_email(request, exception)

    print(exception)
    return HttpResponse(response_value, status=400)


def mail_error(request, exception):
    send_error_email(request, exception)

def obj_dates_to_str(objs, remove_time=False):
    try:
        for key, value in objs.items():
            if isinstance(objs[key], idatetime.date):
                if isinstance(objs[key], datetime):
                    objs[key] = str(objs[key].date())
                else:
                    objs[key] = str(objs[key])

        objs = obj_decimal_to_float(objs)
        return objs
    except Exception as e:
        raise ValueError(e)

def query_params_object(objs, remove_time=False):
    try:
        for key, value in objs.items():

            if value == "true":
                objs[key] = True
            if value == "false":
                objs[key] = False

            if isinstance(objs[key], idatetime.date):

                if isinstance(objs[key], datetime):
                    objs[key] = str(objs[key].date())
                else:
                    objs[key] = str(objs[key])

        objs = obj_decimal_to_float(objs)
        return objs
    except Exception as e:
        raise ValueError(e)


def obj_decimal_to_float(objs):
    try:
        for key, value in objs.items():
            if isinstance(objs[key], decimal.Decimal):
                objs[key] = float(objs[key])

        return objs
    except Exception as e:
        raise ValueError(e)


def json_encode(var_list, use_list_function=True):
    if use_list_function:
        var_list = list(var_list)

    return json.dumps(var_list, cls=DecimalDateEncoder)


class DecimalDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return round(obj, settings.PRECISION)

        if isinstance(obj, idatetime.date):
            if isinstance(obj, datetime):
                return str(obj.date())
            else:
                return str(obj)

        return json.JSONEncoder.default(self, obj)
