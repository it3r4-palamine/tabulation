from ..forms.assessments import *
from ..models.assessments import *
from ..views.common import *


def recommendations(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
		return render(request, 'recommendations/recommendations.html')

def create_dialog(request):
	return render(request, 'recommendations/dialogs/create_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		pagination = None

		filters = {}
		filters['is_active'] = True
		value_search = data.pop("value","")
		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		sort_by = generate_sorting(data.pop("sort",None))
		if value_search:
			filters['value__icontains'] = value_search
		filters['company'] = data['company']
		records = Assessment_recommendation.objects.filter(**filters).order_by(*sort_by)
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		data = []
		for record in records:
			row = record.get_dict()
			data.append(row)

		results['data'] = data
		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = Assessment_recommendation.objects.get(id=postdata.get('id',None))
			recommendation = Assessment_recommendation_form(postdata, instance=instance)
		except Assessment_recommendation.DoesNotExist:
			recommendation = Assessment_recommendation_form(postdata)

		if(recommendation.is_valid()):
			recommendation.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(recommendation.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def delete(request,id = None):
	try:
		try:
			record = Assessment_recommendation.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success()
		except Assessment_recommendation.DoesNotExist:
			raise_error("Recommendation doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)



