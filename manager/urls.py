from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login',views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('utilities', views.utilities, name="utilities"),
    path('jobs', views.jobs, name="assignedjobs"),
    path('announcements', views.announcements, name="announcements"),
    path('addapartment', views.addapartment, name="addapartment"),
    path('addannouncement', views.addannouncement, name="addannouncement"),
    path('mod', views.mod, name="mod"),
    path('viewapplications', views.viewapplications, name="viewapplications"),
    path('assign/<int:code>', views.assign, name="assign"),
    path('close/<int:code>', views.close, name="close"),
    path('requestutil/<int:util_code>', views.requestutil, name="requestutil"),
    path('viewapartmnet/<int:code>', views.viewapartment, name="viewapartment"),
    path('maketenant/<int:code>', views.maketenant, name="maketenant"),
    path('addemployee/<int:code>', views.addemployee, name="addemployee"),
    path('approve/<int:code>/<int:usercode>', views.approve, name="approve"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)