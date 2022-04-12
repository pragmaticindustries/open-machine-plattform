from django.urls import path

from omap.core import views

app_name = "core"

urlpatterns = [
    path("", views.DemoView.as_view()),
    path("tw", views.TailwindDemoView.as_view()),
]
