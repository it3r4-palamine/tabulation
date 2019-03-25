from django.conf.urls import url
from api.views import question, download_data, login, answers, student, users, subject, enrollment, learning_center, \
    exercise ,course, session, program
urlpatterns = [

    url(r'^api-auth', login.ObtainAuthToken.as_view()),
    url(r'^get-data', login.GetData.as_view()),
    url(r'^sync-assessments', login.SyncAssessments.as_view()),
    url(r'^file-upload/', login.FileUpload.as_view()),
    url(r'^file-upload-ios', login.FileUploadIOS.as_view()),
    url(r'^sync-lesson-update', login.LessonUpdate.as_view()),


    url(r'^get-base64-photo', login.GetBase64Photo.as_view()),
    url(r'^get-photo', login.GetPhoto.as_view()),
    url(r'^get-question-photo', login.GetQuestionPhoto.as_view()),
    url(r'^get-answer-image-photo', login.GetAnswerImagePhoto.as_view()),

    url(r'^get-questions/$', answers.GetQuestionList.as_view()),
    url(r'^get-answers/(?P<question_id>[0-9]+)$', answers.GetAnswers.as_view()),

    url(r'^get-profile/$', users.GetUserProfile.as_view()),

    # YIAS Local
    url(r'^get-company-and-user-type/$', login.Get_company_and_user_types.as_view()),
    url(r'^get-programs-and-exercises/$', download_data.Get_programs_and_exercises.as_view()),
    url(r'^get-users/$', download_data.Get_users.as_view()),
    url(r'^get-settings/$', download_data.Get_settings.as_view()),
    url(r'^get-worksheets/$', download_data.Get_worksheets.as_view()),
    url(r'^get-sessions/$', download_data.Get_sessions.as_view()),

    url(r'^get_student_information/$', student.StudentInfo.as_view()),

    url(r'^get_student/', student.get_student),
    url(r'^get_students/$', student.get_students),
    url(r'^get_students_with_information/$', student.get_students_with_information),

    # AVSM API
    url(r'^enrollment/check_reference_no/$', enrollment.check_reference_no),
    url(r'^save_student_time_logs/$', student.save_student_time_logs),

    url(r'^subject/create/$', subject.SubjectAPIView.as_view()),
    url(r'^subject/read/$', subject.read_subjects),

    # Learning Materials

    url(r'^course/create/$', course.CourseAPIView.as_view()),
    url(r'^course/read/$', course.read_course),
    url(r'^course/read_course_programs/$', course.read_course_programs),

    url(r'^program/create/$', program.ProgramAPIView.as_view()),
    url(r'^program/read/$', program.read_programs),
    url(r'^program/read_program_sessions/$', program.read_program_sessions),

    url(r'^session/create/$', session.SessionAPIView.as_view()),
    url(r'^session/read/$', session.read_sessions),
    url(r'^session/read_session_exercise/$', session.read_session_exercise),

    url(r'^exercise/create/$', exercise.ExerciseAPIView.as_view()),
    url(r'^exercise/read/$', exercise.read_exercise),
    url(r'^exercise/read_exercise_questions/$', exercise.read_exercise_questions),

    url(r'^question/create/$', question.QuestionAPIView.as_view()),
    url(r'^question/get/(?P<uuid>[\w\-]+)/$', question.QuestionAPIView.as_view()),
    url(r'^question/read/$', question.read_questions),

    url(r'^learning_center/read/$', learning_center.LearningCenterAPI.as_view()),
    url(r'^learning_center/read/(?P<center_id>[0-9]+)$', learning_center.LearningCenterAPI.as_view()),

    # Student API
    # Get Student's Enrolled Courses/Programs
    url(r'^enrollment/read/$', enrollment.read_enrolled_programs),

    # Student Enrolls a Course
    url(r'^enroll_course/$', enrollment.enroll_course),

    # Get all session of student
    url(r'^read_student_sessions/$', session.read_student_sessions),
    url(r'^test_paypal/$', enrollment.test_paypal),



]

