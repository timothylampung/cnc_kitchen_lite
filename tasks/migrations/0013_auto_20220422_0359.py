# Generated by Django 3.2.6 on 2022-04-22 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_auto_20220422_0335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskset',
            name='task_origin',
        ),
        migrations.AddField(
            model_name='taskset',
            name='origin_index',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]