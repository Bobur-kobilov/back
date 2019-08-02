# Generated by Django 2.0.7 on 2018-08-28 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coin_account', '0008_auto_20180828_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawhistory',
            name='withdraw_apply',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='withdraw_apply_info', to='coin_account.WithdrawApply'),
            preserve_default=False,
        ),
    ]