# Generated by Django 4.1.4 on 2023-05-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Exhibit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("E_name", models.CharField(max_length=200)),
                ("L_name", models.CharField(max_length=50)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("time", models.CharField(max_length=100, null=True)),
                ("fee", models.CharField(max_length=50, null=True)),
                ("url", models.CharField(max_length=500, null=True)),
                ("img", models.CharField(max_length=500, null=True)),
                ("summary", models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("L_name", models.CharField(max_length=50)),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
            ],
        ),
    ]
