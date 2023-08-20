# Generated by Django 4.2 on 2023-08-11 09:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boardpage_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tag1",
            field=models.CharField(default=0, max_length=30, verbose_name="배우"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="post",
            name="tag2",
            field=models.CharField(default=0, max_length=10, verbose_name="장르"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="post",
            name="tag3",
            field=models.CharField(default=0, max_length=10, verbose_name="지역"),
            preserve_default=False,
        ),
    ]
