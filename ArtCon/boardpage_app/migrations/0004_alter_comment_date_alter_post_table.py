# Generated by Django 4.2 on 2023-06-03 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boardpage_app", "0003_alter_post_options_post_board_name_post_hits_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateField(
                verbose_name=datetime.datetime(2023, 6, 4, 0, 44, 59, 59665)
            ),
        ),
        migrations.AlterModelTable(
            name="post",
            table="boardpage_app_post",
        ),
    ]