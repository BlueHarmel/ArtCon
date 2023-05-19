from django.shortcuts import render


# Create your views here.
def exhibition(request):
    return render(request, "exhibpage_app/single.html")
