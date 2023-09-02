# Generated by Django 4.2 on 2023-08-27 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exhibpage_app", "0005_remove_review_like_review_like_users"),
        ("authpage_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="followed_perform",
            field=models.ManyToManyField(
                related_name="followers", to="exhibpage_app.performance"
            ),
        ),
    ]