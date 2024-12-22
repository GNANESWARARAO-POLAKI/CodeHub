from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='codelife'
urlpatterns=[
    path('<int:contest_id>/register',views.register,name='register'),
    path('<int:contest_id>',views.codelife_contest,name='codelife_contest'),
    path('details/<int:contest_id>',views.contest_details,name='contest_details'),
    path('<int:contest_id>/add_question',views.add_question,name="add_question"),
    path('edit_question/<int:question_id>',views.edit_question,name='edit_question'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
