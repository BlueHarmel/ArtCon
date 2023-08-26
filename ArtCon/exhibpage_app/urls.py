from django.urls import path
from . import views

app_name = "exhibit"
urlpatterns = [
    path("<int:pk>/", views.exhibition, name="exhibition"),
    path("<int:pk>/reviews/", views.reviews_create, name="reviews_create"),
    path(
        "<int:performance_pk>/reviews/<int:review_pk>/delete/",
        views.reviews_delete,
        name="reviews_delete",
    ),
    path("<int:performance_pk>/reviews/<int:review_pk>/like/", views.review_likes, name="review_likes"),
]
