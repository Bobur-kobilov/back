# Generated by Django 2.0.4 on 2018-06-19 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0015_coinguide_coinguidelanguage_fileattachcoinguide'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinguide',
            name='abbreviation',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
