from ..models.user import *
from ..views.common import *
import sys, traceback, os


def load_page(request):
	return render(request, 'lesson_update/lesson-updates.html')


def read(request):
	try:
		data = req_data(request, True)
		pagination = None
		lesson_update_header_list = []
		results = {
			'data': [],
			'total_records': None
		}

		if 'pagination' in data: pagination = data.pop("pagination", None)

		# Load lesson update headers
		lesson_update_header_qs = Lesson_update_header.objects.filter(is_active=True).order_by("-date", "-id")
		results['total_records'] = lesson_update_header_qs.count()

		if pagination:
			results.update(generate_pagination(pagination, lesson_update_header_qs))
			lesson_update_header_qs = lesson_update_header_qs [ results['starting'] : results['ending'] ]
		
		for lesson_update_header in lesson_update_header_qs:
			lesson_update_header_dict = lesson_update_header.get_dict()
			lesson_update_header_dict['lesson_update_detail_list'] = []

			# Load lesson update details
			lesson_update_detail_qs = Lesson_update_detail.objects.filter(lesson_update_header=lesson_update_header.pk)

			for lesson_update_detail in lesson_update_detail_qs:
				lesson_update_detail_dict = lesson_update_detail.get_dict()
				lesson_update_header_dict['lesson_update_detail_list'].append(lesson_update_detail_dict)

			lesson_update_header_list.append(lesson_update_header_dict)


		results['data'] = lesson_update_header_list
		
		return success_list(results, False)

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

		dprint(e)
		dprint(fname)

		return HttpResponse(e, status = 400)


def load_lesson_update_activities(request):
	try:
		lesson_update_activity_qs = To_dos_topic.objects.filter(is_active=True)
		lesson_update_activity_list = []

		for lesson_update_activity in lesson_update_activity_qs:
			lesson_update_activity_list.append(lesson_update_activity.get_dict())

		return success_list(lesson_update_activity_list, False)

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

		dprint(e)
		dprint(fname)
		dprint(sys.exc_traceback.tb_lineno)

		return HttpResponse(e, status = 400)