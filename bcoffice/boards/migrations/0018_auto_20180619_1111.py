# Generated by Django 2.0.4 on 2018-06-19 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0017_auto_20180619_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileattachcoinguide',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_attach_coinguide', to='boards.CoinGuide'),
        ),
    ]
