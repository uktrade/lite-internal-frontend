# Generated by Django 2.2.12 on 2020-04-30 11:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_user_lite_api_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="default_queue",
            field=models.UUIDField(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
        ),
    ]
