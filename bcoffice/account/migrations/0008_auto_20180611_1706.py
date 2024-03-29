# Generated by Django 2.0.4 on 2018-06-11 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_user_secret'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentDuty',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('duty_cd', models.CharField(max_length=5)),
                ('duty_name', models.CharField(max_length=100)),
                ('duty_eng_name', models.CharField(max_length=100)),
                ('status', models.CharField(default='ACTV', max_length=20)),
                ('close_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dept_duty',
            },
        ),
        migrations.CreateModel(
            name='DepartmentRank',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rank_cd', models.CharField(max_length=5)),
                ('rank_name', models.CharField(max_length=100)),
                ('rank_eng_name', models.CharField(max_length=100)),
                ('status', models.CharField(default='ACTV', max_length=20)),
                ('close_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dept_rank',
            },
        ),
        migrations.CreateModel(
            name='DepartmentType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dept_cd', models.CharField(max_length=5)),
                ('team_cd', models.CharField(max_length=5)),
                ('dept_name', models.CharField(max_length=100)),
                ('dept_eng_name', models.CharField(max_length=100, null=True)),
                ('managerial', models.BooleanField(default=False)),
                ('status', models.CharField(default='ACTV', max_length=20)),
                ('close_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dept_type',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='cell_phone',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='close_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='emp_no',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='joined_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default='ACTV', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
