# Generated by Django 2.2.16 on 2021-12-09 15:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0009_auto_20211209_1042'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cooment',
            new_name='Comment',
        ),
    ]
