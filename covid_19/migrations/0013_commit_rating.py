# Generated by Django 5.0 on 2024-05-17 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid_19', '0012_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
