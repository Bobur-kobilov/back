# Generated by Django 2.0.4 on 2018-06-19 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0021_auto_20180619_2009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailynewsattachment',
            old_name='files',
            new_name='file_info',
        ),
    ]
