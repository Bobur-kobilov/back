# Generated by Django 2.0.4 on 2018-06-19 11:09

import boards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0020_coinguideusefullink_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyNewsAttachment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mapping_daily', to='boards.DailyNews')),
            ],
            options={
                'db_table': 'boards_daily_mapping',
            },
        ),
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('files', models.FileField(blank=True, null=True, upload_to=boards.models.user_attach_path)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'boards_file_attach',
            },
        ),
        migrations.AddField(
            model_name='dailynewsattachment',
            name='files',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attach_daily', to='boards.FileAttachment'),
        ),
        migrations.AddField(
            model_name='dailynews',
            name='primary_image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='primary_daily', to='boards.FileAttachment'),
            preserve_default=False,
        ),
    ]
