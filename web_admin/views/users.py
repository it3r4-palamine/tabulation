from ..forms.user_form import *
import unicodedata
from datetime import *

import requests
from django.db.models import ExpressionWrapper, DurationField

from utils.dict_types import *
from ..forms.user_form import *
from ..models.company_assessment import *
from ..models.enrollment import *
from ..views.common import *


def users(request):
    return render(request, 'users/users.html')


def create_dialog(request):
    return render(request, 'users/dialogs/create_dialog.html')

def create_student_dialog(request):
    return render(request, 'users/dialogs/create_student_dialog.html')

def create_user_dialog(request):
    return render(request, 'users/dialogs/create_user_dialog.html')

def change_pass_dialog(request):
    return render(request, 'users/dialogs/change_pass_dialog.html')


def user_credits_summary(request):
    return render(request, 'users/dialogs/user_credits_summary.html')

def read_students(request):
    try:
        results = {}
        records = []

        users = User.objects.filter(user_type__name="Student").order_by("id")

        for user in users:
            records.append(user.get_dict(dict_type=UI_SELECT))

        results["records"] = records

        return success_list(results, False)
    except Exception as e:
        return error(str(e))

def read_facilitators(request):
    try:
        results = {}
        records = []

        users = User.objects.filter(user_type__name="Facilitator", is_active=True).order_by("id")

        for user in users:
            records.append(user.get_dict(dict_type=UI_SELECT))

        results["records"] = records

        return success_list(results, False)
    except Exception as e:
        return error(str(e))


def read(request):
    try:
        data        = req_data(request, True)
        pagination  = None
        results     = dict(data=[])
        records     = []

        code        = data.pop("code", "")
        user_type   = data.pop("user_type", None)

        if 'pagination' in data:
            pagination = data.pop("pagination", None)

        filters = (Q(company=data['company'], is_active=True))

        if code:
            filters &= (Q(email__icontains=code) | Q(fullname__icontains=code))

        if user_type:
            filters &= Q(user_type=user_type["id"])

        queryset = User.objects.filter(filters).order_by("fullname")

        for qs in queryset:
            records.append(qs.get_dict())

        results['total_records'] = records

        if pagination:
            results.update(generate_pagination(pagination, queryset))
            records = records[results['starting']:results['ending']]

        results['data'] = records

        return success_list(results, False)
    except Exception as e:
        return error(e, show_line=True)


def create(request):
    try:
        postdata = req_data(request, True)
        if 'user_type' not in postdata:
            return error("User Type is required.")
        postdata['user_type'] = postdata['user_type']['id']
        try:
            instance = User.objects.get(id=postdata.get('id', None))
            user_type = AdminUserForm(postdata, instance=instance)
        except User.DoesNotExist:
            user_type = AdminUserForm(postdata)

        if user_type.is_valid():
            instance = user_type.save()

            results = {
                "record" : instance.get_dict(),
                "message" : "Successfully saved"
            }

            return success_list(results, False)
        else:
            return HttpResponse(user_type.errors, status=400)
    except Exception as err:
        return HttpResponse(err, status=400)


def delete(request, id=None):
    try:
        try:
            record = User.objects.get(pk=id)
            record.delete()
            record.save()
            return success("Successfully deleted.")
        except User.DoesNotExist:
            raise_error("User doesn't exist.")
    except Exception as e:
        return HttpResponse(e, status=400)


def read_user_types(request):
    try:
        data = req_data(request, True)
        records = UserType.objects.filter(company=data['company'], is_active=True).values("id", "name",
                                                                                           "is_active").order_by("id")
        return success_list(records)
    except Exception as e:
        return HttpResponse(e, status=400)


def change_password(request):
    try:
        data = req_data(request)
        instance = User.objects.get(id=data.get('id', None))
        data['is_active'] = True

        user_form = SetPasswordForm(data, instance=instance)
        if user_form.is_valid():
            new_password = user_form.cleaned_data['password2']
            instance.set_password(new_password)
            instance.save()

            return success("Password has been reset.")

        else:
            return error(user_form.errors)

    except Exception as e:
        return HttpResponse(e, status=400)


