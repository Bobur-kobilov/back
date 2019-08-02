# Generated by Django 2.0.7 on 2018-07-04 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0032_auto_20180704_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinguide',
            name='currency',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='coinguidelanguage',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language', to='boards.CoinGuide'),
        ),
        migrations.AlterField(
            model_name='coinguideusefullink',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link', to='boards.CoinGuide'),
        ),
    ]