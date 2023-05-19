from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, "authpage_app/login.html")


def findP(request):
    return render(request, "authpage_app/findPassword.html")


def register(request):
    return render(request, "authpage_app/register.html")
