# Generated by Django 4.1.4 on 2023-08-08 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibpage_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='P_summary',
            field=models.CharField(max_length=5000),
        ),
    ]
