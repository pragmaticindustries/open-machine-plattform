from django.conf.urls import url

from omap.core import views

app_name = "assets"
urlpatterns = [
    url("", views.demo),
]
