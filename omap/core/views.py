from django.http import HttpResponse
from django.views.generic import TemplateView


class DemoView(TemplateView):
    template_name = "omap/frontend/base.html"


class DashboardView(TemplateView):
    template_name = "omap/frontend/base_dashboard.html"


class TailwindDemoView(TemplateView):
    template_name = "omap/core/tailwinddemo.html"
