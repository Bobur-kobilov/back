# Generated by Django 2.0.4 on 2018-06-20 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0024_auto_20180620_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailynewsfilemap',
            name='board',
        ),
        migrations.RemoveField(
            model_name='dailynewsfilemap',
            name='file_info',
        ),
        migrations.DeleteModel(
            name='DailyNewsFileMap',
        ),
    ]
