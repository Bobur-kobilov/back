# Generated by Django 2.0.4 on 2018-06-21 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0028_auto_20180620_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinguide',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='logo_coinguide', to='boards.FileAttachment'),
        ),
    ]
