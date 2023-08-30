from django.shortcuts import render, redirect, get_object_or_404
from .models import Performance, Location, Review
from .forms import ReviewForm
from authpage_app.models import User
from django.views.decorators.http import require_GET, require_POST
import json
import datetime

# 페이지 로드
def exhibition(request, pk):
    pk = pk  # request.GET.get("exhibitID")
    performance_data = list(Performance.objects.filter(id__exact=pk).values())
    p_location = performance_data[0]["L_name"].split()[0]
    location = list(Location.objects.filter(L_name__startswith=p_location).values())
    performance_data[0]["la"] = location[0]["L_la"]
    performance_data[0]["lo"] = location[0]["L_lo"]
    reviews = Review.objects.filter(P_id=pk)
    review_form = ReviewForm()
    user_id = request.user.username

    if user_id:
        user_data = User.objects.filter(username__exact=user_id)
        user_age = user_data[0]['age']
        user_gender = user_data[0]['gender']
    else:
        user_age = ''
        user_gender = ''
    log_text = {'user_id': user_id, 'user_age': user_age, 'user_gender': user_gender, 'page': 'exhibpage', 'performance_name': performance_data[0]['P_name'], 'time': datetime.datetime.today()}

    total_rank = 0
    num_review = len(reviews)

    if num_review > 0:
        for review in reviews:
            total_rank += int(review.rank)
        avg_rank = f"{(total_rank / num_review):.1f}"
    else:
        avg_rank = f"{0:.1f}"

    context = {
        "pk": pk,
        "exhibit": performance_data,
        "reviews": reviews,
        "forms": review_form,
        "avg_rank": avg_rank,
    }

    logging(log_text)

    return render(request, "exhibpage_app/single.html", context=context)


@require_POST
def reviews_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Performance, pk=pk)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.P_id = article
            review.username = request.user
            print("Before saving:", review)  # Debugging line
            review.save()
            print("After saving:", review)  # Debugging line
        else:
            print(review_form.errors)
        return redirect("exhibit:exhibition", pk)
    return redirect("authpage_app:login")


@require_POST
def reviews_delete(request, performance_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.username:
            review.delete()
    return redirect("exhibit:exhibition", performance_pk)

def logging(log_dict):
    with open('../test.log', 'a', encoding='utf-8') as f:
        text = json.dumps(log_dict) + '\n'
        f.write(text)