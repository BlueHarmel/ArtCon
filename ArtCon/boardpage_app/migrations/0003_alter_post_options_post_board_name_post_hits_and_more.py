# Generated by Django 4.2 on 2023-06-03 15:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("boardpage_app", "0002_alter_comment_date_alter_post_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"verbose_name": "게시판", "verbose_name_plural": "게시판"},
        ),
        migrations.AddField(
            model_name="post",
            name="board_name",
            field=models.CharField(
                default="test", max_length=32, verbose_name="게시판 종류"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="hits",
            field=models.PositiveIntegerField(default=0, verbose_name="조회수"),
        ),
        migrations.AddField(
            model_name="post",
            name="update_dttm",
            field=models.DateTimeField(auto_now=True, verbose_name="마지막 수정일"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateField(
                verbose_name=datetime.datetime(2023, 6, 4, 0, 28, 51, 214420)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="contents",
            field=models.CharField(max_length=500, verbose_name="글 내용"),
        ),
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="글 작성일"),
        ),
        migrations.AlterField(
            model_name="post",
            name="postname",
            field=models.CharField(max_length=50, verbose_name="글 제목"),
        ),
        migrations.AlterField(
            model_name="post",
            name="username",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="작성자",
            ),
        ),
        migrations.AlterModelTable(
            name="post",
            table="post",
        ),
    ]