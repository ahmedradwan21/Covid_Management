# Generated by Django 5.0 on 2024-05-07 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid_19', '0002_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='risk',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
