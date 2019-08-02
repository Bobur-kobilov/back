# Generated by Django 2.0.4 on 2018-06-20 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0027_auto_20180620_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileattachcoinguide',
            name='post',
        ),
        migrations.AddField(
            model_name='coinguide',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logo_coinguide', to='boards.FileAttachment'),
        ),
        migrations.DeleteModel(
            name='FileAttachCoinGuide',
        ),
    ]