# Generated by Django 2.0.4 on 2018-06-11 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20180611_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dept_duty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dept_duty', to='account.DepartmentDuty'),
        ),
        migrations.AddField(
            model_name='user',
            name='dept_rank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dept_rank', to='account.DepartmentRank'),
        ),
        migrations.AddField(
            model_name='user',
            name='dept_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dept_type', to='account.DepartmentType'),
        ),
    ]
