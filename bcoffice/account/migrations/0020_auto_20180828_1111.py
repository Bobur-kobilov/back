# Generated by Django 2.0.7 on 2018-08-28 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20180814_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='role',
            field=models.CharField(max_length=30),
        ),
    ]