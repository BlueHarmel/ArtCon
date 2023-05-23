from django.shortcuts import render


# Create your views here.
def recommend(request):
    return render(request, "recompage_app/recommend.html")