def read_user_credits(request):
    try:
        datus = req_data(request, True)
        results = {'data': []}
        data = []
        i = datetime.today()
        date_now = i.strftime('%Y-%m-%d')
        # user_credits = User_credit.objects.filter(program_id=datus['company_rename']['program_id'],user=datus['consultant']['id'])
        user_credits = UserCredit.objects.filter(
            program_id=datus['company_rename']['program_id'],
            user=datus['consultant']['id'],
            session_start_date__lte=date_now,
            session_end_date__gte=date_now,
        )
        for user_credit in user_credits:
            row = user_credit.get_dict()
            data.append(row)

        if not user_credits:
            enrollments = Enrollment.objects.filter(
                user=datus['consultant']['id'],
                session_start_date__lte=date_now,
                session_end_date__gte=date_now,
                company_rename=datus['company_rename']['id'],
                )

            for enrollment in enrollments:
                datus = enrollment.get_dict()
                datus['session_credits'] = datus['session_credits_seconds']
                data.append(datus)
        results['data'] = data
        return success_list(results, False)
    except Exception as e:
        return HttpResponse(e, status=400)


def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD', unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()


def view_lesson_update(request):
    try:
        data = req_data(request, True)
        results = {'data': []}

        lesson_updates = User_lesson_update.objects.filter(user=data['user_id'], is_active=True,
                                                           to_dos_topic=data['topic_id']).order_by("date")

        data = []
        for lesson_update in lesson_updates:
            row = lesson_update.get_dict()
            data.append(row)

        results['data'] = data
        return success_list(results, False)
    except Exception as e:
        return HttpResponse(e, status=400)


def read_user_reconciled_credits(request):
    try:
        results = {"yias": [], "yiss": []}
        data = req_data(request)

        user_credits = UserCredit.objects.filter(user=data["id"])

        yias_credits = []
        for user_credit in user_credits:
            row = user_credit.get_dict()

            company_rename = Company_rename.objects.filter(program_id=row['program_id']).first()
            row["program_name"] = company_rename.name if company_rename else "No Program"

            assessments = Company_assessment.objects.filter(consultant=data['id'],company_rename=company_rename.id).aggregate(
                total_time_consumed=models.Sum(
                    ExpressionWrapper(F('session_credits') - F('credits_left'), output_field=DurationField())))

            session_credits = row.get("session_credits", 0)
            yiss_consumed = row.get("session_credits_left", 0)
            assessments_total_seconds = assessments["total_time_consumed"].total_seconds() if assessments["total_time_consumed"] else 0

            row["session_credits"] = format_time_consumed(session_credits)
            row["yiss_consumed"] = format_time_consumed(yiss_consumed)
            row["total_time_consumed"] = format_time_consumed(assessments_total_seconds)

            total_reconciled_credits = float(session_credits) - (float(yiss_consumed) + float(assessments_total_seconds))

            row['credits_left_reconciled'] = format_time_consumed(total_reconciled_credits)

            yias_credits.append(row)

        results["yias"] = yias_credits

        return success_list(results, False)
    except Exception as e:
        return HttpResponse(e, status=400)


def reconcile_student_credits(request):
    try:
        results = {}
        url = 'http://35.185.70.123/api/read_student_credits/'
        headers = {'content-type': 'application/json'}
        data = {"complete_detail": True}
        result = requests.post(url, data=json.dumps(data), headers=headers)
        result.encoding = 'ISO-8859-1'
        records = result.json()

        for record in records:

            for enrollment in record["enrollments"]:
                user_credits = UserCredit.objects.filter(enrollment_id=enrollment["enrollment_id"]).first()

                if user_credits:
                    user_credits.session_credits_left = timedelta(seconds=enrollment['credits_consumed']) if enrollment[
                                                                                                             'credits_consumed'] > 0 else timedelta(
                        seconds=enrollment['credits_consumed'])
                    user_credits.save()

        return HttpResponse("Reconcile Complete", status=200)
    except Exception as e:
        return HttpResponse(e, status=400)


