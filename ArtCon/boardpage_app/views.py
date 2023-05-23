from django.shortcuts import render


# Create your views here.
def board(request):
    return render(request, "boardpage_app/board.html")


def write(request):
    return render(request, "boardpage_app/write.html")
