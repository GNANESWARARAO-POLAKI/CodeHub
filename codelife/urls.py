from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='codelife'
urlpatterns=[
    path('<int:contest_id>/register',views.register,name='register'),
    path('<int:contest_id>',views.codelife_contest,name='contest'),
    path('<int:contest_id>/details',views.contest_details,name='contest_details'),
    path('<int:contest_id>/add_question',views.add_or_edit_question,name="add_question"),
    path('<int:contest_id>/leaderboard',views.leaderboard,name='leaderboard'),
    path('edit_question/<int:question_id>',views.add_or_edit_question,name='edit_question'),
    path('<int:contest_id>/question/', views.questions, name='questions'),
    path('submit/<int:question_id>',views.submit,name='submit_question'),
    path('run_code/<int:question_id>',views.run_code,name='run_question'),
    path('save_temporary_code/',views.save_temporary_code,name='save_temporary_code'),
    path('<int:contest_id>/contest_results',views.contest_results,name='contest_results'),
    path('<int:contest_id>/mange_contest',views.manage_contest,name='mange_contest'),
    path('<int:contest_id>/manage_participant/<str:participant_name>',views.manage_participant,name='manage_participant'),
    path('add_life',views.add_life,name='add_life'),
    path('verify_passcode',views.verify_passcode,name='verify_passcode'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
