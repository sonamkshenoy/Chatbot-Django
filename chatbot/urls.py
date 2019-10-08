from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$',views.home),
    url(r'^options/',views.options),
    url(r'^start_conv/', include('conversation.urls')),
    url(r'^upload/', include('upload_dataset.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^personalize/', include('personalization.urls')),
]

urlpatterns += staticfiles_urlpatterns()
