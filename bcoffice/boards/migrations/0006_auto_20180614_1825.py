# Generated by Django 2.0.4 on 2018-06-14 09:25

import boards.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0005_fileattach_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqLanguage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'boards_faq_language',
            },
        ),
        migrations.CreateModel(
            name='FileAttachNotice',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('files', models.FileField(blank=True, null=True, upload_to=boards.models.user_attach_path)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(default='normal', max_length=50)),
            ],
            options={
                'db_table': 'boards_notice_attach',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('notice', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(default='ing', max_length=50)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('contents', models.TextField(blank=True, null=True)),
                ('read_count', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'boards_notice',
            },
        ),
        migrations.CreateModel(
            name='NoticeLanguage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=50)),
                ('board_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langauge_notice', to='boards.Notice')),
            ],
            options={
                'db_table': 'boards_notice_language',
            },
        ),
        migrations.CreateModel(
            name='PostLanguage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=50)),
                ('board_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langauge_post', to='boards.Post')),
            ],
            options={
                'db_table': 'boards_posts_language',
            },
        ),
        migrations.AlterModelTable(
            name='faq',
            table='boards_faq',
        ),
        migrations.AddField(
            model_name='fileattachnotice',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_attach_notice', to='boards.Notice'),
        ),
        migrations.AddField(
            model_name='faqlanguage',
            name='board_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langauge_faq', to='boards.Faq'),
        ),
    ]