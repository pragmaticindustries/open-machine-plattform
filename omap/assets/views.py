from django.http import HttpResponse


def demo(request):
    return HttpResponse("Hey Yo")
