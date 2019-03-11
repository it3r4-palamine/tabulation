# DJANGO REST
from rest_framework.response import Response
from rest_framework.views import APIView

# MODELS
from web_admin.models.company_assessment import *


class GetUserProfile(APIView):

	def get(self,request):
		try:
			user_id = request.user.id
			user = User.objects.get(id=user_id).values()

			return Response("Success")
		except Exception as e:
			return Response(str(e), status = 500)