# Generated by Django 2.2.3 on 2019-07-25 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_user_user_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="lite_api_user_id",
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
