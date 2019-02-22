from ..serializers import *

from django.db.models import *

# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

from systech_account.views.common import *

# MODELS
from systech_account.models.company_assessment import *
from systech_account.models.assessments import *
from systech_account.forms.assessments import *
from systech_account.models.multiple_choice import *


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