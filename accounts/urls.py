from django.contrib import admin
from . import views
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='accounts'

urlpatterns = [
    url(r'^$',views.choices, name="index"),
    url(r'^signup/$',views.signup_view, name='signup'),
    url(r'^login/$',views.login_view, name='login'),

]


urlpatterns += staticfiles_urlpatterns()
