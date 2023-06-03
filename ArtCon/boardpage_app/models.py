from django.db import models
from authpage_app.models import User
import datetime

# Create your models here.


class Post(models.Model):
    postname = models.CharField(max_length=50, verbose_name="글 제목")
    contents = models.CharField(max_length=500, verbose_name="글 내용")
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    date = models.DateTimeField(auto_now_add=True, verbose_name="글 작성일")
    board_name = models.CharField(max_length=32, default="test", verbose_name="게시판 종류")
    update_dttm = models.DateTimeField(auto_now=True, verbose_name="마지막 수정일")
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")

    def __str__(self):
        return self.postname

    class Meta:
        db_table = "boardpage_app_post"
        verbose_name = "게시판"
        verbose_name_plural = "게시판"


class Comment(models.Model):
    contents = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(datetime.datetime.now())

    def __str__(self):
        return str(
            {"contents": self.contents, "username": self.username, "date": self.date}
        )
