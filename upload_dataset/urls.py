from django.contrib import admin
from . import views
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='urls'

urlpatterns = [
    url(r'^$',views.upload, name="index"),
    url(r'^save/$',views.upload_save),

]


urlpatterns += staticfiles_urlpatterns()
