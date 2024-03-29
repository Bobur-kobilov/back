# Generated by Django 2.0.7 on 2018-08-22 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('policy_manage', '0005_walletrule'),
        ('coin_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawApply',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('wallet_type', models.CharField(max_length=30)),
                ('currency', models.IntegerField()),
                ('withdraw_volume', models.FloatField(default=0)),
                ('deposit_volume', models.FloatField(default=0)),
                ('etc_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(default=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proc_date', models.DateTimeField(blank=True, null=True)),
                ('deposit_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_wallet', to='policy_manage.DepositAddress')),
            ],
            options={
                'db_table': 'withdraw_apply',
            },
        ),
        migrations.CreateModel(
            name='WithdrawHistroy',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('currency', models.IntegerField()),
                ('deal_type', models.IntegerField()),
                ('volume', models.FloatField()),
                ('request_date', models.DateTimeField()),
                ('approval_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('txid', models.CharField(max_length=255)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_info', to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_address', to='policy_manage.DepositAddress')),
            ],
            options={
                'db_table': 'withdraw_history',
            },
        ),
        migrations.CreateModel(
            name='WithdrawReason',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'withdraw_reason',
            },
        ),
        migrations.AddField(
            model_name='withdrawapply',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reason', to='coin_account.WithdrawReason'),
        ),
        migrations.AddField(
            model_name='withdrawapply',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='withdrawapply',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='withdrawapply',
            name='withdraw_wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraw_wallet', to='policy_manage.DepositAddress'),
        ),
    ]
