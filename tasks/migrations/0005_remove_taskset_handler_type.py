# Generated by Django 3.2.6 on 2022-04-20 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_taskset_module_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskset',
            name='handler_type',
        ),
    ]