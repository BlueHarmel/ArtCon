# Generated by Django 4.2 on 2023-06-04 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boardpage_app", "0007_alter_comment_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateField(
                verbose_name=datetime.datetime(2023, 6, 4, 12, 46, 52, 227154)
            ),
        ),
    ]
