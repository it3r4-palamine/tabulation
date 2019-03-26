from ..views.common import *


def payment_reports(request):
	return render(request, 'payment_reports/payment_reports.html')