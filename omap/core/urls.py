from django.urls import path

from omap.core import views

app_name = "core"

urlpatterns = [
    path("", views.demo),
    path("tw", views.TailwindDemoView.as_view()),
]
