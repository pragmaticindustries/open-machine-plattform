from django.http import HttpResponse
from django.views.generic import TemplateView


class DemoView(TemplateView):
    template_name = "omap/frontend/base.html"


class DashboardView(TemplateView):
    template_name = "omap/frontend/base_dashboard.html"


class TailwindDemoView(TemplateView):
    template_name = "omap/core/tailwinddemo.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["display_hints"] = True
        return data


