# Generated by Django 3.2.6 on 2022-04-20 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_remove_taskset_handler_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskset',
            old_name='module_id',
            new_name='module',
        ),
    ]