# Generated by Django 3.2.6 on 2022-04-22 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_taskset_current_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskset',
            name='completed_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taskset',
            name='queued_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taskset',
            name='started_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
