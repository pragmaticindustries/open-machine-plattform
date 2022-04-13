from django.urls import path

from omap.core import views

app_name = "core"

urlpatterns = [
    path("", views.TailwindDemoView.as_view()),
    path("dashboard", views.DashboardView.as_view()),
]
