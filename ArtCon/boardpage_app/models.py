from django.db import models
from django.utils import timezone
from django.conf import settings


class Post(models.Model):
    postname = models.CharField(max_length=50, verbose_name="글 제목")
    contents = models.CharField(max_length=500, verbose_name="글 내용")
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="글 작성일")
    update_dttm = models.DateTimeField(auto_now=True, verbose_name="마지막 수정일")
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_articles"
    )
    tag1 = models.CharField(max_length=30, verbose_name="배우")
    tag2 = models.CharField(max_length=30, verbose_name="장르")
    tag3 = models.CharField(max_length=30, verbose_name="지역")

    def __str__(self):
        return self.postname

    class Meta:
        db_table = "boardpage_app_post"
        verbose_name = "게시판"
        verbose_name_plural = "게시판"


class Comment(models.Model):
    postname = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.CharField(max_length=100)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.contents
