from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='core'

urlpatterns=[
     path('',views.home,name='home'),
     path('about',views.about,name='about'),
     path('register',views.register,name='register'),
     path('login/',views.user_login,name='login'),
     path('user/<str:username>',views.user_profile,name='user_profile'),
     path('edit_user',views.edit_profile,name='edit_profile'),
     path('contests',views.contests,name='contests'),
     path('create_contest',views.create_contest,name='create_contest'),
     path('logout/',views.user_logout,name='logout'),
     path('edit_contest/<int:contest_id>',views.edit_contest,name='edit_contest'),
     path('send_email',views.send_email_view,name='send_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
