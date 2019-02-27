from api.serializers import *

from django.db.models import *

# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

from web_admin.views.common import *

# MODELS
from web_admin.models.company_assessment import *
from web_admin.models.assessments import *
from web_admin.forms.assessments import *
from web_admin.models.multiple_choice import *


class GetUserProfile(APIView):

	def get(self,request):
		try:
			print("Gogoy")
			user_id = request.user.id
			user = User.objects.get(id=user_id).values()

			print user


			return Response("Success")
		except Exception as e:
			return Response(str(e), status = 500)