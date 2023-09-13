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
    is_followed = False
    if request.user.is_authenticated:
        user_followed_perform = [
            perform["P_id"] for perform in request.user.followed_perform.values("P_id")
        ]
        is_followed = performance_data[0]["P_id"] in user_followed_perform
    p_location = performance_data[0]["L_name"].split()[0]
    location = list(Location.objects.filter(L_name__startswith=p_location).values())
    reviews = Review.objects.filter(P_id=pk)
    review_form = ReviewForm()
    user_id = request.user.username

    # if user_id:
    #    user_data = User.objects.filter(username__exact=user_id)
    #    user_age = user_data[0]['age']
    #    user_gender = user_data[0]['gender']
    # else:
    #    user_age = ''
    #    user_gender = ''
    # log_text = {'user_id': user_id, 'user_age': user_age, 'user_gender': user_gender, 'page': 'exhibpage', 'performance_name': performance_data[0]['P_name'], 'time': datetime.datetime.today()}

    total_rank = 0
    num_review = len(reviews)

    if num_review > 0:
        for review in reviews:
            total_rank += int(review.rank)
        avg_rank = float(total_rank / num_review)
    else:
        avg_rank = 0.0

    context = {
        "pk": pk,
        "exhibit": performance_data,
        "la": location[0]["L_la"],
        "lo": location[0]["L_lo"],
        "reviews": reviews,
        "forms": review_form,
        "avg_rank": avg_rank,
        "is_followed": is_followed,  # 추가
    }
    avg_rank
    # logging(log_text)

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
            review.Perform_id = pk
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
    with open("../test.log", "a", encoding="utf-8") as f:
        text = json.dumps(log_dict) + "\n"
        f.write(text)


@require_POST
def review_likes(request, performance_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_pk)

        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
        else:
            review.like_users.add(request.user)
        return redirect("exhibit:exhibition", performance_pk)
    return redirect("authpage_app:login")


def follow_perform(request, perform_id):
    if request.user.is_authenticated:
        perform = get_object_or_404(Performance, id=perform_id)
        person = request.user

        if perform in person.followed_perform.all():
            person.followed_perform.remove(perform)
            print("언팔로우")
        else:
            person.followed_perform.add(perform)
            print("팔로우")

    return redirect("exhibit:exhibition", perform_id)
