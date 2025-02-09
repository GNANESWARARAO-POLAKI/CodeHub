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
     path('save_temporary_code/',views.save_temporary_code,name='save_temporary_code'),
     path('<int:contest_id>/contest_results',views.ended_contests,name='contest_results'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
