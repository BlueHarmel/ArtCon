# Generated by Django 4.2 on 2023-06-04 05:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("boardpage_app", "0013_alter_comment_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"verbose_name": "댓글", "verbose_name_plural": "댓글"},
        ),
    ]