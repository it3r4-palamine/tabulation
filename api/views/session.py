from rest_framework.decorators import api_view
from rest_framework.views import APIView
from web_admin.models.session import *
from api.serializers.session import *


class SessionAPIView(APIView):

    def post(self, request):
        try:
            data    = extract_json_data(request)
            company = get_current_company(request)

            if data.get("uuid", None):
                instance = Session.objects.get(pk=data.get("uuid"))
                serializer = SessionSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = SessionSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:
            return error_response(e)


@api_view(["POST"])
def read_sessions(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        subjects = Session.objects.filter(company=company).order_by("-date_created")

        for subject in subjects:
            row = subject.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))