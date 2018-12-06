
from django.conf.urls import url, handler404,patterns,include
from django.conf import settings as root_settings
from django.conf.urls.static import static

from systech_account.views import crud,assessments,transaction_type,company,company_assessment,settings,users,index,recommendations,generate_report,common, lesson_updates,user_logs,enrollment,session_evaluation
from systech_account.views import crud,assessments,transaction_type,company,company_assessment,settings,users,index,recommendations,generate_report,common, lesson_updates,user_logs,enrollment,payment_reports,student_reports

urlpatterns = [
	url(r'^common/pagination/$',common.pagination),

	# url(r'^$', assessments.home, name='home'),
	url(r'^$', index.loginpage, name='loginpage'),
	url(r'^login/$',index.log_in),
	url(r'^signin/$',index.signin),
	url(r'^logout/$',index.log_out,name="logout"),
	url(r'^register/$',index.register,name="register"),
	url(r'^assessments/$', assessments.home, name='home'),
	url(r'^assessments/create_dialog/$', assessments.create_dialog),
	url(r'^assessments/upload_dialog/$', assessments.upload_dialog),
	url(r'^assessments/create/$', assessments.create),
	url(r'^assessments/saveData/$', assessments.saveData),
	url(r'^assessments/upload/$', assessments.upload),
	url(r'^assessments/multiple_upload/$', assessments.multiple_upload),
	url(r'^assessments/multiple_upload_answer_keys/$', assessments.multiple_upload_answer_keys),
	url(r'^assessments/read/$', assessments.read),
	url(r'^assessments/generate_code/$', assessments.generate_code),
	url(r'^assessments/delete/(?P<id>[0-9]+)$', assessments.delete),
	url(r'^assessments/delete_choice/(?P<id>[0-9]+)$', assessments.delete_choice),
	url(r'^assessments/delete_effect/(?P<id>[0-9]+)$', assessments.delete_effect),
	url(r'^assessments/delete_finding/(?P<id>[0-9]+)$', assessments.delete_finding),
	url(r'^assessments/delete_image/(?P<id>[0-9]+)$', assessments.delete_image),
	url(r'^assessments/delete_answer/(?P<id>[0-9]+)$', assessments.delete_answer),
	url(r'^assessments/delete_multiple_answer/(?P<id>[0-9]+)$', assessments.delete_multiple_answer),

	url(r'^transaction_types/$', transaction_type.transaction_type, name='transaction_type'),
	url(r'^transaction_types/read/$', transaction_type.read),
	url(r'^transaction_types/create_dialog/$', transaction_type.create_dialog),
	url(r'^transaction_types/create/$', transaction_type.create),
	url(r'^transaction_types/delete/(?P<id>[0-9]+)$', transaction_type.delete),
	url(r'^transaction_types/delete_selected/$', transaction_type.delete_selected),
	url(r'^transaction_types/get_intelex_exercises/$', transaction_type.get_intelex_exercises),

	url(r'^company/$', company.company, name='company'),
	url(r'^company/read/$', company.read),
	url(r'^company/create_dialog/$', company.create_dialog),
	url(r'^company/create/$', company.create),
	url(r'^company/delete/(?P<id>[0-9]+)$', company.delete),
	url(r'^company/get_intelex_subjects/$', company.get_intelex_subjects),

	url(r'^company_assessment/$', company_assessment.company_assessment, name='company_assessment_redirect'),
	url(r'^company_assessment/read/$', company_assessment.read),
	url(r'^company_assessment/create_dialog/$', company_assessment.create_dialog),
	url(r'^company_assessment/create/$', company_assessment.create),
	url(r'^company_assessment/delete/(?P<id>[0-9]+)$', company_assessment.delete),
	url(r'^company_assessment/check_reference_no/$', company_assessment.check_reference_no),

	url(r'^import/$', settings.import_default, name='settings'),
	url(r'^import/read_module_columns/(?P<module_type>\w{0,50})$',settings.read_module_columns),
	url(r'^import/create_dialog/$', settings.create_dialog),
	url(r'^import/upload_dialog/$', settings.upload_dialog),
	url(r'^import/import_questions/$', settings.import_questions),
	url(r'^import/import_choices/$', settings.import_choices),
	url(r'^import/import_effects/$', settings.import_effects),
	url(r'^import/import_recommendations/$', settings.import_recommendations),
	url(r'^import/import_findings/$', settings.import_findings),
	url(r'^import/import_transaction_types/$', settings.import_transaction_types),
	
	url(r'^users/$', users.users, name='users'),
	url(r'^users/read/$', users.read),
	url(r'^users/create_dialog/$', users.create_dialog),
	url(r'^users/read_user_types/$', users.read_user_types),
	url(r'^users/create/$', users.create),
	url(r'^users/delete/(?P<id>[0-9]+)$', users.delete),
	url(r'^users/change_pass_dialog/$', users.change_pass_dialog),
	url(r'^users/change_password/$', users.change_password),
	url(r'^users/user_credits_summary/$', users.user_credits_summary),
	url(r'^users/get_intelex_students/$', users.get_intelex_students),
	url(r'^users/reconcile_student_credits/$', users.reconcile_student_credits),
	url(r'^users/read_user_reconciled_credits/$', users.read_user_reconciled_credits),
	url(r'^users/view_lesson_update/$', users.view_lesson_update),
	url(r'^users/read_user_credits/$', users.read_user_credits),
	
	url(r'^recommendations/$', recommendations.recommendations, name='recommendations'),
	url(r'^recommendations/read/$', recommendations.read),
	url(r'^recommendations/create_dialog/$', recommendations.create_dialog),
	url(r'^recommendations/create/$', recommendations.create),
	url(r'^recommendations/delete/(?P<id>[0-9]+)$', recommendations.delete),

	### ENROLLMENT
	url(r'^enrollments/enrollments/$', enrollment.enrollment, name='enrollment'),
	url(r'^enrollments/create_dialog/$', enrollment.create_dialog),
	url(r'^enrollments/read_enrollees/$', enrollment.read_enrollees),
	url(r'^enrollments/get_excess_time/$', enrollment.get_excess_time),
	url(r'^enrollments/save_enrollment/$', enrollment.save_enrollment),
	url(r'^enrollments/check_reference_no/$', enrollment.check_reference_no),
	url(r'^enrollments/read_enrollment/(?P<enrollment_id>\w{0,50})$$', enrollment.read_enrollment),
	url(r'^enrollments/delete_enrollment/$', enrollment.delete_enrollment),
	url(r'^enrollments/read_sessions_reconcile/$', enrollment.read_sessions_reconcile),
	url(r'^enrollments/session_handler_dialog/$', enrollment.session_handler_dialog),

	url(r'^enrollments/payment_reports/$', payment_reports.payment_reports, name='payment_reports'),
	url(r'^enrollments/student_reports/$', student_reports.student_reports, name='student_reports'),
	url(r'^enrollments/read_enrollment_report/$', student_reports.read_enrollment_report),

	url(r'^generate_report/(?P<generate_report_id>[0-9]+)/$',generate_report.generate_report,name="generate_report"),
	url(r'^generate_report/generate/$', generate_report.generate),
	url(r'^generate_report/download_dialog/$', generate_report.download_dialog),
	url(r'^generate_report_pdf/(?P<generate_report_id>[0-9]+)/$', generate_report.generate_pdf),
	url(r'^generate_report/read_chosen_recommendations/$', generate_report.read_chosen_recommendations),
	url(r'^generate_report/read_assessments/$', generate_report.read_assessments),
	url(r'^generate_report/delete_report/$', generate_report.delete_report),
	url(r'^generate_report/new_score/$', generate_report.new_score),

	url(r'^related_questions/$', assessments.related_questions),
	url(r'^assessments/read_related_questions/$', assessments.read_related_questions),
	url(r'^assessments/related_questions_create_dialog/$', assessments.related_questions_create_dialog),
	url(r'^assessments/related_questions_create/$', assessments.related_questions_create),
	url(r'^assessments/delete_related_questions/(?P<id>[0-9]+)$', assessments.delete_related_questions),


	### SETTINGS
	url(r'^settings/$', settings.settings, name='settings'),
	
	url(r'^settings/display_settings/$', settings.display_settings),
	url(r'^settings/display_settings_read/$', settings.display_settings_read),
	url(r'^settings/save_display_terms/$', settings.save_display_terms),
	
	url(r'^settings/user_types/$', settings.user_types),
	url(r'^settings/read_user_types/$', settings.read_user_types),
	url(r'^settings/user_types_create_dialog/$', settings.user_types_create_dialog),
	url(r'^settings/user_types_create/$', settings.user_types_create),
	url(r'^settings/user_types_delete/(?P<id>[0-9]+)$', settings.user_types_delete),
	
	url(r'^settings/to_dos/$', settings.to_dos),
	url(r'^settings/read_to_dos/$', settings.read_to_dos),
	url(r'^settings/to_dos_create_dialog/$', settings.to_dos_create_dialog),
	url(r'^settings/to_dos_create/$', settings.to_dos_create),
	url(r'^settings/to_dos_delete/(?P<id>[0-9]+)$', settings.to_dos_delete),
	
	url(r'^settings/math_symbols/$', settings.math_symbols),
	url(r'^settings/math_symbols_create_dialog/$', settings.math_symbols_create_dialog),
	url(r'^settings/math_symbols_create/$', settings.math_symbols_create),
	url(r'^settings/read_math_symbols/$', settings.read_math_symbols),
	url(r'^settings/math_symbols_delete/(?P<id>[0-9]+)$', settings.math_symbols_delete),

	url(r'^settings/schools/$', settings.schools),
	url(r'^settings/schools_create_dialog/$', settings.schools_create_dialog),
	url(r'^settings/schools_create/$', settings.schools_create),
	url(r'^settings/read_schools/$', settings.read_schools),
	url(r'^settings/schools_delete/(?P<id>[0-9]+)$', settings.schools_delete),

	url(r'^settings/grade_levels/$', settings.grade_levels),
	url(r'^settings/grade_levels_create_dialog/$', settings.grade_levels_create_dialog),
	url(r'^settings/grade_levels_create/$', settings.grade_levels_create),
	url(r'^settings/read_grade_levels/$', settings.read_grade_levels),
	url(r'^settings/grade_levels_delete/(?P<id>[0-9]+)$', settings.grade_levels_delete),

	# Lesson Updates
	url(r'^lesson_updates/load_page/$', lesson_updates.load_page),
	url(r'^lesson_updates/read/$', lesson_updates.read),
	url(r'^lesson_updates/load_lesson_update_activities/$', lesson_updates.load_lesson_update_activities),

	# User Logs
	url(r'^user_logs/$', user_logs.user_logs),
	url(r'^user_logs/read/$', user_logs.read),

    ### Session ###
	url(r'^student_sessions/$', session_evaluation.session_evaluation_list),
    url(r'^student_sessions/read_student_session/(?P<session_id>\w{0,50})$', session_evaluation.read_student_session),
	url(r'^student_sessions/create_dialog/$', session_evaluation.create_dialog),
	url(r'^student_sessions/check_reference_no/$', session_evaluation.check_reference_no),
	url(r'^student_sessions/read/$', session_evaluation.read),
	url(r'^student_sessions/create/$', session_evaluation.create),



]
urlpatterns += static(root_settings.STATIC_URL,document_root=root_settings.STATIC_ROOT)
urlpatterns += static(root_settings.MEDIA_URL,document_root=root_settings.MEDIA_ROOT)


if root_settings.ENVIRONMENT == "localhost":
	from django.conf.urls import patterns
	import debug_toolbar
	urlpatterns += patterns('',
	    url(r'^__debug__/', include(debug_toolbar.urls)),
	)