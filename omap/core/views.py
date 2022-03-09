from django.http import HttpResponse
from django.views.generic import TemplateView


def demo(request):
    return HttpResponse('<div class="text-5xl">Hallo</div>')


class TailwindDemoView(TemplateView):
    template_name = "omap/core/tailwinddemo.html"
