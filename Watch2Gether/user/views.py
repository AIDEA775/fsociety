from django.http import HttpResponse

def index(request):
    user = None

    if not request.user.is_authenticated:
        return HttpResponse("Please first login.")

