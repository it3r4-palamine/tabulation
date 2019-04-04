from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.serializers.enrollment import EnrollmentSerializer
from utils import dict_types, response_handler
from utils.model_utils import get_next
from utils.view_utils import remove_non_numeric_str
from web_admin.models import Enrollment
from utils.response_handler import *
from utils.model_utils import generate_random_code

class EnrollmentAPIView(APIView):

    def delete(self, request, id):
        instance = Enrollment.objects.get(id=id)
        instance.code = remove_non_numeric_str(str(datetime.now()))
        instance.is_deleted = True
        instance.save()

        return success_response()


@api_view(["POST"])
def read_enrolled_programs(request):
    try:
        results = {}
        records = []

        user = request.user.id

        query_set = Enrollment.objects.filter(user=user, is_active=True, is_deleted=False)

        for qs in query_set:
            row = qs.get_dict(dict_type=dict_types.STUDENT)
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


def check_existing_course(course_id, user):
    return Enrollment.objects.filter(course=course_id,user=user,is_deleted=False).exists()


@api_view(["POST"])
def enroll_course(request):
    try:
        data        = extract_json_data(request)
        user        = get_current_user(request)
        course_id   = data.get("uuid", None)
        company     = data.get("company", None)

        if check_existing_course(course_id, user):
            return error_response({"title" : "Invalid Enrollment", "message": "You are already enrolled to this Course"})

        enrollment = dict(
            code=generate_random_code(),
            user=user,
            course=course_id,
            company=company,
            is_active=False)

        serializer = EnrollmentSerializer(data=enrollment)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return success_response(response_data=response_handler.ENROLLED_SUCCESS)
    except Exception as e:
        return error_response(e, show_line=True)


@api_view(["POST"])
def check_reference_no(request):
    try:
        company     = get_current_company(request)
        query_set   = Enrollment.objects.filter(company=company).last()

        if not query_set and query_set.code:
            ref_no = "000000"
        else:
            ref_no = str(query_set.code)

        ref_no = get_next(ref_no)

        return success_response(ref_no)
    except Exception as e:
        return error_response(e, show_line=True)

import paypalrestsdk
import logging


@api_view(["POST"])
@permission_classes((AllowAny, ))
def test_paypal(request):
    try:
        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": "ATpJRFvQhoT_Jj9esCrxoIodM22QtG-qWV8A598_E4CLQnvlKtBQPGAXygPJ_Mif3Yrdiu1LqTcs_z0I",
            "client_secret": "EBUTPt-sXI1jbMnu-FGR2UsXu1p3oPkVT-0jUWK8v6xgVDu8W5xAScdXZoreTIweTrPaZXVg3GiCipWY"})

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/payment/execute",
                "cancel_url": "http://127.0.0.1:8000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "5.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print("Payment created successfully")
        else:
            print(payment.error)

        return success_response({"orderID" : 1})
    except Exception as e:
        return error_response(str(e))



