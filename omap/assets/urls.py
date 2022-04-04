from django.urls import path

from omap.assets import views

app_name = "assets"

urlpatterns = [
    path("", views.demo, name="assets/home"),
]
