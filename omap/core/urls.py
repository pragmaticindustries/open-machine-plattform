from django.conf.urls import url

from omap.core import views

app_name = "core"
urlpatterns = [
    url("tw", views.TailwindDemoView.as_view()),
    url("", views.demo),
]
