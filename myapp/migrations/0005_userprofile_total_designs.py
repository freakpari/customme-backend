# Generated by Django 4.2.23 on 2025-06-27 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_userprofile_profile_completion'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_designs',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
