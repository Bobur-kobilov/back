# Generated by Django 2.0.4 on 2018-06-18 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20180612_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='eng_name',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
