# Generated by Django 2.0.7 on 2018-07-14 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy_manage', '0004_depositaddress_wallet_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletRule',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('currency', models.IntegerField()),
                ('target_rate', models.FloatField()),
            ],
            options={
                'db_table': 'wallet_rule',
            },
        ),
    ]