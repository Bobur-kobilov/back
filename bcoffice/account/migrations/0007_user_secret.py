# Generated by Django 2.0.4 on 2018-04-12 00:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180406_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='secret',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
