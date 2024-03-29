# Generated by Django 2.0.7 on 2018-07-04 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0031_auto_20180621_0949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coinguide',
            old_name='abbreviation',
            new_name='abbr',
        ),
        migrations.RenameField(
            model_name='coinguide',
            old_name='func',
            new_name='algorithm',
        ),
        migrations.RenameField(
            model_name='coinguide',
            old_name='major',
            new_name='feature',
        ),
        migrations.RenameField(
            model_name='coinguide',
            old_name='total',
            new_name='total_volume',
        ),
        migrations.AddField(
            model_name='coinguide',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='icon_coinguide', to='boards.FileAttachment'),
        ),
        migrations.AlterField(
            model_name='coinguide',
            name='block_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
