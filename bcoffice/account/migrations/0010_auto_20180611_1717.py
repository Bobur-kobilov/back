# Generated by Django 2.0.4 on 2018-06-11 08:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20180611_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentduty',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='departmentrank',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
