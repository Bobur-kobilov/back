# Generated by Django 2.0.4 on 2018-04-06 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180405_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='update_at',
            new_name='updated_at',
        ),
    ]
