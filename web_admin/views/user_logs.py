from ..forms.user_form import *
from ..views.common import *

def user_logs(request):
    return render(request, "user_logs/user_logs.html")


def read(request):
    try:
        data = req_data(request, True)
        pagination = None

        code = data.pop("code", "")

        if 'pagination' in data:
            pagination = data.pop("pagination", None)

        records = UserLogs.objects.order_by("id")
        results = {'data': []}
        results['total_records'] = records.count()

        if pagination:
            results.update(generate_pagination(pagination, records))
            records = records[results['starting']:results['ending']]
        data = []

        for record in records:
            row = {}
            row['id'] = record.pk
            row['fullname'] = record.user.fullname
            row['date_login'] = record.date_login
            row["device"] = record.device

            data.append(row)
        results['data'] = data
        return success_list(results, False)
    except Exception as e:
        return HttpResponse(e, status=400)