def get_intelex_students(request):
    try:
        datus = req_data(request, True)
        url = 'http://35.185.70.123/api/read_enrolled_students/'
        headers = {'content-type': 'application/json'}
        data = {"complete_detail": True}
        result = requests.post(url, data=json.dumps(data), headers=headers)
        result.encoding = 'ISO-8859-1'
        records = result.json()

        for record in records["records"]:
            first_name = record.get("first_name", "student_")
            last_name = record.get("last_name", "code")

            first_name = first_name.encode('UTF-8').strip()
            first_name = first_name.decode('UTF-8')

            last_name = last_name.encode('UTF-8').strip()
            last_name = last_name.decode('UTF-8')

            last_name = elimina_tildes(last_name)
            first_name = elimina_tildes(first_name)
            username = '%s%s' % (first_name.lower(), last_name.lower())
            username = username.replace(" ", "").replace(".", "")

            email_add = username + "@gmail.com"
            user_id = None
            user_exists = User.objects.filter(username__iexact=username, is_active=True).first()
            if user_exists:
                user_id = user_exists.pk
                if 'enrollments' in record:
                    for credits in record['enrollments']:
                        session_credits = credits["session_credits"]

                        user_credits = {'user': user_id, 'enrollment_id': credits['enrollment_id'],
                                        'program_id': credits['program_id'], 'program_name': credits["program"]["name"],
                                        'session_start_date': datetime.strptime(credits['session_start_date'],
                                                                                '%Y-%m-%d').date(),
                                        'session_end_date': datetime.strptime(credits['session_end_date'],
                                                                              '%Y-%m-%d').date(),
                                        'enrollment_code': credits["code"],
                                        "session_credits": timedelta(seconds=credits['total_time_left_seconds']) if \
                                            credits['total_time_left_seconds'] > 0 else timedelta(
                                            seconds=credits['session_credits'])}
                        try:
                            instance = UserCredit.objects.get(enrollment_id=credits['enrollment_id'])
                            user_credits_form = User_credit_form(user_credits, instance=instance)
                        except UserCredit.DoesNotExist:
                            user_credits_form = User_credit_form(user_credits)

                        if user_credits_form.is_valid():
                            user_credits_form.save()
                continue
            else:
                student_user = UserType.objects.filter(is_active=True, company=datus['company'],
                                                       name="Student").first()
                if student_user:
                    record['user_type'] = student_user.pk
                else:
                    return error("No Student user type. Please go to User Types Settings.")
                record["email"] = email_add
                record["fullname"] = record["first_name"] + record["last_name"]
                record["user_intelex_id"] = record["id"]
                record["username"] = username
                record["password1"] = username
                record["password2"] = username
                record["is_intelex"] = True
                record["is_active"] = True
                record["session_credits"] = timedelta(
                    milliseconds=record["session_credits"]) if "session_credits" in record and record[
                    "session_credits"] else 0
                record["company"] = get_current_company(request)

                user_type = StudentUserForm(record)

                if user_type.is_valid():
                    user_account = user_type.save()
                    user_id = user_account.pk
                    if 'enrollments' in record:
                        for credits in record['enrollments']:
                            session_credits = credits["session_credits"]
                            user_credits = {'user': user_id, 'enrollment_id': credits['enrollment_id'],
                                            'program_id': credits['program_id'],
                                            'session_start_date': datetime.strptime(credits['session_start_date'],
                                                                                    '%Y-%m-%d').date(),
                                            'session_end_date': datetime.strptime(credits['session_end_date'],
                                                                                  '%Y-%m-%d').date(),
                                            "session_credits": timedelta(seconds=credits['total_time_left_seconds']) if \
                                                credits['total_time_left_seconds'] > 0 else timedelta(
                                                seconds=credits['session_credits'])}
                            try:
                                instance = UserCredit.objects.get(enrollment_id=credits['enrollment_id'])
                                user_credits_form = User_credit_form(user_credits, instance=instance)
                            except UserCredit.DoesNotExist:
                                user_credits_form = User_credit_form(user_credits)

                            if user_credits_form.is_valid():
                                user_credits_form.save()
                            else:
                                print(user_credits_form)
                else:
                    print(user_type)
        return HttpResponse("Successfully saved.", status=200)
    except Exception as e:
        return HttpResponse(e, status=400)


def format_time_consumed(time_seconds):
    # Converts Seconds to HH:MM:SS

    if time_seconds is None:
        return "Incomplete Logs"

    m, s = divmod(time_seconds, 60)
    h, m = divmod(m, 60)

    return "%d:%02d:%02d" % (h, m, s)
