# Generated by Django 4.2 on 2023-08-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boardpage_app", "0003_remove_post_board_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="tag2",
            field=models.CharField(max_length=30, verbose_name="장르"),
        ),
        migrations.AlterField(
            model_name="post",
            name="tag3",
            field=models.CharField(max_length=30, verbose_name="지역"),
        ),
    ]