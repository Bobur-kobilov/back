# Generated by Django 2.0.7 on 2018-07-05 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0034_auto_20180704_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailynewsfilemap',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_attach', to='boards.DailyNews'),
        ),
        migrations.AlterField(
            model_name='dailynewslanguage',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language', to='boards.DailyNews'),
        ),
        migrations.AlterField(
            model_name='faqlanguage',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language', to='boards.Faq'),
        ),
        migrations.AlterField(
            model_name='noticefilemap',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_attach', to='boards.Notice'),
        ),
        migrations.AlterField(
            model_name='noticelanguage',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language', to='boards.Notice'),
        ),
    ]
