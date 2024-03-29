# Generated by Django 2.1.3 on 2018-12-14 09:23

from django.db import migrations
from bcoffice.migrate_init_value import Boards

def load_stores(apps, schema_editor):
    FaqCategory = apps.get_model('boards', 'FaqCategory')
    if (FaqCategory.objects.all()).exists() is False:
        for index, item in enumerate(Boards.DEFAULT_FAQ_CATEGORY):
            instance_category = FaqCategory.objects.create(
                id=index+1,
                category=item['category'],
                category_id=item['category_id'],
                lang=item['lang']
            )

class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0039_auto_20181024_0952'),
    ]

    operations = [
        migrations.RunPython(load_stores)
    ]
