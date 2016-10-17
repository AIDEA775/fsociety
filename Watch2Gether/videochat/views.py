from django.shortcuts import render
from django.conf import settings
from social.backends.utils import load_backends


def index(request):
    """Index view, displays login mechanism"""
    backends = load_backends(settings.AUTHENTICATION_BACKENDS)
    context = {'available_backends': backends}
    return render(request, "videochat/index.html", context)
