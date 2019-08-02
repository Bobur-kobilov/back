# Generated by Django 2.0.4 on 2018-06-20 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0025_auto_20180620_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyNewsFileMap',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_attach_daily', to='boards.DailyNews')),
                ('file_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_daily', to='boards.FileAttachment')),
            ],
            options={
                'db_table': 'boards_daily_mapping',
            },
        ),
    ]