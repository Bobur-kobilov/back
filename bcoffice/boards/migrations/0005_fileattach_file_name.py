# Generated by Django 2.0.4 on 2018-05-31 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20180531_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileattach',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
