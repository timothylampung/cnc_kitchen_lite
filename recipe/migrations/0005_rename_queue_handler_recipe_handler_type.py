# Generated by Django 3.2.6 on 2022-04-20 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_step_step_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='queue_handler',
            new_name='handler_type',
        ),
    ]
