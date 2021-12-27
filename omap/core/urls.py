from django.conf.urls import url

from omap.core import views

app_name = "core"
urlpatterns = [
    url("", views.demo),
]
