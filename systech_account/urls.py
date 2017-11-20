
from django.conf.urls import url, handler404,patterns,include
from django.conf import settings as root_settings
from django.conf.urls.static import static

from systech_account.views import crud,assessments,transaction_type,company,company_assessment,settings,users,index,recommendations,generate_report,common

urlpatterns = [
	url(r'^common/pagination/$',common.pagination),

	# url(r'^$', assessments.home, name='home'),
	url(r'^$', index.loginpage, name='loginpage'),
	url(r'^login/$',index.log_in),
	url(r'^logout/$',index.log_out,name="logout"),
	url(r'^assessments/$', assessments.home, name='home'),
	url(r'^assessments/create_dialog/$', assessments.create_dialog),
	url(r'^assessments/create/$', assessments.create),
	url(r'^assessments/read/$', assessments.read),
	url(r'^assessments/delete/(?P<id>[0-9]+)$', assessments.delete),
	url(r'^assessments/delete_choice/(?P<id>[0-9]+)$', assessments.delete_choice),
	url(r'^assessments/delete_effect/(?P<id>[0-9]+)$', assessments.delete_effect),
	url(r'^assessments/delete_finding/(?P<id>[0-9]+)$', assessments.delete_finding),

	url(r'^transaction_types/$', transaction_type.transaction_type, name='transaction_type'),
	url(r'^transaction_types/read/$', transaction_type.read),
	url(r'^transaction_types/create_dialog/$', transaction_type.create_dialog),
	url(r'^transaction_types/create/$', transaction_type.create),
	url(r'^transaction_types/delete/(?P<id>[0-9]+)$', transaction_type.delete),

	url(r'^company/$', company.company, name='company'),
	url(r'^company/read/$', company.read),
	url(r'^company/create_dialog/$', company.create_dialog),
	url(r'^company/create/$', company.create),
	url(r'^company/delete/(?P<id>[0-9]+)$', company.delete),

	url(r'^company_assessment/$', company_assessment.company_assessment, name='company_assessment'),
	url(r'^company_assessment/read/$', company_assessment.read),
	url(r'^company_assessment/create_dialog/$', company_assessment.create_dialog),
	url(r'^company_assessment/create/$', company_assessment.create),
	url(r'^company_assessment/delete/(?P<id>[0-9]+)$', company_assessment.delete),
	url(r'^company_assessment/check_reference_no/$', company_assessment.check_reference_no),

	url(r'^import/$', settings.import_default, name='settings'),
	url(r'^import/read_module_columns/(?P<module_type>\w{0,50})$',settings.read_module_columns),
	url(r'^import/create_dialog/$', settings.create_dialog),
	url(r'^import/import_questions/$', settings.import_questions),
	url(r'^import/import_choices/$', settings.import_choices),
	url(r'^import/import_effects/$', settings.import_effects),
	url(r'^import/import_recommendations/$', settings.import_recommendations),
	url(r'^import/import_findings/$', settings.import_findings),
	
	url(r'^users/$', users.users, name='users'),
	url(r'^users/read/$', users.read),
	url(r'^users/create_dialog/$', users.create_dialog),
	url(r'^users/read_user_types/$', users.read_user_types),
	url(r'^users/create/$', users.create),
	url(r'^users/delete/(?P<id>[0-9]+)$', users.delete),
	url(r'^users/change_pass_dialog/$', users.change_pass_dialog),
	url(r'^users/change_password/$', users.change_password),
	
	url(r'^recommendations/$', recommendations.recommendations, name='recommendations'),
	url(r'^recommendations/read/$', recommendations.read),
	url(r'^recommendations/create_dialog/$', recommendations.create_dialog),
	url(r'^recommendations/create/$', recommendations.create),
	url(r'^recommendations/delete/(?P<id>[0-9]+)$', recommendations.delete),
	
	url(r'^generate_report/(?P<generate_report_id>[0-9]+)/$',generate_report.generate_report,name="generate_report"),
	url(r'^generate_report/generate/$', generate_report.generate),
	url(r'^generate_report/download_dialog/$', generate_report.download_dialog),
	url(r'^generate_report_pdf/(?P<generate_report_id>[0-9]+)/$', generate_report.generate_pdf),
	url(r'^generate_report/read_chosen_recommendations/$', generate_report.read_chosen_recommendations),
	url(r'^generate_report/read_assessments/$', generate_report.read_assessments),
	url(r'^generate_report/delete_report/$', generate_report.delete_report),
]
urlpatterns += static(root_settings.STATIC_URL,document_root=root_settings.STATIC_ROOT)
urlpatterns += static(root_settings.MEDIA_URL,document_root=root_settings.MEDIA_ROOT)
