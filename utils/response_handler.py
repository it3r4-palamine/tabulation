from rest_framework.response import Response
from django.http.response import HttpResponse
import json
import ast
import decimal



def extract_json_data(request):
    post_params = json.loads(request.body.decode("utf-8"), parse_float=round_off_req_data) if request.body.decode(
        "utf-8") else {}
    return post_params

def extract_get_parameters(data):
    return ast.literal_eval(data)

def round_off_req_data(s):
    amount = decimal.Decimal(str(round(float(s), 2)))
    return amount


def success_response(response_data):
    return Response(response_data, status=200)


def error_response(response_data):
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
